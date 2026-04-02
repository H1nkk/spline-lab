cmake_minimum_required(VERSION 3.10)

project(SplineLab)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python (required for pybind11)
find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Find pybind11 using Python to get the correct paths
execute_process(
    COMMAND ${Python_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(PYBIND11_CMAKE_DIR AND EXISTS ${PYBIND11_CMAKE_DIR})
    set(pybind11_DIR ${PYBIND11_CMAKE_DIR})
    find_package(pybind11 CONFIG REQUIRED)
    set(PYBIND11_FOUND_VIA_CMAKE TRUE)
    message(STATUS "Found pybind11 via Python module at: ${pybind11_DIR}")
else()
    message(STATUS "pybind11 not found via Python, trying manual method...")
    # Fallback to manual method
    find_path(PYBIND11_INCLUDE_DIR
        NAMES pybind11/pybind11.h
        PATHS
            # Linux/macOS paths
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/lib/python*/site-packages/pybind11/include
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/include
            # Windows paths
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Lib/site-packages/pybind11/include
            ${CMAKE_CURRENT_SOURCE_DIR}/.venv/include
        )
    if(NOT PYBIND11_INCLUDE_DIR)
        message(FATAL_ERROR "pybind11 not found. Please install it: pip install pybind11")
    endif()
    set(PYBIND11_FOUND_VIA_CMAKE FALSE)
endif()

# List your source files
set(SOURCES
    src/main.cpp
    src/solver.cpp
    # Add your other .cpp files here
)

# Create Python module
if(PYBIND11_FOUND_VIA_CMAKE)
    # Use pybind11's built-in function (recommended)
    pybind11_add_module(splinelab ${SOURCES})
else()
    # Manual module creation
    add_library(splinelab MODULE ${SOURCES})
    target_include_directories(splinelab PRIVATE ${PYBIND11_INCLUDE_DIR})
    target_include_directories(splinelab PRIVATE ${Python_INCLUDE_DIRS})
    target_link_libraries(splinelab ${Python_LIBRARIES})
endif()

# Add your project-specific include directories
target_include_directories(splinelab PRIVATE includes)

# Set C++ standard for the target
set_target_properties(splinelab PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
    POSITION_INDEPENDENT_CODE ON
)

# Set platform-specific module suffix
if(WIN32)
    set_target_properties(splinelab PROPERTIES SUFFIX ".pyd")
elseif(APPLE)
    set_target_properties(splinelab PROPERTIES SUFFIX ".so")
else()
    set_target_properties(splinelab PROPERTIES SUFFIX ".so")
endif()

# Auto-copy to python directory
set(PYTHON_SCRIPTS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python")
file(MAKE_DIRECTORY ${PYTHON_SCRIPTS_DIR})

add_custom_command(TARGET splinelab POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:splinelab>
        ${PYTHON_SCRIPTS_DIR}
    COMMENT "Copying splinelab module to ${PYTHON_SCRIPTS_DIR}"
)

# Optional: Show debug information
message(STATUS "Building Python module: splinelab")
message(STATUS "Python version: ${Python_VERSION}")
message(STATUS "Python includes: ${Python_INCLUDE_DIRS}")
message(STATUS "Python libraries: ${Python_LIBRARIES}")
if(PYBIND11_FOUND_VIA_CMAKE)
    message(STATUS "Using pybind11 from: ${pybind11_DIR}")
else()
    message(STATUS "Using pybind11 include: ${PYBIND11_INCLUDE_DIR}")
endif()