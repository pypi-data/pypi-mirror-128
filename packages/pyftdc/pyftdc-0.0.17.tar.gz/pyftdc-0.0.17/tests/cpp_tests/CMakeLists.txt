project(Boost_Tests_run)

find_package (Boost REQUIRED COMPONENTS unit_test_framework)

add_executable (${PROJECT_NAME}
        basic_tests.cpp
        ${CMAKE_SOURCE_DIR}/src/CSVWriter.cpp
        ${CMAKE_SOURCE_DIR}/src/Dataset.cpp
        ${CMAKE_SOURCE_DIR}/src/ParserTask.cpp
        ${CMAKE_SOURCE_DIR}/src/Chunk.cpp
        ${CMAKE_SOURCE_DIR}/src/FTDCParser.cpp
        ${CMAKE_SOURCE_DIR}/src/ParserTasksList.cpp
        ${CMAKE_SOURCE_DIR}/src/ConstDataRangeCursor.cpp
        ${CMAKE_SOURCE_DIR}/src/ChunkMetric.cpp
        ../../src/parser/Configuration.cpp
        ../../src/parser/Configuration.h
        ../../src/MergerTask.cpp
        ../../src/include/MergerTask.h
        ../../src/MergerTasksList.cpp
        ../../src/include/MergerTasksList.h ../../src/SampleLocation.cpp ../../src/SampleLocation.h)

target_include_directories (${PROJECT_NAME}  PUBLIC
        ${Boost_INCLUDE_DIRS}
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/src/include
        ${CMAKE_SOURCE_DIR}/src/mongo-c-driver/src/libbson/src
        ${CMAKE_CURRENT_BINARY_DIR}/src/mongo-c-driver/src/libbson/src/bson
)

target_link_directories(${PROJECT_NAME} PUBLIC
        ${CMAKE_CURRENT_BINARY_DIR}/../../src/mongo-c-driver/src/libbson
)

target_link_libraries (${PROJECT_NAME}
        ${Boost_LIBRARIES}
        Boost::log
        bson-static-1.0.a
)