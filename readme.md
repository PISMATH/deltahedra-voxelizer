# 3D Voxelizer using Tetrahedral-Octahedral Honeycomb

This Python script voxelizes a given 3D STL model using a tetrahedral-octahedral honeycomb structure. It outputs a corresponding OpenSCAD (.scad) file, where the voxelized version of the model is represented using octahedrons and tetrahedrons.

## Features
- Loads a 3D model in STL format.
- Creates a voxelized representation using tetrahedral-octahedral tessellation.
- Outputs an OpenSCAD file with octahedrons and two differently oriented tetrahedrons.

## Prerequisites
Make sure you have the following dependencies installed. You can install them using the `requirements.txt` file provided.

```bash
pip install -r requirements.txt
