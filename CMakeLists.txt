cmake_minimum_required(VERSION 3.10)

project(SplineLab)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(includes)

file(GLOB SOURCES "src/*.cpp")

add_executable(main ${SOURCES})
