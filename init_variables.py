from pygame.locals import *
from OpenGL.GL import *
import time
import math

# Function to initialize fractal settings
def initialize_fractal_settings():
    fractal_levels = int(input("Enter the number of fractal levels: "))

    # Define the vertices of the initial tetrahedron
    initial_tetrahedron = [
        (-1, -0.5, -2 * (1 / 3) * math.sqrt(3) / 2),
        (1, -0.5, -2 * (1 / 3) * math.sqrt(3) / 2),
        (0, -0.5, 2 * (math.sqrt(3) / 2 - (1 / 3) * math.sqrt(3) / 2)),
        (0, 2 * (math.sqrt((math.sqrt(3) / 2) ** 2 - ((1 / 3) * math.sqrt(3) / 2) ** 2)) - 0.5,
        2 * ((1 / 3) * math.sqrt(3) / 2 - (1 / 3) * math.sqrt(3) / 2))
    ]

    return fractal_levels, initial_tetrahedron

# Function to initialize textures
def initialize_textures():
    last_texture_toggle_time = time.time()
    texture_ids = []

    # Specify texture images
    texture_images = [
        "img_1.png",
        "img_2.png"
    ]
    return texture_images, texture_ids, last_texture_toggle_time

# Function to initialize renderer state
def initialize_renderer_state():
    enable_textures = False
    is_rotating_fractal = False
    rotate_fractal = False
    reset_fractal = False
    enable_lighting = False
    rota = 0
    rotb = 0
    zoom = 0
    scale = 1
    control_zoom = 0
    angle = 0
    return enable_textures, is_rotating_fractal, rotate_fractal, \
           reset_fractal, rota, rotb, zoom, scale, control_zoom, \
           enable_lighting, angle

# Function to initialize light components
def initialize_light_components():
    light_ambient = [0.1, 0.1, 0.0, 1.0]
    light_diffuse = [0.8, 0.8, 0.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    return light_ambient, light_diffuse, light_specular

# Function to initialize material components
def initialize_material_components():
    mat_ambient = [1.0, 1.0, 1.0, 1.0]
    mat_diffuse = [1.0, 1.0, 1.0, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = 20.0
    return mat_ambient, mat_diffuse, mat_specular, mat_shininess

# Function to initialize light position
def initialize_light_position():
    light_position_0 = [0.0, 0.0, 5.0, 1.0]
    light_position_1 = [0.0, 0.0, 5.0, 0.0]

    return light_position_0, light_position_1

# Function to initialize light attenuation
def initialize_light_attenuation():
    att_constant = 1.0
    att_linear = 0.5
    att_quadratic = 0.001
    return att_constant, att_linear, att_quadratic
