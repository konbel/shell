cmake_minimum_required(VERSION 4.1)
project(shell)

set(CMAKE_CXX_STANDARD 20)

file(GLOB_RECURSE SOURCES "src/*.cpp" "src/*.h")

add_executable(shell ${SOURCES})
