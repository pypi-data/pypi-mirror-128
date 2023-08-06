//
// Created by jorge on 11/2/20.
//

#ifndef FTDCPARSER_FTDCPARSER_H
#define FTDCPARSER_FTDCPARSER_H

#include "iostream"
#include "vector"
#include <Chunk.h>
#include <Dataset.h>
#include <ParserTasksList.h>
#include <string_view>
#include <string>
#include "FileParsedData.h"


// From libbson
#include <bson/bson.h>

#include <boost/program_options.hpp>

class FTDCParser    {
public:

    //FTDCParser() : keepChunkStruct(false) {};

    bson_reader_t* open(std::string file_path);
    int parseFiles(std::vector<std::string> const *filePaths, bool onlyMetadata=false,  bool onlyMetricNames=false, bool lazyParsing=false);
    int parseFiles(std::string filePaths, bool onlyMetadata=false,  bool onlyMetricNames=false, bool lazyParsing=false);

    int parseInfoChunk (const bson_t *bson);
    std::vector<std::string> getMetricsNamesPrefixed(std::string prefix) ;
    std::vector<std::string> getMetricsNames();

    Dataset::MetricsPtr getMetric(std::string name, size_t start=Dataset::INVALID_TIMESTAMP, size_t end=Dataset::INVALID_TIMESTAMP);
 
    size_t getMetricLength() { return dataSet.getMetricLength(); }
    std::vector<Chunk*> getChunks() { return dataSet.getChunkVector(); }

    std::vector<std::string> getMetadata() { return metadata; }

    std::map<std::string,  Dataset::MetricsPtr> getHashMetrics() { return dataSet.getHashMetrics(); }

    //void keepChunkStructures(bool b) { keepChunkStruct = b; }

    std::vector<FileParsedData*> getParsedFileInfo() {return dataSet.getParsedFileInfo(); }


private:
     ParserTasksList parserTasks;
     Dataset dataSet;
     std::vector<std::string> metadata;
     //bool keepChunkStruct;
};




#endif //FTDCPARSER_FTDCPARSER_H