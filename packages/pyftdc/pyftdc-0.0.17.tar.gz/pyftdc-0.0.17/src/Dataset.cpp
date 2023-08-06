//
// Created by jorge on 12/16/20.
//
#include "include/Dataset.h"
#include "MergerTask.h"
#include "MergerTasksList.h"
#include "SampleLocation.h"
#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/thread.hpp>

namespace logging = boost::log;

size_t
Dataset::getMetricNames(std::vector<std::string> & metrics) {

    if (metricNames.empty()) {
        if (chunkVector.size() > 0) {

            if (lazyParsing && (chunkVector[0]->getUncompressedSize() == 0)) {
                // miau the first chunk, so we have metric names.
                chunkVector[0]->miau();
            }
            chunkVector[0]->getMetricNames(metricNames);
        }
    }

    metrics = metricNames;
    return metrics.size();
}

void
Dataset::addChunk(Chunk *pChunk) {

    // Critical section
    mu.lock();
    chunkVector.emplace_back(pChunk);

    // total size of samplesInDataset
    samplesInDataset += pChunk->getSamplesCount();

    // Append metrics here.
    mu.unlock();
}


void
Dataset::addMergedMetric(std::string   metricName,  Dataset::MetricsPtr data) {

    // Critical section
    mu.lock();
    hashMapMetrics.emplace( metricName, data);
    // Append metrics here.
    mu.unlock();
}

void
Dataset::sortChunks() {
    struct {
        bool operator()(Chunk *a, Chunk *b) const { return a->getId() < b->getId(); }
    } compare;
    std::sort(chunkVector.begin(), chunkVector.end(), compare);
}


Dataset::MetricsPtr
Dataset::getMetric(std::string   metricName, size_t start, size_t end)
{
    auto start_chunk_pos = getLocationInMetric(start, true);
    auto end_chunk_pos = getLocationInMetric(end, false);

    // TODO:  in case of lazy parsing, we should be  parsing here
    if (lazyParsing) { ;
        // for chunks between start and end, start parser threads
        for (auto chunkNumber = start_chunk_pos.getChunkLoc(); chunkNumber<=end_chunk_pos.getChunkLoc(); ++chunkNumber ) {
            if (chunkVector[chunkNumber]->getUncompressedSize() == 0)
                chunkVector[chunkNumber]->miau();
        }
    }

    Dataset::MetricsPtr p =  assembleMetricFromChunks(metricName, start_chunk_pos, end_chunk_pos);

    return p;
}

void
Dataset::FileParsed(const char * filePath,
                    uint64_t start, uint64_t end,
                    size_t samples) {

    int metricsNameLen = 0;
    for (auto chunk : chunkVector) {

        auto currMetricLen = chunk->getMetricsCount();
        if (metricsNameLen != 0  && metricsNameLen!=currMetricLen) {
            BOOST_LOG_TRIVIAL(debug) << "Number of metrics differ from chunk to chunk:" << metricsNameLen << "!= " << currMetricLen;
        }

        if (metricsNameLen!=currMetricLen) {
            metricNames.clear();
            chunk->getMetricNames(metricNames);
            metricsNameLen = currMetricLen;
        }
    }

    auto fileData = new FileParsedData(filePath, start, end, samples);
    filesParsed.emplace_back(fileData);
}


SampleLocation
Dataset::getLocationInMetric(size_t sample, bool fromStart) {

    auto chunkPos = Chunk::INVALID_CHUNK_NUMBER;
    auto samplePos = Chunk::INVALID_TIMESTAMP_POS;

    // Easy cases
    if (sample == Dataset::INVALID_TIMESTAMP) {
        if (fromStart) { // first sample of first chunk
            chunkPos = 0;
            samplePos = 0;
        }
        else { // last sample of last chunk
            chunkPos = chunkVector.size()-1;
            samplePos =  ChunkMetric::MAX_SAMPLES-1;
        }

        return  SampleLocation(chunkPos, samplePos);
    }

    //
    int chunkNumber = 0;
    for (auto c: chunkVector) {
        if (sample >= c->getStart() && sample <= c->getEnd()) {  // this is the chunk
            chunkPos = chunkNumber;
            // Timestamps 'start' metrics are always the 0-th position
            auto ts = c->getMetric(0);
            for (int i = 0; i < ChunkMetric::MAX_SAMPLES; ++i) {
                if (ts->values[i] >= sample) {
                    samplePos = i;

                    if (i ==0 && !fromStart) {
                        // actually previous chunk
                        samplePos = ChunkMetric::MAX_SAMPLES - 1;
                        --chunkPos;
                    }
                    break;
                }
            }
            break;
        }
        ++chunkNumber;
    }
    SampleLocation pos(chunkPos,samplePos);
    return pos;
}

Dataset::MetricsPtr
Dataset::assembleMetricFromChunks(const std::string metricName, SampleLocation startLocation, SampleLocation endLocation) {

    // chunks and positions
    auto startChunk = startLocation.getChunkLoc();
    auto startSamplePos =  startLocation.getSampleLoc();

    auto endChunk = endLocation.getChunkLoc();
    auto endSamplePos = endLocation.getSampleLoc();

    Dataset::MetricsPtr p = new std::vector<uint64_t>;
    if (endChunk == startChunk) {
        auto sample_count = endSamplePos - startSamplePos;
        p->reserve(sample_count);
        auto c = chunkVector[startChunk]->getMetric(metricName);
        p->assign(c + startSamplePos, c + endSamplePos);
    }
    else {

        size_t sampleCount = (endChunk-startChunk)*ChunkMetric::MAX_SAMPLES;
        BOOST_LOG_TRIVIAL(info) << "Metric: '" << metricName << "'. Reserving for " << sampleCount << " samples.";
        p->reserve(sampleCount);

        // first chunk
        auto c = chunkVector[startChunk]->getMetric(metricName);
        p->assign(c, c + (ChunkMetric::MAX_SAMPLES - startSamplePos));
        // Append chunks
        for (int i = startChunk + 1; i < endChunk; ++i) {
            c = chunkVector[i]->getMetric(metricName);
            p->insert(p->end(), c, c + ChunkMetric::MAX_SAMPLES);
        }

        // Append last chunk
        c = chunkVector[endChunk]->getMetric(metricName);
        p->insert(p->end(), c, c + endSamplePos);


    }
    return p;
}

