# Stage_MeshMedicali

## Table of Contents
- [General Description](#general-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Tutorial](#tutorial)
- [Other Info](#other-info)


## General Description
> **What the Pipeline do** 
- Processing an .off file with a mesh in it ,
- Creating a .blend file through the Blender API bpy
- Rendering an image from Python script


> **Time Execution:**

- remove_zero_area_faces : about 3.97 sec

- removing not connected components : about 2.79 sec

- scaling : about 0.23 sec

- repair_mesh : about 4.62 sec

## Installation

To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

## Configuration
The configuration file (`config.json`) should follow the sample below:

```json
{
    "dataname": "000199_tumoredbrain",
    "logfile_name_processing": "logTprocessing",
    "logfile_name_blender": "logTBlender",
    "value_eps": 1.02,
    "value_minsamples": 5,
    "value_decimation": 140000,
    "value_scalefactor":  1,
    "value_scalingtype": 0,
    "name_off_file": "processed",
    "processing_0": true,
    "processing_1": false,
    "blend_file_ex": false,
    "render_file_ex": false,
    "blend_file_name": "testBlend_",
    "render_file_name": "testION_",
    "blender_path_execute": "Full path of Blender in your system"
}
```
- `dataname`: **String-value.** File's name the program is going to work on. The User does not have to change the name every single time, **'name_off_file'** comes to help.
- `logfile_name_processing`: **String-value.** File txt's name where the description of the operation will be saved. ***[Processing Operation Only]***
- `logfile_name_blender`: **String-value.** File txt's name where the description of the operation will be saved. ***[Blender Operation Only]***
- `value_eps`: **Float-value.** Value to detect the distance between point. Points inside this are called 'cluster'. ***[Processing Operation Only]***
- `value_minsamples`: **Integer-value.** Value to define the min numbers of points inside a cluster. ***[Processing Operation Only]***
- `value_decimation`: **Integer-value.** Value used to decimanted the mesh. ***[Processing Operation Only]***
- `value_scalefactor`: **Float-value.** Value used to scale a mesh. ***[Processing Operation Only]***
- `value_scalingtype`: **Integer-value.** Value to choose what scaling type apply on the mesh. [**Type 0**: scaling on X, Y and Z. **Type 1**: scaling to UNIT-BOX. **Type 2**: scaling to UNIT-SPHERE] ***[Processing Operation Only]***
- `name_off_file`: **String-value.** String value added as a prefix on the file Generated during the pipeline's ***Phase 0*** and ***Phase 1***.
- `processing_0`: **Boolean-value.** Define the ***Phase 0*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `processing_1`: **Boolean-value.** Define the ***Phase 1*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `blend_file_ex`: **Boolean-value.** Define the ***Phase 2*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `render_file_ex`: **Boolean-value.** Define the ***Phase 3*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `blend_file_name`: **String-value.** String name to define the blend file.
- `render_file_name`: **String-value.** String name to define the rendering image name.
- `blender_path_execute`: **String-value.** String path of Blender program.



# Tutorial
**mainPipelineT.py:** is the main and the only file you sould focus on
> Fill in the json configuration file first and run the main file

### Pipeline operation
**Phase 0:** processing the mesh
> - Remove Zero Area Faces
> - Remove Not Connected Components

- **Before starting the next operation, add the file generated in the *OUTPUT_SOURCE* to the *INPUT_SOURCE* folder**

**Phase 1:** processing the mesh
> - Repair Mesh
> - Scaling Mesh

- **For the last time, before starting the next operation, add the file generated in the *OUTPUT_SOURCE* to the *INPUT_SOURCE* folder**

**Phase 2:** set up the .blend file
> What I suggest is:
> - Try to run it, AS IS, open the **outFinal.blend** and check on it
> - Make the changes you in the blend file and reported to the CODE too
> - Delete the previous blend files created
> - Re-run the CODE again, and check it

**Phase 3:** rendering an image file
> - Before run the code for the last operation, copy and paste the **PATH** of the blender execution file in the json config file: ***blender_path_execute*** variable
> - Now you run it
> - The output file is in ***IMAGE_RENDERED*** folder



## Other Info
**Python Version:**
>3.11

**Environment:**
> I suggest on using a virtual enviroment or just a simple IDE with a virtual environment as a set-up
