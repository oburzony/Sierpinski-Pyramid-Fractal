import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import objects_drawing as od
import init_variables as iv
import textures_handling as th
import move_handling as mh
import light_handling as lh

# Function to configure the OpenGL environment
def configure_environment():
    # Initialize fractal settings and initial tetrahedron
    (fractal_levels, initial_tetrahedron) = iv.initialize_fractal_settings()
    # Initialize textures 
    (texture_images, texture_ids, last_texture_toggle_time) =  iv.initialize_textures()

    pygame.init()
    display = (1600, 900)
    scr = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Load textures
    for filename in texture_images:
        texture_ids.append(th.load_texture(filename))

    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    # Set up the modelview matrix and look at the origin
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0 ,0, 5, 0, 0, 0, 0, 1, 0)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    # Center the mouse and set cursor to hand
    displayCenter = [scr.get_size()[i] // 2 for i in range(2)]
    pygame.mouse.set_pos(displayCenter)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    # Enable color material and set material properties
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    return fractal_levels, initial_tetrahedron, viewMatrix, last_texture_toggle_time, texture_ids, display

# Function to scale the fractal based on user input
def scaling_fractal(key, scale):
    if key == pygame.K_F1:
        if scale < 5.0:
            scale += 0.25
    elif key == pygame.K_F2:
        if scale > 0.25:
            scale -= 0.2
    return scale

# Function to handle zooming based on mouse wheel input
def zoom_handling(button, zoom):
    if button == 4:
        if zoom < 4:
            zoom += 0.5
    if button == 5:
        if zoom > -4:
            zoom -= 0.5
    return zoom

# Function to reset the view and light settings
def reset_view_and_light(): 
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    (light_ambient, light_diffuse, light_specular) = iv.initialize_light_components()
    (light_position_0, light_position_1) = iv.initialize_light_position()
    (att_constant, att_linear, att_quadratic) = iv.initialize_light_attenuation()
    rot_a, rot_b = 0, 0 
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    return (light_ambient, light_diffuse, light_specular, light_position_0,
            light_position_1, att_constant, att_linear, att_quadratic, rot_a,
            rot_b, viewMatrix )

# Function to disable light
def light_disable():
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHT3)
    glDisable(GL_LIGHTING)

# Function to set material properties for ambient, diffuse, specular, and shininess
def set_material_behavior(material_ambient, material_diffuse, material_specular, material_shininess):
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)

