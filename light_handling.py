import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import objects_drawing as od

# Function to add a light source with specified parameters
def add_light_source(name, position, ambient, diffuse, specular, constant_attenuation, linear_attenuation, quadratic_attenuation):
    glLightfv(name, GL_AMBIENT, ambient)
    glLightfv(name, GL_DIFFUSE, diffuse)
    glLightfv(name, GL_SPECULAR, specular)
    glLightfv(name, GL_POSITION, position)
    glLightf(name, GL_CONSTANT_ATTENUATION, constant_attenuation)
    glLightf(name, GL_LINEAR_ATTENUATION, linear_attenuation)
    glLightf(name, GL_QUADRATIC_ATTENUATION, quadratic_attenuation)
    glEnable(GL_LIGHTING)  

# Function to modify the position of two light sources based on user input
def modify_light_position(key, light_position_0, light_position_1):
    # Define the step size for changing light position
    light_position_step = 1.0

    # Check if the key corresponds to moving the lights up or down
    if key in [pygame.K_1, pygame.K_2]:
        direction = 1 if key == pygame.K_1 else -1
        light_position_0[1] += direction * light_position_step
        light_position_1[1] += direction * light_position_step
    # Check if the key corresponds to moving the lights forward or backward
    elif key in [pygame.K_3, pygame.K_4]:
        direction = 1 if key == pygame.K_3 else -1
        light_position_0[2] += direction * light_position_step
        light_position_1[2] += direction * light_position_step
    # Check if the key corresponds to moving the lights left or right
    elif key in [pygame.K_5, pygame.K_6]:
        direction = 1 if key == pygame.K_5 else -1
        light_position_0[0] += direction * light_position_step
        light_position_1[0] += direction * light_position_step

    # Print the updated positions for point light and directional light
    print("Point light:", light_position_0)
    print("Directional light:", light_position_1)

    return light_position_0, light_position_1

# Function to modify light attenuation based on user input
def modify_light_attenuation(key, att_constant, att_linear, att_quadratic):
    # Define the step size for changing light attenuation
    light_attenuation_step = 0.1

    # Check if the key corresponds to increasing constant, linear, or quadratic attenuation
    if key in [pygame.K_7, pygame.K_9, pygame.K_MINUS]:
        if key == pygame.K_7:
            att_constant += light_attenuation_step
        elif key == pygame.K_9:
            att_linear += light_attenuation_step
        elif key == pygame.K_MINUS:
            att_quadratic += light_attenuation_step
    # Check if the key corresponds to decreasing constant, linear, or quadratic attenuation
    elif key in [pygame.K_8, pygame.K_0, pygame.K_EQUALS]:
        if key == pygame.K_8 and att_constant >= light_attenuation_step:
            att_constant -= light_attenuation_step
        elif key == pygame.K_0 and att_linear >= light_attenuation_step:
            att_linear -= light_attenuation_step
        elif key == pygame.K_EQUALS and att_quadratic >= light_attenuation_step:
            att_quadratic -= light_attenuation_step
        else:
            print("Operation not possible")

    # Adjust the precision of the attenuation values
    precision = 10  # Adjust the precision as needed
    att_constant = round(att_constant, precision)
    att_linear = round(att_linear, precision)
    att_quadratic = round(att_quadratic, precision)

    # Print information about the changed attenuation values
    print("\nConstant attenuation:", att_constant)
    print("Linear attenuation:", att_linear)
    print("Quadratic attenuation:", att_quadratic)

    return att_constant, att_linear, att_quadratic

# Function to modify light color based on user input
def modify_light_color(key, light_ambient, light_diffuse, light_specular):
    # Define the step size for changing light color
    light_color_step = 0.1
    
    # Map keys to color components (ambient, diffuse, specular) and direction of change
    color_indices = {
        pygame.K_F3: 0, pygame.K_F4: 0,
        pygame.K_F5: 1, pygame.K_F6: 1,
        pygame.K_F7: 2, pygame.K_F8: 2
    }

    # Determine the direction of change based on the key pressed
    direction = 1 if key in [pygame.K_F3, pygame.K_F5, pygame.K_F7] else -1

    # Check if the key corresponds to a valid color component
    if key in color_indices:
        index = color_indices[key]

        # Update the specified color component with the defined step and constrain it between 0.0 and 1.0
        light_ambient[index] = max(min(light_ambient[index] + direction * light_color_step, 1.0), 0.0)
        light_diffuse[index] = max(min(light_diffuse[index] + direction * light_color_step, 1.0), 0.0)
        light_specular[index] = max(min(light_specular[index] + direction * light_color_step, 1.0), 0.0)

        # Adjust the precision of the color components
        precision = 10  # Adjust the precision as needed
        light_ambient[index] = round(light_ambient[index], precision)
        light_diffuse[index] = round(light_diffuse[index], precision)
        light_specular[index] = round(light_specular[index], precision)

        # Print information about the changed color component
        print("\nChanging", ["red", "green", "blue"][index], "component:")
    
    # Print the updated values for ambient, diffuse, and specular components
    print("Ambient", light_ambient)
    print("Diffuse", light_diffuse)
    print("Specular", light_specular)

    return light_ambient, light_diffuse, light_specular

# Function for day-night cycle animation
def day_night_cycle_animation(angle):
    # Calculate positions for the sun and moon based on the angle of the animation
    sun_position = [1.5 * math.cos(math.radians(angle)), 0.5, 1.5 * math.sin(math.radians(angle)), 1.0]
    moon_position = [1.5 * math.cos(math.radians(angle + 180)), 0.5, 1.5 * math.sin(math.radians(angle + 180)), 1.0]

    # Define colors for sun and moon lights
    sun_ambient = sun_diffuse = sun_specular = [1.0, 1.0, 0.0, 1.0]
    moon_ambient = moon_diffuse = moon_specular = [1.0, 0.0, 1.0, 1.0]

    # Define attenuation parameters for light sources
    attenuation_constant = 0.01
    attenuation_linear = 0.001
    attenuation_quadratic = 1

    # Add light sources for the sun and moon
    add_light_source(GL_LIGHT2, sun_position, sun_ambient, sun_diffuse, sun_specular, attenuation_constant, attenuation_linear, attenuation_quadratic)
    add_light_source(GL_LIGHT3, moon_position, moon_ambient, moon_diffuse, moon_specular, attenuation_constant, attenuation_linear, attenuation_quadratic)

    # Define positions for the sun and moon spheres
    sphere_sun_position = [1.5 * math.cos(math.radians(angle)), -0.5, 1.5 * math.sin(math.radians(angle))]
    sphere_moon_position = [1.5 * math.cos(math.radians(angle + 180)), -0.5, 1.5 * math.sin(math.radians(angle + 180))]

    # Draw the sun and moon spheres if the respective lights are enabled
    if glIsEnabled(GL_LIGHT2) and glIsEnabled(GL_LIGHT3):
        od.draw_light_source(sphere_sun_position)
        od.draw_light_source(sphere_moon_position)

    # Increment the angle for the next frame of the animation
    angle = (angle + 5) % 360

    return angle
