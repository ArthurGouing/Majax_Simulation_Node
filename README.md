# Majax Simulation Node
### With GPU Computation

## Presentation and Objectives
The physics simulation of Blender is an old system that use strong algorithme. That why Blender simulation is still been used. But thoses algorithmes are not thinked to moderne computer architecture. Nowday, every computer have multiple core and GPU(s) to bring more computation power to the user, But current Blender physics, use sequential algorithmes, that uses only one core at a time, and can't use GPU at all.

Majax use an Python wrapper of OpenCL, to integrate GPU computation on Blender, easly, throught a simple add-on.
For now, Majax provide a nodal interface to design OpenCL algorithmes, so they can be written, previewed and used directly inside Blender. 

After somes basics algorithmes for physics simulation will be written, they could be integrated in build in nodes, to provide an user-friendly nodal physics system.

## Installation
To install Majax, you need to:
 - Have OpenCL driver on your Computer
 - Install PyOpenCL wrapper on the Blender's python
 - Install the Add-on files

### Install OpenCL
#### Window
On window, OpenCL driver should already been installed on your computer when GPU driver has been installed.
If OpenCL isn't installed on yout computor, fo check the official page of your GPU vendor:
 - NVIDIA: 
 - AMD: 
 - INTEL: 

#### Linux
On Linux, you had to install your GPU driver manually. If they are installed, you should already have OpenCL.
Other wise, fo to the official page of your GPU vendor to find out how to install OpenCL drivers:
 - NVIDIA: 
 - AMD: 
 - INTEL: 

#### Mac
If you have and Apple Sillicon processor (M1, M2, M3), it is possible that OpenCL don't work as Apple as depreciated support for OpenCL. 
Howerver, I find that some people managed to run OpenCL on M1, M2.
Let me know if it's working on Mac

### Install PyOpenCL
Majax need the (pyopencl)[] python package to use OpenCL trhought python, but Blender doesn't have installed this package by default. To install pyopencl on Blender, open Blender, then go in the console tab, and enter the following line:
```python
import pip
# Equivalent to `pip install pyopencl` in command line
pip.main(["install", "pyopencl"])
```
(pip.main(["install", "--upgrade", "pip"]) # To update pip)


cf OpenCL official website

### Install Majax
Like any other Blender add-on, you need to download Majax as a zip file, and then install them in Blender.
Open a Blender and open a setting tab. Go to add-on, cick on "Install" and select the Majax.zip file you download.

## Demo
