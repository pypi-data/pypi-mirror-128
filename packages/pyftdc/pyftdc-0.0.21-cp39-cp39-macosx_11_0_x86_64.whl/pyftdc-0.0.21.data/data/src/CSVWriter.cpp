//
// Created by Jorge Imperial-Sosa on 1/16/21.
//

#include "include/CSVWriter.h"

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/thread.hpp>

#include <fstream>
#include <filesystem>
#include <ctime>

static
std::string
tm2StringDateTime(tm *gmtm ) {

    std::stringstream dateTime;
    dateTime << gmtm->tm_year+1900  << "/"
             << std::setfill('0') << std::setw(2) << gmtm->tm_mon+1 << "/"
             << std::setfill('0') << std::setw(2) << gmtm->tm_mday
             <<  " "
            << std::setfill('0') << std::setw(2) << gmtm->tm_hour <<  ":"
            << std::setfill('0') << std::setw(2) << gmtm->tm_min << ":"
            << std::setfill('0') << std::setw(2) << gmtm->tm_sec;

    return dateTime.str();
}

int
CSVWriter::OutputSingleFile(FTDCParser *pParser, std::string prefix,  std::vector<std::string> metrics,  bool timestamps,
                            std::string start, std::string end){

        std::ofstream  out_file;

        out_file.open(prefix, std::ios::out);

        // Get timestamp
        auto  ts_metric = pParser->getMetric(  "start"); /// ALL OF IT.

        // Write metrics header
        std::vector<std::vector< uint64_t>*> mm;

        out_file << "timestamp";
        for (auto &metric_name : metrics) {
            BOOST_LOG_TRIVIAL(info) << "ChunkMetric: " << metric_name;

            auto metric_values = pParser->getMetric(metric_name);

            if (metric_values->size() == 0) {  // getMetricsCopy(metric_name)) { ;
                BOOST_LOG_TRIVIAL(error) << "No metric named '" << metric_name << "' was found in parsed data.";
            }
            else {
                mm.push_back(metric_values);
                out_file << "," << metric_name;
            }
        }
        out_file << std::endl;

        // Output
        size_t l = 0;

        for (size_t i=0; i<ts_metric->size(); ++i) {
            time_t t = ts_metric->at(i)  / 1000;

            auto dateTime = tm2StringDateTime(gmtime(&t));

            if (start.empty() || dateTime >= start) {
               if (end.empty() || dateTime < end) {

                   if (timestamps)
                       out_file << (ts_metric->at(i)/1000);
                   else
                       out_file << dateTime;

                   for (auto &m : mm)
                       out_file << "," << m->at(l) ;

                   out_file << std::endl;
               }
            }
            ++l;
        }

        out_file.close();

    return 0;
}

int
CSVWriter::OutputMultipleFiles(FTDCParser *pParser, std::string prefix,
                    std::vector<std::string> metrics,
                    bool timestamps,
                    std::string start,  std::string end){

    std::vector< boost::thread *> writeThreads;

    for (int metric = 0; metric < metrics.size(); ++metric) {

        // Construct path to to output file
        std::string outFileName = prefix;
        outFileName += "." + metrics[metric] + ".csv";

        std::vector<std::string> thisMetric;
        thisMetric.emplace_back(metrics[metric]);
        OutputSingleFile(pParser, outFileName, thisMetric, timestamps, start, end);
    }

    return 0;
}
