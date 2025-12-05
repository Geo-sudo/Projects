#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <glm/glm.hpp>
using std::cout;
using std::endl;
using std::vector;
using glm::dvec2;
using glm::dot;
using glm::normalize;

const double G = 6.67430e-11f; // m³·kg⁻¹·s⁻²
const double scale_factor = 1.0/(1.1*1.496e11); // AU⁻¹
const float dt = 86400.0f; // seconds·frame⁻¹


class Body {
public:
    dvec2 position;
    dvec2 velocity;
    double radius, mass;
    int segments;
    vector<float> vertices;
    vector<float> color;

    Body(double x_, double y_, double vel_x_, double vel_y_, double mass_, double radius_, int segments_, vector<float> color_ = {1.0f, 1.0f, 1.0f}){
        position[0]=x_; position[1]=y_; velocity[0]=vel_x_; velocity[1]=vel_y_; mass = mass_; radius=radius_; segments = segments_; color=color_;
        vertices = genCircle(segments);
    }

    vector<float> genCircle(int segments){
        vector<float> vertices;
        vertices.push_back(0.0f);
        vertices.push_back(0.0f);
        vertices.push_back(0.0f);
        for(int i=0; i <= segments; i++){
            float angle = 2.0f * M_PI * float(i)/float(segments);
            vertices.push_back(cosf(angle)); 
            vertices.push_back(sinf(angle));
            vertices.push_back(0.0f);
    }
    return vertices;
    }

    void render(GLuint shaderProgram){
        GLint radiusLoc = glGetUniformLocation(shaderProgram, "radius");
        GLint offsetLoc = glGetUniformLocation(shaderProgram, "offset");
        GLint colorLoc = glGetUniformLocation(shaderProgram, "bodyColor");

        float scaledRadius = static_cast<float>(radius);
        float scaled_X = static_cast<float>(position[0] * scale_factor);
        float scaled_Y = static_cast<float>(position[1] * scale_factor);

        glUniform2f(offsetLoc, scaled_X, scaled_Y);
        glUniform1f(radiusLoc, scaledRadius);
        glUniform3fv(colorLoc, 1, color.data());
    }

};

void gravitas(vector<Body>& bodies, float dt){
    vector<dvec2> accelerations(bodies.size());

    for(size_t i=0; i < bodies.size(); ++i){
        dvec2 acc(0.0);
        for(size_t j=0; j < bodies.size(); ++j){
            if (i==j) {continue;}
            dvec2 r = bodies[j].position - bodies[i].position;
            double r_2 = dot(r,r);
            double F;
            if (r_2==0){F = (G * bodies[j].mass) /1e-6;}
            else {F = (G * bodies[j].mass) / r_2;}
            acc += F * normalize(r);
        }
        accelerations[i] = acc;
    }

    for(size_t i=0; i < bodies.size(); ++i){
        bodies[i].velocity += accelerations[i] * static_cast<double>(dt);
        bodies[i].position += bodies[i].velocity * static_cast<double>(dt);
    }

}

vector<Body> inputBodies(){
    vector<Body> bodies;
    vector<float> yellow = {1.0f, 1.0f, 0.0f}, blue = {0.0f, 0.5f, 1.0f};
    //set the radii based on a ratio between them with a lower boundary 
    auto body1 = Body(0.0, 0.0, 0.0, 0.0, 1.989e30, 0.3, 100, yellow); //6.9634e8
    auto body2 = Body(1.496e11, 0.0, 0.0, 29780.0, 5.972e24, 0.1, 100, blue); //6.371e6
    
    bodies.emplace_back(body1);
    bodies.emplace_back(body2);

    return bodies;
}

int main() {

    auto UnitCircle = Body(0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 100);
    vector<Body> bodies = inputBodies();

    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(850, 650, "Gravitational_Potential", NULL, NULL);
    if(window == NULL)
    {
        cout << "Failed to create GLFW window" << endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (glewInit() != GLEW_OK) {
    cout << "Failed to initialize GLEW" << endl;
    return -1;
    };

    unsigned int VBO, VAO;
    glGenBuffers(1, &VBO);
    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, UnitCircle.vertices.size() * sizeof(float), UnitCircle.vertices.data(), GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    const char* vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "uniform vec2 aspect;\n"
    "uniform vec2 offset;\n"
    "uniform float radius;\n"
    "void main() {\n"
    "    vec2 scaled = aPos.xy * radius * aspect;\n"
    "    vec2 finalPos = scaled + offset;\n"
    "    gl_Position = vec4(finalPos, aPos.z, 1.0);\n"
    "}";


    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    const char* fragmentShaderSource = "#version 330 core\n"
    "out vec4 FragColor;\n"
    "uniform vec3 bodyColor;\n"
    "void main() {\n"
    "   FragColor = vec4(bodyColor, 1.0);\n"
    "}";

    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    while(!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(shaderProgram);

        //add fps counter, make dt adjustable mid-simulation
        

        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        float aspectRatio = float(width)/float(height);
        int aspectLocation = glGetUniformLocation(shaderProgram, "aspect");
        glUniform2f(aspectLocation, 1.0f / (float(width) / float(height)), 1.0f);

        glBindVertexArray(VAO);

        gravitas(bodies, dt);

        for (auto& body : bodies) {
            body.render(shaderProgram);
            glDrawArrays(GL_TRIANGLE_FAN, 0, body.vertices.size() / 3);
        }

        glfwPollEvents();
        glfwSwapBuffers(window);
    }

    glfwTerminate();
    return 0;
}
