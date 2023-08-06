//
// Created by Jorge Imperial-Sosa on 9/19/21.
//

#ifndef PYFTDC_MERGERTASKSLIST_H
#define PYFTDC_MERGERTASKSLIST_H

#include <queue>
#include <MergerTask.h>
#include <boost/thread/mutex.hpp>

class MergerTasksList {
public:
    MergerTasksList() = default;;

    void push(std::string & metricName, int index, std::vector<Chunk *> *chunkVector, size_t metricLength);
    MergerTask *pop();
    bool empty();
private:
    boost::mutex mu;
    std::queue< MergerTask *> mergerTasks;
};


#endif //PYFTDC_MERGERTASKSLIST_H
