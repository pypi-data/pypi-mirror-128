//
// Created by Jorge Imperial-Sosa on 9/19/21.
//

#ifndef PYFTDC_MERGERTASK_H
#define PYFTDC_MERGERTASK_H

#include <string>
#include <Chunk.h>

class MergerTask {

public:
    MergerTask(std::string metricName, int index, std::vector<Chunk *> *chunkVector, size_t metricLength) {
        this->metricName = metricName;
        this->index = index;
        this->chunkVector = chunkVector;
        this->chunkCount = chunkVector->size();
        this->metricLength = metricLength;
    }
    [[nodiscard]] int getIndex() const { return index; }
    [[nodiscard]] size_t getChunkCount() const { return chunkCount; }
    [[nodiscard]] std::vector<Chunk *> *getChunkVector() const {
        return chunkVector;
    }
    [[nodiscard]] const std::string &getMetricName()  const {
        return metricName;
    }
    [[nodiscard]] size_t getMetricLength() const { return metricLength; }

private:
    std::string metricName;
    int index;
    std::vector<Chunk*> *chunkVector;
    size_t chunkCount;
    size_t metricLength;
};


#endif //PYFTDC_MERGERTASK_H
