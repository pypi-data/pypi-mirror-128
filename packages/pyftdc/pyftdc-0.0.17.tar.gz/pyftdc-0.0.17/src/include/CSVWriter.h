//
// Created by Jorge Imperial-Sosa on 1/16/21.
//

#ifndef FTDCPARSER_CSVWRITER_H
#define FTDCPARSER_CSVWRITER_H

#include "FTDCParser.h"

class CSVWriter {

public:
    static int OutputMultipleFiles(FTDCParser *pParser, std::string path,
                                   std::vector<std::string> metrics,
                                    bool timestamps,
                                    std::string start,  std::string end);
    static int OutputSingleFile(FTDCParser *pParser, std::string prefix, std::vector<std::string> metrics,
                                bool timestamps,
                                std::string start, std::string end);

private:
    static void writer(std::string metricName, std::string parsedFile, const uint64_t *timestamps, size_t samples, uint64_t *metric_values,   std::string start,  std::string end);
};


#endif //FTDCPARSER_CSVWRITER_H
