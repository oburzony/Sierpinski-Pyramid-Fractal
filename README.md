# Sierpinski Pyramid

## Description
The Sierpinski Pyramid project is the implementation of a graphical program that creates an animated, interactive, three-dimensional Sierpinski pyramid. The program was created in Python using libraries such as Pygame, PyOpenGL, PIL (Pillow), and numpy.

<img width="1280" alt="image" src="Read-image\image-program.png">

## Requirements
To run the program, you need to install the required libraries:
- pygame
- PyOpenGL
- Pillow
- numpy

You can do this using the following command:
```bash
pip install pygame PyOpenGL Pillow numpy
```
Additionally, the program uses standard Python modules such as math, os, and time.
Make sure you have Python installed in version 3.x. If not, you can download it from the official Python website.

## Running
**Installing libraries and downloading the repository:**
1. Install the required libraries necessary for the program to run.
2. Download the repository with the source code of the program and unzip it.

**Opening a terminal or command prompt:**
1. Open a terminal or command prompt on your computer.

**Navigating to the project directory:**
1. Use the `cd` command in the terminal to navigate to the project directory where the `main.py` file is located. For example:
   ```bash
   cd path/to/your/project
   ```

**Running the program:**
1. Run the program using the following command:
   ```bash
   python3 main.py 
   ```

**Entering the number of pyramid levels:**
- After starting the program, you will be prompted to enter the number of pyramid levels (N). Enter the appropriate number and press Enter.

## Features
- **Pyramid with N levels:** The application allows generating a pyramid with a defined number of levels, adapted to the user's needs.
- **Rotating pyramid:** The ability to rotate the pyramid around its axis, allowing for various perspectives.
- **Pyramid standing on a base:** Stable placement of the pyramid on a virtual base, giving it a realistic appearance.
- **Turning on and off light sources:** Control over lighting by activating and deactivating directional and point light sources.
- **Changing light source parameters:** The ability to adjust the intensity, direction, and color of light, allowing for the creation of different visual effects.
- **Moving in space using the keyboard:** Controlling camera movement using keyboard keys, allowing for free movement around the scene.
- **Zooming with the scroll wheel:** Functionality for zooming in and out of the view using the mouse scroll wheel.
- **Scaling the pyramid:** The ability to change the size of the pyramid, adjusting it to the user's individual preferences.
- **Turning textures on and off:** Control over the use of textures on the surface of the pyramid, affecting its appearance.
- **Day and night simulation using spheres:** Option to simulate changes in lighting over time using spheres representing day and night.

## Controls:
- "w" - move camera forward
- "s" - move camera backward
- "a" - move camera left
- "d" - move camera right
- "UP" - move camera up
- "DOWN" - move camera down
- "LEFT" - move camera left
- "RIGHT" - move camera right
- "SCROLL" - zoom in/out
- "r" - reset camera position, light, and zoom
- "o" - turn on/off pyramid rotation
- "p" - reset pyramid to initial position
- "t" - turn on/off textures
- "F1" - increase pyramid scale
- "F2" - decrease pyramid scale
- "x" - turn on/off scene lighting (must be turned on to demonstrate lighting)
- "k" - turn on/off directional light (lighting in scene "x" must be turned on)
- "l" - turn on/off point light (lighting in scene "x" must be turned on)
- "LEFT_MOUSE_BUTTON" - turn on/off day and night simulation (lighting in scene "x" must be turned on)
- "1" - move light position towards positive Y
- "2" - move light position towards negative Y
- "3" - move light position towards positive Z
- "4" - move light position towards negative Z
- "5" - move light position towards positive X
- "6" - move light position towards negative X
- "7" - increase constant light attenuation
- "8" - decrease constant light attenuation
- "9" - increase linear light attenuation
- "0" - decrease linear light attenuation
- "-" - increase quadratic light attenuation
- "=" - decrease quadratic light attenuation
- "F3" - increase red light component
- "F4" - decrease red light component
- "F5" - increase green light component
- "F6" - decrease green light component
- "F7" - increase blue light component
- "F8" - decrease blue light component
