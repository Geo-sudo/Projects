cmake_minimum_required(VERSION 3.10)
project(Algorithm_Visualizer)

set(SFML_STATIC_LIBRARIES TRUE)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(SFML 3 REQUIRED COMPONENTS Graphics Window System)

add_executable(Algorithm_Visualizer main.cpp)
target_compile_definitions(Algorithm_Visualizer PRIVATE SFML_STATIC)

target_link_libraries(Algorithm_Visualizer PRIVATE 
    SFML::Graphics
    SFML::Window
    SFML::System
)