def main():
    
    (num_divisions, initial_tetrahedron, viewMatrix, 
     last_texture_toggle_time, texture_ids, display) = configure_environment()

    (enable_textures, is_rotating_fractal, rotate_fractal, 
     reset_fractal_rotation, rot_a, rot_b, zoom, scale, control_zoom, 
     enable_lighting, angle) = iv.initialize_renderer_state()
    
    (light_ambient,light_diffuse,light_specular) = iv.initialize_light_components()
    (light_position_0, light_position_1) = iv.initialize_light_position()
    (mat_ambient,mat_diffuse,mat_specular,mat_shininess) = iv.initialize_material_components()
    (att_constant, att_linear, att_quadratic) = iv.initialize_light_attenuation()

    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # Handle mouse events for zooming and day/night simulation     
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if event.button in [4, 5]:
                    zoom = zoom_handling(event.button,zoom)

                if event.button == 1:
                    if glIsEnabled(GL_LIGHT3):
                        glDisable(GL_LIGHT2)
                        glDisable(GL_LIGHT3)
                    else:
                        glEnable(GL_LIGHT2)
                        glEnable(GL_LIGHT3)

            if event.type == pygame.KEYDOWN:
                # Handle various key events
                if event.key == pygame.K_t:
                    # Toggle textures
                    (enable_textures,
                    last_texture_toggle_time) = th.toggle_textures(last_texture_toggle_time, enable_textures)
                                
                if event.key == pygame.K_ESCAPE:
                    # Quit application on ESC key
                    pygame.quit()
                    quit() 
                
                if event.key == pygame.K_RETURN:
                    # Toggle fullscreen mode on RETURN key
                    pygame.display.toggle_fullscreen()

                if event.key == pygame.K_BACKSPACE:
                    # Iconify the window on BACKSPACE key
                    pygame.display.iconify()

                if event.key == pygame.K_r:
                    # Reset view and lighting parameters on 'r' key
                    (light_ambient, light_diffuse, light_specular, light_position_0,
                    light_position_1, att_constant, att_linear, att_quadratic, rot_a, rot_b, viewMatrix) = reset_view_and_light()

                if event.key == pygame.K_o:
                    # Toggle fractal rotation
                    is_rotating_fractal = not is_rotating_fractal 
                
                if event.key == pygame.K_p:
                    # Toggle ractal rotation reset
                    reset_fractal_rotation = not reset_fractal_rotation

                if event.key == pygame.K_x:
                    # Toggle lighting
                    enable_lighting = not enable_lighting

                if event.key in [pygame.K_F1, pygame.K_F2]:
                    # Scale the fractal on function key press
                    scale = scaling_fractal(event.key, scale)
                
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    # Modify light positions based on numeric keys
                    (light_position_0, light_position_1) = lh.modify_light_position(event.key, light_position_0, light_position_1)

                if event.key in [pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS]:
                    # Modify light attenuation based on numeric and symbol keys
                    (att_constant, att_linear, att_quadratic) = lh.modify_light_attenuation(event.key, att_constant, att_linear, att_quadratic)

                if event.key in [pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8]:
                    # Modify light color based on function keys
                    (light_ambient, light_diffuse, light_specular) = lh.modify_light_color(event.key, light_ambient, light_diffuse, light_specular)

                if event.key == pygame.K_l:
                    # Toggle GL_LIGHT0 (spot)
                    if glIsEnabled(GL_LIGHT0):
                        glDisable(GL_LIGHT0)
                    else:
                        glEnable(GL_LIGHT0)

                if event.key == pygame.K_k:
                    # Toggle GL_LIGHT1 (directional)
                    if glIsEnabled(GL_LIGHT1):
                        glDisable(GL_LIGHT1)
                    else:
                        glEnable(GL_LIGHT1)
        
        # Update camera position based on user interaction
        rot_a, rot_b, viewMatrix, control_zoom = mh.move_camera(rot_a, rot_b, viewMatrix, zoom, control_zoom)

        # OpenGL rendering logic
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        
        set_material_behavior(mat_ambient,mat_diffuse,mat_specular,mat_shininess)
        od.draw_base(texture_ids)
        od.draw_axes()

        glPushMatrix()
        glScalef(scale, scale, scale)
        if is_rotating_fractal:
            rotate_fractal +=1
            glRotatef(rotate_fractal,0,-1,0)
            od.draw_fractal(num_divisions,initial_tetrahedron,texture_ids)
        else:
            rotate_fractal = rotate_fractal
            glRotatef(rotate_fractal,0,-1,0)
            od.draw_fractal(num_divisions,initial_tetrahedron,texture_ids)

        if reset_fractal_rotation:
            rotate_fractal = 0 
            od.draw_fractal(num_divisions,initial_tetrahedron,texture_ids)
            reset_fractal_rotation = not reset_fractal_rotation

        if enable_lighting:
            lh.add_light_source(GL_LIGHT0, light_position_0, light_ambient,light_diffuse,light_specular, att_constant,att_linear,att_quadratic)
            lh.add_light_source(GL_LIGHT1, light_position_1, light_ambient,light_diffuse,light_specular, att_constant,att_linear,att_quadratic)
            (angle) = lh.day_night_cycle_animation(angle)   
        else:
            light_disable()

        glPopMatrix()

        od.draw_crosshair(display)
        glDisable(GL_DEPTH_TEST)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
