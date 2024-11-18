# Stage_MeshMedicali

## GENERAL DESCRIPTION
> **What the Pipeline do** 
- Processing an .off file with a mesh in it ,
- Creating a .blend file through the Blender API bpy
- Rendering an image from Python script


> **Time Execution:**

- remove_zero_area_faces : about 3.97 sec

- removing not connected components : about 2.79 sec

- scaling : about 0.23 sec

- repair_mesh : about 4.62 sec

## Configuration
The configuration file (`config.json`) should follow the sample below:

```json
{
    "device": "cuda:0",
    "seeds": [21, 314, 561, 41041, 9746347772161, 1007, 11051999, 27092000, 20071969, 4101957],
    "prompt_1": "cat",
    "prompt_2": "lion",
    "blend_methods": ["SWITCH", "UNET", "TEXTUAL", "ALTERNATE"],
    "timesteps": 25,
    "scheduler": "UniPCMultistepScheduler",
    "model_id": "CompVis/stable-diffusion-v1-4",
    "height": 512,
    "width": 512,
    "latent_scale": 8,
    "guidance_scale": 7.5,
    "from_timestep": 8, 
    "to_timestep": 25,
    "TEXTUAL_scale": 0.5, 
    "same_base_latent": true
}
```
- `device`: Device to run the code (default: `cuda:0`).
- `seeds`: List of seeds for the random number generator.
- `prompt_1`: First textual prompt.
- `prompt_2`: Second textual prompt.
- `blend_methods`: List of blending methods to use.
- `timesteps`: Number of timesteps for the diffusion process.
- `scheduler`: Scheduler to use for the diffusion process.
- `model_id`: Model ID for the diffusion model.
- `height`: Height of the image.
- `width`: Width of the image.
- `latent_scale`: Latent scale for the diffusion model.
- `guidance_scale`: Guidance scale for the diffusion model.
- `from_timestep`: Exclusive to the `SWITCH` method, controls the timestep at which the __switch__ is performed.
- `to_timestep`: Exclusive to the `SWITCH` method, controls the timestep at which the synthesis of the image is completed.
- `TEXTUAL_scale`: Exclusive to the `TEXTUAL` method, controls the ratio of the blending between the two prompts.
- `same_base_latent`: Whether to use the same base latent for all blending methods.


## TUTORIAL FIRST TIME USING THE CODE
**mainPipelineT.py:** is the main and the only file you sould focus on

> **But first you need to, manually, add the screen resolution of your screen**
> 
> *Till new updates, do it manually*
> 
> **After each execution the program ask the User if he wants to continue with the Pipeline Operation or Re-Run an operation**

**Back to the tutorial:** 

-  In the **mainPipelineT.py** 
> there is a description of what the methods / functions do and the type of settings the User could do

- *Variable:* **dataname**
> contains the file-name of the mesh the programm should work on, during the pipeline operantion the User **DO NOT NEED** to change it everytime, only at the beginning

## Pipeline operation
**OPERATION 0:** processing the mesh
> - Remove Zero Area Faces
> - Remove Not Connected Components

- **Before starting the next operation, add the file generated in the *OUTPUT_SOURCE* to the *INPUT_SOURCE* folder**

**OPERATION 1:** processing the mesh
> - Repair Mesh
> - Scaling Mesh

- **For the last time, before starting the next operation, add the file generated in the *OUTPUT_SOURCE* to the *INPUT_SOURCE* folder**

**OPERATION 2:** set up the .blend file
> What I suggest is:
> - Try to run it, AS IS, open the **outFinal.blend** and check on it
> - Make the changes you in the blend file and reported to the CODE too
> - Delete the previous blend files created
> - Re-run the CODE again, and check it

**OPERATION 3:** rendering an image file
> - Before run the code for the last operation, copy and paste the **PATH** of the blender execution file on the ***blender_path*** variable
> - Now you run it
> - The output file is in ***IMAGE_RENDERED*** folder

That is the end of the tutorial of how the User should work on this CODE


## Other Info
**Python Version:**
>3.11

**Libraries:**
> - numpy
> - subprocess
> - os
> - bpy
> - open3d

**Environment:**
> I suggest on using a virtual enviroment or just a simple IDE with a virtual environment as a set-up
