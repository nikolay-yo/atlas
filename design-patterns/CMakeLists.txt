cmake_minimum_required(VERSION 3.15)
project(design_patterns)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)

# Automatically include all .cpp files from the src directory
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Automatically include all .hpp files from the include directory (header files)
file(GLOB_RECURSE HEADERS "include/*.hpp")

# Add an executable
add_executable(${PROJECT_NAME}_run ${SOURCES} ${HEADERS})

# Include directories for header files
target_include_directories(${PROJECT_NAME}_run PRIVATE ${CMAKE_SOURCE_DIR}/include)
