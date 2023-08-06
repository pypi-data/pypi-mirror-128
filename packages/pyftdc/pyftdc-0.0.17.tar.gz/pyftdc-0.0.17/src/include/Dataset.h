//
// Created by jorge on 12/16/20.
//

#ifndef FTDCPARSER_DATASET_H
#define FTDCPARSER_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <boost/thread/mutex.hpp>
#include <SampleLocation.h>
#include "Chunk.h"
#include "MergerTasksList.h"
#include "FileParsedData.h"

class Dataset {

public:
    typedef std::vector<uint64_t> Metrics;
    typedef std::vector<uint64_t>* MetricsPtr;

    Dataset() : samplesInDataset(0),  metricNames(0), lazyParsing(0) {};

    void addChunk(Chunk *pChunk);
    size_t getChunkCount() { return chunkVector.size(); }
    Chunk *getChunk(size_t n) { return (n < chunkVector.size()) ? chunkVector[n] : nullptr; }
    std::vector<Chunk *> getChunkVector() { return chunkVector; }
    size_t getMetricNames(std::vector< std::string> & metricNames);
    [[nodiscard]] size_t getMetricLength() const { return samplesInDataset; }

    MetricsPtr getMetric(std::string   metricName, size_t start, size_t end);

    std::map<std::string, MetricsPtr> getHashMetrics() { return hashMapMetrics; }
    size_t getMetricNamesCount() { return metricNames.size(); }
    void sortChunks();
    void FileParsed(const char * path, uint64_t start, uint64_t end, size_t samplesInFile);
    void   addMergedMetric(std::string   metricName, MetricsPtr data );
    std::vector<FileParsedData*> getParsedFileInfo() {  return this->filesParsed; }

    static const uint64_t FIRST_TIMESTAMP = UINT64_MAX;
    static const uint64_t LAST_TIMESTAMP = UINT64_MAX;
    static const uint64_t INVALID_TIMESTAMP = UINT64_MAX;

    void setLazyParsingFlag() { lazyParsing = true; }
    bool getLazyParsing() { return lazyParsing; }

private:
    void releaseChunks();
    std::vector<FileParsedData *> filesParsed;
    SampleLocation getLocationInMetric(size_t sample, bool fromStart);
    Dataset::MetricsPtr assembleMetricFromChunks(const std::string name,  SampleLocation startLocation, SampleLocation endLocation);

private:
    std::vector<Chunk*> chunkVector;
    size_t samplesInDataset;
    boost::mutex mu;
    std::vector<std::string> metricNames;
    std::map<std::string,  MetricsPtr>  hashMapMetrics;

    bool lazyParsing;


};


#endif //FTDCPARSER_DATASET_H
