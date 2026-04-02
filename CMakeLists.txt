cmake_minimum_required(VERSION 3.10)

project(SplineLab)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python interpreter and development files
find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Try to find pybind11 via CMake config first
find_package(pybind11 CONFIG QUIET)

if(NOT pybind11_FOUND)
    # Fallback: find pybind11 in common virtual environment locations
    find_path(PYBIND11_INCLUDE_DIR
        NAMES pybind11/pybind11.h
        PATHS
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/lib/python*/site-packages/pybind11/include
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Lib/site-packages/pybind11/include
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/include
        )
    
    if(NOT PYBIND11_INCLUDE_DIR)
        message(FATAL_ERROR "pybind11 not found. Please install it in your virtual environment.")
    endif()
endif()

# List sources explicitly (avoid GLOB for better reliability)
set(SOURCES
    src/main.cpp
    src/solver.cpp
    # Add your other .cpp files here
)

add_executable(main ${SOURCES})

# Set C++ standard for the target
set_target_properties(main PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
)

# Include directories
target_include_directories(main PRIVATE includes)

# Handle pybind11 and Python includes
if(pybind11_FOUND)
    # pybind11 config will automatically handle Python dependencies
    target_link_libraries(main pybind11::headers)
    target_link_libraries(main Python::Python)
else()
    # Manual setup
    target_include_directories(main PRIVATE ${PYBIND11_INCLUDE_DIR})
    target_include_directories(main PRIVATE ${Python_INCLUDE_DIRS})
    target_link_libraries(main ${Python_LIBRARIES})
endif()

# Windows-specific: Set Python version for consistent searching
if(WIN32)
    # This helps CMake find the correct Python version
    set(Python_FIND_REGISTRY "HKEY_CURRENT_USER HKEY_LOCAL_MACHINE")
endif()

# Optional: Show found paths for debugging
message(STATUS "Python includes: ${Python_INCLUDE_DIRS}")
message(STATUS "Python libraries: ${Python_LIBRARIES}")
if(pybind11_FOUND)
    message(STATUS "Using pybind11 config")
else()
    message(STATUS "pybind11 include dir: ${PYBIND11_INCLUDE_DIR}")
endif()