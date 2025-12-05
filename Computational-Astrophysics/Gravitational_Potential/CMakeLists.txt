cmake_minimum_required(VERSION 3.10)
project(Gravitational_Potential)

set(CMAKE_CXX_STANDARD 17)

cmake_policy(SET CMP0072 NEW)

find_package(OpenGL REQUIRED)

add_executable(Gravitational_Potential main.cpp)

target_include_directories(Gravitational_Potential PRIVATE 
    ${OPENGL_INCLUDE_DIR}
    /usr/include
    /usr/include/GL
    /usr/include/GLFW
    /usr/include/glm
)

target_link_libraries(Gravitational_Potential
    ${OPENGL_gl_LIBRARY}
    glfw
    GLEW
    GL
    GLU
    m
)
