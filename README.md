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
    "file_path_choosen": "sceltaUserRiunione.txt",
    "dir_name_scelta": "\\log_sceltaUtente\\",
    "value_eps": 1.02,
    "value_minsamples": 5,
    "value_decimation": 140000,
    "value_scalefactor":  1,
    "value_scalingtype": 0,
    "name_off_file": "processed", 
    "input_user": "",
    "processing": true,
    "blender_ex": true,
    "rendering": true,
    "test_name":"TEST_GILON"
}
```
- `dataname`: file's name the programm is gonna work on. The User does not have to change the name every single time, 'file_path_choosen' comes to help 
- `logfile_name_processing`: file txt's name where the description of the operation will be saved ***[Processing Operation Only]***
- `logfile_name_blender`: file txt's name where the description of the operation will be saved ***[Blender Operation Only]***
- `file_path_choosen`: file txt's name where the pipeline operation will be saved. Used by the programm to detect which operation of the pipeline is currently on + the prefix of the off file generated during the pipeline's Operation 0
- `dir_name_scelta`: directory's name of [file_path_choosen]
- `value_eps`: value to detect the distance between point. Points inside this are called 'cluster' ***[Processing Operation Only]***
- `value_minsamples`: value to define the min numbers of points inside a cluster ***[Processing Operation Only]***
- `value_decimation`: value used to decimanted the mesh ***[Processing Operation Only]***
- `value_scalefactor`: value used to scale a mesh ***[Processing Operation Only]***
- `value_scalingtype`: value to choose what scaling type apply on the mesh [**Type 0**: scaling on X, Y and Z. **Type 1**: scaling to UNIT-BOX. **Type 2**: scaling to UNIT-SPHERE] ***[Processing Operation Only]***
- `name_off_file`: string value added as a prefix on the file Generated during the pipeline's **OPERATION 0** and **OPERATION 1**
- `pipeline_operation`: range value from 0 to 3 represents the [Pipeline Operation](#pipeline-operation)
- `test_name`: string name to define the rendering image



# Tutorial
**mainPipelineT.py:** is the main and the only file you sould focus on
> Fill in the json configuration file first and run the main file

### Pipeline operation
**Operation 0:** processing the mesh
> - Remove Zero Area Faces
> - Remove Not Connected Components

- **Before starting the next operation, add the file generated in the *OUTPUT_SOURCE* to the *INPUT_SOURCE* folder**

**Operation 1:** processing the mesh
> - Repair Mesh
> - Scaling Mesh

- **For the last time, before starting the next operation, add the file generated in the *OUTPUT_SOURCE* to the *INPUT_SOURCE* folder**

**Operation 2:** set up the .blend file
> What I suggest is:
> - Try to run it, AS IS, open the **outFinal.blend** and check on it
> - Make the changes you in the blend file and reported to the CODE too
> - Delete the previous blend files created
> - Re-run the CODE again, and check it

**Operation 3:** rendering an image file
> - Before run the code for the last operation, copy and paste the **PATH** of the blender execution file on the ***blender_path*** variable
> - Now you run it
> - The output file is in ***IMAGE_RENDERED*** folder



## Other Info
**Python Version:**
>3.11

**Environment:**
> I suggest on using a virtual enviroment or just a simple IDE with a virtual environment as a set-up
