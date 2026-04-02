cmake_minimum_required(VERSION 3.10)

project(SplineLab)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Better: Use pybind11's CMake config if available
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    # Fallback: try to find it in common locations
    find_path(PYBIND11_INCLUDE_DIR
        NAMES pybind11/pybind11.h
        PATHS
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/lib/python*/site-packages/pybind11/include
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Lib/site-packages/pybind11/include
        )
    if(NOT PYBIND11_INCLUDE_DIR)
        message(FATAL_ERROR "pybind11 not found")
    endif()
endif()

# List sources explicitly (recommended)
set(SOURCES
    src/main.cpp
    # Add your other .cpp files here
)

add_executable(main ${SOURCES})

# Use target_include_directories instead
target_include_directories(main PRIVATE includes)

if(pybind11_FOUND)
    target_link_libraries(main pybind11::headers)
else()
    target_include_directories(main PRIVATE ${PYBIND11_INCLUDE_DIR})
endif()