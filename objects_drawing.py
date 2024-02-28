from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Function to draw the fractal by dividing the tetrahedron
def draw_fractal(num_divisions, initial_tetrahedron, texture_ids):
    texture_coordinates = [
        [(0, 0), (1, 0), (1, 1)],  # Texture coordinates for Face 1
        [(0, 0), (1, 1), (0, 1)],  # Texture coordinates for Face 2
        [(0, 1), (1, 1), (0, 0)],  # Texture coordinates for Face 3
        [(0, 1), (1, 0), (1, 1)]   # Texture coordinates for Face 4
    ]
    divide_tetrahedron(*initial_tetrahedron, texture_coordinates, texture_ids, depth=num_divisions)

# Function to recursively divide the tetrahedron
def divide_tetrahedron(V1, V2, V3, V4, texture_coordinates, texture_ids, depth):
    # Check if recursion depth is greater than 0
    if depth > 0:
        # Calculate midpoints of the edges
        mid1 = [(V1[i] + V2[i]) / 2 for i in range(3)]
        mid2 = [(V1[i] + V3[i]) / 2 for i in range(3)]
        mid3 = [(V1[i] + V4[i]) / 2 for i in range(3)]
        mid4 = [(V2[i] + V3[i]) / 2 for i in range(3)]
        mid5 = [(V2[i] + V4[i]) / 2 for i in range(3)]
        mid6 = [(V3[i] + V4[i]) / 2 for i in range(3)]

        # Recursively divide each of the four smaller tetrahedra
        divide_tetrahedron(V1, mid1, mid2, mid3, texture_coordinates, texture_ids, depth - 1)
        divide_tetrahedron(mid1, V2, mid4, mid5, texture_coordinates, texture_ids, depth - 1)
        divide_tetrahedron(mid2, mid4, V3, mid6, texture_coordinates, texture_ids, depth - 1)
        divide_tetrahedron(mid3, mid5, mid6, V4, texture_coordinates, texture_ids, depth - 1)
    else:
        # If recursion depth is 0, draw the tetrahedron
        draw_tetrahedron(V1, V2, V3, V4, texture_coordinates, texture_ids)

# Function to draw a tetrahedron
def draw_tetrahedron(V1, V2, V3, V4, texture_coordinates_faces, texture_ids):
    # Define the direction of triangles considered as front-facing
    glFrontFace(GL_CCW)

    # Bind the second texture for the tetrahedron
    glBindTexture(GL_TEXTURE_2D, texture_ids[1])
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glBegin(GL_TRIANGLES)

    # Face 1
    normal = np.cross(np.subtract(V2, V1), np.subtract(V3, V1))
    normal = normal / np.linalg.norm(normal)
    glColor3f(1, 0, 0)
    glTexCoord2fv(texture_coordinates_faces[0][0])
    glVertex3fv(V1)
    glColor3f(0, 1, 0)
    glTexCoord2fv(texture_coordinates_faces[0][1])
    glVertex3fv(V2)
    glColor3f(0, 0, 1)
    glTexCoord2fv(texture_coordinates_faces[0][2])
    glVertex3fv(V3)

    # Face 2
    normal = np.cross(np.subtract(V3, V1), np.subtract(V4, V1))
    normal = normal / np.linalg.norm(normal)
    glColor3f(1, 0, 1)
    glTexCoord2fv(texture_coordinates_faces[1][0])
    glVertex3fv(V1)
    glColor3f(0, 1, 1)
    glTexCoord2fv(texture_coordinates_faces[1][1])
    glVertex3fv(V3)
    glColor3f(1, 1, 0)
    glTexCoord2fv(texture_coordinates_faces[1][2])
    glVertex3fv(V4)

    # Face 3
    normal = np.cross(np.subtract(V2, V3), np.subtract(V4, V3))
    normal = normal / np.linalg.norm(normal)
    glColor3f(0, 1, 1)
    glTexCoord2fv(texture_coordinates_faces[2][0])
    glVertex3fv(V2)
    glColor3f(1, 1, 0)
    glTexCoord2fv(texture_coordinates_faces[2][1])
    glVertex3fv(V3)
    glColor3f(1, 0, 1)
    glTexCoord2fv(texture_coordinates_faces[2][2])
    glVertex3fv(V4)

    # Face 4
    normal = np.cross(np.subtract(V2, V1), np.subtract(V4, V1))
    normal = normal / np.linalg.norm(normal)
    glColor3f(0, 0, 1)
    glTexCoord2fv(texture_coordinates_faces[3][0])
    glVertex3fv(V1)
    glColor3f(1, 0, 0)
    glTexCoord2fv(texture_coordinates_faces[3][1])
    glVertex3fv(V2)
    glColor3f(0, 1, 0)
    glTexCoord2fv(texture_coordinates_faces[3][2])
    glVertex3fv(V4)

    # End drawing triangles
    glEnd()

