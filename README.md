# Stage_MeshMedicali

## Table of Contents
- [General Description](#general-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Details](#details)
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
    "type_off_file": "noff",
    "dataname": "off file name (no extension specification)",
    "logfile_name_processing": "logTprocessing",
    "logfile_name_blender": "logTBlender",
    "value_eps": 1.02,
    "value_minsamples": 5,
    "value_decimation": 140000,
    "value_scalefactor": 1,
    "value_scalingtype": 1,
    "poisson_density": 12390,
    "name_off_file": "test_repaired",
    "processing_0": false,
    "processing_1": [
        false,
        false
    ],
    "blend_file_ex": true,
    "fill_holes": false,
    "blend_file_name": "testBlend_",
    "plane_on_base_size": 300,
    "base_plane_location": [
        0,
        0,
        -0.000925
    ],
    "cube_size": 1,
    "cube_rotation": [
        0,
        0,
        0
    ],
    "axes_rotation": [
        0,
        0,
        -161.18
    ],
    "axes_location": [
        0,
        0,
        -1.52386
    ],
    "camera_rotation": [
        90,
        0,
        135.458
    ],
    "camera_type" : "persp",
    "lens_camera" : 50,
    "ortho_scale" : 6,
    "camera_axes_offset": 1,
    "camera_light_offset": 0,
    "light_energy_at_camera": 90,
    "light_energy_at_camera_radius": 1.12,
    "light_front": 0,
    "light_back": 3,
    "light_right": 0,
    "light_left": 2.5,
    "light_top": 1.5,
    "light_bottom": 0,
    "lights_radius": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.73,
        0.0
    ],
    "light_set": 2,
    "sun_strength": 0.0,
    "sun_angle": 32.2,
    "sun_location": [
          0.0, 
          0.0, 
          3.0
      ],
      "sun_rotation": [
          0.0, 
          0.0, 
          0.0
      ],
      "sun_color": [
          1.0, 
          1.0, 
          1.0
      ],
    "material_value": 5,
    "color_map_value": 3,
    "name_scalar_field_txt": "registered_fmap.txt",
    "name_scalar_labels_txt": "template_labels.txt",
    "is_deformation_active": true,
    "median_coordinate": [
        [0.113773, 0.450449, 0.409456],
        [0.163708, -0.307038, 0.556879],
        [0.218791, -0.259485, 0.163292]
    ],
    "number_deformation" : 0,
    "min_value" : -0.5,
    "max_value" : 0.5,
    "uv_scale_factor" : 0.1,
    "material_plane_value": 1,
    "hex_color": [
        "000000",
        "A77843",
        "FFB100"
    ],
    "color_transp_bsdf": [],
    "color_diff_bsdf": [],
    "wall_front": true,
    "wall_back": true,
    "wall_right": true,
    "wall_left": true,
    "type_engine": 0,
    "floor_transparency" : false,
    "film_transparency" : false,
    "type_device": "GPU",
    "n_samples": 300,
    "file_format": "png",
    "screen_percentage": 1,
    "render_file_ex": false,
    "render_file_name": "testION_",
    "blender_path_execute": "Path Blender Executable Program"
}
```
- `type_off_file` : **String-value.** Off's file type, with normals (NOFF), without normals (OFF)
- `dataname`: **String-value.** File's name the program is going to work on. The User does not have to change the name every single time, **'name_off_file'** comes to help.
- `logfile_name_processing`: **String-value.** File txt's name where the description of the operation will be saved. ***[Processing Operation Only]***
- `logfile_name_blender`: **String-value.** File txt's name where the description of the operation will be saved. ***[Blender Operation Only]***
- `value_eps`: **Float-value.** Value to detect the distance between point. Points inside this are called 'cluster'. ***[Processing Operation Only]***
- `value_minsamples`: **Integer-value.** Value to define the min numbers of points inside a cluster. ***[Processing Operation Only]***
- `value_decimation`: **Integer-value.** Value used to decimanted the mesh. ***[Processing Operation Only]***
- `value_scalefactor`: **Float-value.** Value used to scale a mesh. ***[Processing Operation Only]***
- `value_scalingtype`: **Integer-value.** Value to choose what scaling type apply on the mesh. [**Type 0**: scaling on X, Y and Z. **Type 1**: scaling to UNIT-BOX. **Type 2**: scaling to UNIT-SPHERE] ***[Processing Operation Only]***
- `poisson_density` : **Integer-value.** Value for reconstruction off type file with no normals. Same function as the ***value_decimantion***.
- `name_off_file`: **String-value.** String value added as a prefix on the file Generated during the pipeline's ***Phase 0*** and ***Phase 1***.
- `processing_0`: **Boolean-value.** Define the ***Phase 0*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `processing_1`: **Array Boolean-value.** Define the ***Phase 1*** of the Pipeline, each item corresponds to the specific operation. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `blend_file_ex`: **Boolean-value.** Define the ***Phase 2*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `fill_holes`: **Boolean-value.** Apply the fill holes in Blender Environment.
- `blend_file_name`: **String-value.** String name to define the blend file.
- `plane_on_base_size`: **Integer-value.** Dimension of the plane at the base.
- `base_plane_location`: **List-value.** Location of the plane base on X, Y and Z.
- `cube_size`: **Integer-value.** Dimension of the CUBE.
- `cube_rotation`: **List-value.** Rotation on X, Y and Z.
- `axes_rotation`: **List-value.** Rotation on X, Y and Z.
- `axes_location`: **List-value.** Location on X, Y and Z.
- `camera_rotation`: **List-value.** Rotation on X, Y and Z.
- `camera_type`: **String-value.** Choose the type for the camera; ***"persp"*=Perspective*** and ***"ortho"*=Orthogonal***
- `lens_camera`: **Float-value.** Focal Length of the camera in **Perspective**-mode.
- `ortho_scale`: **Float-value.** Scale of the camera in **Orthographic**-mode.
- `camera_axes_offset`: **Float-value.** Offset value from Axes to Camera
- `camera_light_offset`: **Float-value.** Offset value from Camera to Light-at-Camera
- `light_energy_at_camera`: **Float-value.** Energy value for light.
- `light_energy_at_camera_radius`: **Float-value.** Radius of light for soft ray-light.
- `light_front`: **Float-value.** Energy value for light.
- `light_back`: **Float-value.** Energy value for light.
- `light_right`: **Float-value.** Energy value for light.
- `light_left`: **Float-value.** Energy value for light.
- `light_top`: **Float-value.** Energy value for light.
- `light_bottom`: **Float-value.** Energy value for light.
- `ligths_radius`: **Array with Float-values.** Radius of lights in 3D environment for soft ray-light
- `light_set`: **Integer-value.** Value to choose a light set ***(Look at: [Light](#light)).***
- `sun_strength`: **Float-value.** Energy value for light.
- `sun_angle`: **Float-value.** Angle of the light.
- `sun_location`: **Array-Float values.** Define the location of the sun-light.
- `sun_rotation`: **Array-Float values.** Define the rotation of the sun-light.
- `sun_color`: **Array-Float values.** Define the color of the sun-light.
- `material_value`: **Integer-value.** Value to choose a material to apply to the mesh ***(Look at: [Material](#material)).***
- `color_map_value`: **Integer-value.** Value to choose a color-map material ***(material_value=6 in order to choose the color-map).***
- `scalar_field`: **Boolean-value.** If the User has the txt's file with the scalar field.
- `name_scalar_field_txt`: **String-value.** Name of the file with the scalar field.
- `name_scalar_labels_txt`: **String-value.** Name of the file with labels referring to the mesh.
- `is_deformation_active`: **Boolean-value.** Value to activate or deactivate the customized deformation on mesh.
- `median_coordinate`: **Array's Array with 3D coordinates.** Represents the coordinates on where to apply the deformation.
- `number_deformation`: **Integer-value.** Apply quantity (var value) random deformation on mesh.
- `min_value`: **Float-value**. Min range to deform.
- `max_value`: **Float-value**. Max range to deform.
- `uv_scale_factor`: **Float-value**. Value for scaling an uv-sphere.
- `material_plane_value`: **Integer-value**. Value to choose a material to apply to the planes ***(Look at: [Material](#material)).***
- `hex_color`: **List-value**. String values inside the list. The strings are the HEX value of the colors.
- `color_transp_bsdf`: **List-value**. String values inside the list. The strings are the HEX value of the colors. ***(Only if material-value=4)***
- `color_diff_bsdf`: **List-value**. String values inside the list. The strings are the HEX value of the colors. ***(Only if material-value=4)***
- `wall_front`: **Boolean-value**. True or False if plane should appear in the 3D world.
- `wall_back`: **Boolean-value**. True or False if plane should appear in the 3D world.
- `wall_right`: **Boolean-value**. True or False if plane should appear in the 3D world.
- `wall_left`: **Boolean-value**. True or False if plane should appear in the 3D world.
- `type_engine`: **Integer-value**. Value to choose the type of engine ***[0-CYCLES, 1-EEVEE]***
- `floor_transparency`: **Boolean-value**. Value to apply a transparency on planes object in 3D Environment.
- `film_transparency`: **Boolean-value**. Value to apply a transparency in 3D Environment.
- `type_device`: **String-value**. Value to choose the type of device ***[GPU, CPU]***
- `n_sample`: **Integer-value**. Number of sample for rendering the Image
- `file_format`: **String-value**. Value to choose the format of the rendered file ***[png, jpeg]***
- `screen_percentage` **Float-value**. Value to choose the percentage of the screen. Default:1
- `render_file_ex`: **Boolean-value.** Define the ***Phase 3*** of the Pipeline. Loot at [Pipeline Operation](#pipeline-operation)'s Phases.
- `render_file_name`: **String-value.** String name to define the rendering image name.
- `blender_path_execute`: **String-value.** String path of Blender program.

# Details
### MATERIAL
>The program give the User the permission to choose on different type of materials.
>Below you can find the ***name of the material*** and the ***number to apply it***.

>**MESH**
- **0** : **Dull Yellow**
- **1** : **Transparent / Glass**
- **2** : **Wireframe**
- **3** : **Custom**
- **4** : **Full-Transparency**
- **5** : **ColorMap's Values:**
    - **0** : **Propagation from Origin**
    - **1** : **Curvature Analysis**
    - **2** : **Heat-Map on Axis**
    - **3** : **Deformation on Surface**
- **6** : **ColorMaps - Scalar Value**

>**PLANE**:
- **0** : **White**
- **1** : **White with Emission - better for Full-Transparency Material**


### LIGHT
>There ara 6 lights type: **SPOT** in the 3D WORLD + 1 light type: **SUN**.
>The program lets the User chooses on **4 different Light set mode**:

- **0** : **Customize by the User**
- **1** : *mode=6 light.* ***Film Lighting Scenario***
- **2** : *mode=6 light.* ***ShowRoom Lighting Scenario***
- **3** : **BLACK MODE, all lights are turned OFF - useful for Wireframe Material, Sun-Light**



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

**Blender Version:**
>4.2

**Environment:**
> I suggest on using a virtual enviroment or just a simple IDE with a virtual environment as a set-up
