from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np 
import time
import os


# Function to load a texture from an image file
def load_texture(filename):
   
    current_path = os.getcwd()
    folder = "textures"
    image_path = os.path.join(current_path, folder ,filename)

    # Open the image file and convert it to a NumPy array
    image = Image.open(image_path)
    texture_data = np.array(list(image.getdata()), dtype=np.uint8)

    # Generate and bind a texture ID
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters and upload the texture data to the GPU
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

# Function to toggle textures on and off
def toggle_textures(last_texture_toggle_time, enable_textures):
    # Check if enough time has passed since the last texture toggle
    if time.time() - last_texture_toggle_time > 0.1: 
        # Toggle the texture state (enable/disable) and update the toggle time
        if not enable_textures: 
            glEnable(GL_TEXTURE_2D) 
        else:
            glDisable(GL_TEXTURE_2D)     
        enable_textures = not enable_textures
        last_texture_toggle_time = time.time()
    
    return enable_textures, last_texture_toggle_time