# Function to draw a triangle
def draw_triangle(A, B, C):
    glBegin(GL_TRIANGLES)
    glVertex3fv(A)
    glVertex3fv(B)
    glVertex3fv(C)
    glEnd()

# Function to draw the base with textures
def draw_base(texture_ids):
    # Use the first texture for the floor
    glBindTexture(GL_TEXTURE_2D, texture_ids[0])

    # Enable blending for transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Begin drawing quads for the floor
    glBegin(GL_QUADS)
    
    # Loop through grid points on the floor
    for i in np.arange(-10, 10, 1.0):
        for j in np.arange(-10, 10, 1.0):
            # Set color and texture coordinates for the current vertex
            glColor4ub(255, 255, 255, 255)
            glTexCoord2f(0, 0)
            glVertex3fv(np.array([i, -0.5, j]))

            glTexCoord2f(1, 0)
            glVertex3fv(np.array([i + 1.0, -0.5, j]))

            glTexCoord2f(1, 1)
            glVertex3fv(np.array([i + 1.0, -0.5, j + 1.0]))

            glTexCoord2f(0, 1)
            glVertex3fv(np.array([i, -0.5, j + 1.0]))

    # End drawing quads
    glEnd()

    # Disable blending after drawing
    glDisable(GL_BLEND)

# Function to draw axes
def draw_axes():
    # Begin drawing lines for axes
    glBegin(GL_LINES)

    # X-axis (red)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.0, 0.0, 0.0]))
    glVertex3fv(np.array([10.0, 0.0, 0.0]))

    # Y-axis (green)
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.0, 0.0, 0.0]))
    glVertex3fv(np.array([0.0, 10.0, 0.0]))

    # Z-axis (blue)
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.0, 0.0, 0.0]))
    glVertex3fv(np.array([0.0, 0.0, 10.0]))

    # End drawing lines
    glEnd()

# Function to draw a crosshair
def draw_crosshair(display):
    crosshair_size = 12
    crosshair_color = (255, 255, 0)  

    # Set 2D drawing mode
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, display[0], display[1], 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw the crosshair
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3ub(*crosshair_color)
    glVertex2i(display[0] // 2 - crosshair_size, display[1] // 2)
    glVertex2i(display[0] // 2 + crosshair_size, display[1] // 2)
    glVertex2i(display[0] // 2, display[1] // 2 - crosshair_size)
    glVertex2i(display[0] // 2, display[1] // 2 + crosshair_size)
    glEnd()

    # Restore 3D drawing mode
    glLineWidth(1)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

# Function to draw a light source
def draw_light_source(position):
    # Translate to the coordinates of the light source
    glTranslate(-position[0], -position[1], -position[2])

    # Set the light color to white
    glColor3f(1.0, 1.0, 1.0)

    # Define the radius and number of steps for latitude and longitude
    radius = 0.25
    latitude_steps = 10
    longitude_steps = 10

    # Loop for latitude steps
    for i in range(latitude_steps + 1):
        lat = math.pi * (-0.5 + float(i) / float(latitude_steps))
        cos_lat = math.cos(lat)
        sin_lat = math.sin(lat)

        # Begin drawing lines
        glBegin(GL_LINES)

        # Loop for longitude steps
        for j in range(longitude_steps + 1):
            lon = 2.0 * math.pi * float(j) / float(longitude_steps)
            x = radius * math.cos(lon) * cos_lat
            y = radius * math.sin(lon) * cos_lat
            z = radius * sin_lat

            # Add vertex to the current line
            glVertex3f(x, y, z)

            # Calculations for the next point on the same line
            lon_next = 2.0 * math.pi * float(j + 1) / float(longitude_steps)
            x_next = radius * math.cos(lon_next) * cos_lat
            y_next = radius * math.sin(lon_next) * cos_lat
            z_next = radius * sin_lat

            # Add vertex to the next line
            glVertex3f(x_next, y_next, z_next)

        # End drawing lines
        glEnd()

    # Restore translation to the original position
    glTranslate(position[0], position[1], position[2])

