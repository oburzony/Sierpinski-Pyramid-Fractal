import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Function to move the camera based on user input
def move_camera(rot_a, rot_b, viewMatrix, zoom, control_zoom):
    # Reset the current matrix and replace it with the identity matrix
    glLoadIdentity()
    glPushMatrix()
    glLoadIdentity()

    keys = pygame.key.get_pressed()

    # Rotation controls
    if keys[pygame.K_UP]:
        # Adjust pitch (rotation around the x-axis)
        if rot_a < 0:
            rot_a = 0
        rot_a -= 1
        glRotatef(rot_a, 1.0, 0.0, 0.0)
    if keys[pygame.K_DOWN]:
        # Adjust pitch (rotation around the x-axis)
        if rot_a > 0:
            rot_a = 0
        rot_a += 1
        glRotatef(rot_a, 1.0, 0.0, 0.0)
    if keys[pygame.K_LEFT]:
        # Adjust yaw (rotation around the y-axis)
        if rot_b < 0:
            rot_b = 0
        rot_b -= 1
        glRotatef(rot_b, 0.0, 1.0, 0.0)
    if keys[pygame.K_RIGHT]:
        # Adjust yaw (rotation around the y-axis)
        if rot_b > 0:
            rot_b = 0
        rot_b += 1
        glRotatef(rot_b, 0.0, 1.0, 0.0)

    # Translation controls
    if keys[pygame.K_w]:
        # Move forward
        glTranslatef(0, 0, 0.1)
    if keys[pygame.K_s]:
        # Move backward
        glTranslatef(0, 0, -0.1)
    if keys[pygame.K_d]:
        # Move right
        glTranslatef(-0.1, 0, 0)
    if keys[pygame.K_a]:
        # Move left
        glTranslatef(0.1, 0, 0)
    if keys[pygame.K_LSHIFT]:
        # Move up
        glTranslatef(0, 0.1, 0)
    if keys[pygame.K_SPACE]:
        # Move down
        glTranslatef(0, -0.1, 0)

    # Zoom control
    if control_zoom != zoom:
        # Adjust zoom
        glTranslatef(0, 0, zoom - control_zoom)
        control_zoom = zoom

    # Apply rotation and translation to the view matrix
    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    # Restore the original matrix
    glPopMatrix()

    # Apply the updated view matrix
    glMultMatrixf(viewMatrix)

    return rot_a, rot_b, viewMatrix, control_zoom
