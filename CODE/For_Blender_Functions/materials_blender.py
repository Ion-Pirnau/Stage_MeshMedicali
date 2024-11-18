import bpy

class CreationMaterial:

    material_type = None
    material_plane_type = None
    message_material = None
    color_trasparent_bsdf = []
    color_diffuse_bsdf = []


    # Initialize the class with default values or User' values
    def __init__(self, material_type=0, material_plane_type=0, color_trasparent_bsdf=[], color_diffuse_bsdf=[]) -> None:
        self.material_type = material_type
        self.material_plane_type = material_plane_type
        self.color_trasparent_bsdf = color_trasparent_bsdf
        self.color_diffuse_bsdf = color_diffuse_bsdf

    def check_parameter(self) -> None:
        # Check material_type is between 0 and 4
        if not (0 <= self.material_type <= 4):
            raise ValueError(f"The integer chosen as material type ({self.material_type}) is incorrect. It must be between 0 and 4.")

        # Check material_plane_type is between 0 and 1
        if not (0 <= self.material_plane_type <= 1):
            raise ValueError(f"The integer chosen as material plane type ({self.material_plane_type}) is incorrect. It must be either 0 or 1.")

    # Based on the material_type, there are 5 material that can be applied on the mesh
    def fetch_material(self):
        result = None

        if self.material_type == 0:
            result = self.material_giallo_opaco()
        elif self.material_type == 1:
            result = self.material_trasparente()
        elif self.material_type == 2:
            result = self.material_wireframe()
        elif self.material_type == 3:
            result = self.material_custom()
        elif self.material_type == 4:
            result = self.material_full_transparency()
        else:
            raise ValueError(f"Material Type: {self.material_type}, does not exists!")

        return  result

    # As the previous methods: 2 materials for the plane
    def fetch_material_plane(self):
        result = None

        if self.material_plane_type == 0:
            result = self.material_white_plane()
        elif self.material_plane_type == 1:
            result = self.material_white_plane_emission()
        else:
            raise ValueError(f"Material Plane Type: {self.material_type}, does not exists!")

        return result

    # Material Function Section: Create the material and return it
    def material_giallo_opaco(self):
        material = bpy.data.materials.new(name="GialloOpaco")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')

        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        r, g, b = self.hex_to_rgb("#E3E8A6")
        principled.inputs['Base Color'].default_value = (r, g, b, 1)
        principled.inputs['Roughness'].default_value = 0.780
        principled.inputs['IOR'].default_value = 1.350

        self.write_message("Giallo-Opaco")
        return material

    def material_trasparente(self):
        material = bpy.data.materials.new(name="Trasparente")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        fresnel = nodes.new(type='ShaderNodeFresnel')

        transparent.inputs['Color'].default_value = (*self.hex_to_rgb("#FFFFFF"), 1)
        # FFF5E0, D9D6B1
        principled.inputs['Base Color'].default_value = (*self.hex_to_rgb("#FFF5E0"), 1)
        principled.inputs['Roughness'].default_value = 0.5
        fresnel.inputs['IOR'].default_value = 1.48

        color_ramp.color_ramp.elements[0].position = 0.0
        color_ramp.color_ramp.elements[0].color = (*self.hex_to_rgb_color_ramp("#A6A6A6"), 1)
        color_ramp.color_ramp.elements[1].position = 1.0
        color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)

        links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        links.new(principled.outputs['BSDF'], mix_shader.inputs[2])
        links.new(fresnel.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], mix_shader.inputs['Fac'])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])


        self.write_message("Trasparente-Vetro")
        return material

    def material_wireframe(self):
        material = bpy.data.materials.new(name="Wireframe")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        mix_shader1 = nodes.new(type='ShaderNodeMixShader')
        mix_shader2 = nodes.new(type='ShaderNodeMixShader')
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        emission = nodes.new(type='ShaderNodeEmission')
        value_input = nodes.new(type='ShaderNodeValue')
        wireframe = nodes.new(type='ShaderNodeWireframe')
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        fresnel = nodes.new(type='ShaderNodeFresnel')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')


        r, g, b = self.hex_to_rgb("#D4D8D9")

        transparent.inputs['Color'].default_value = (r, g, b, 1)

        r, g, b = self.hex_to_rgb("#FFF7F3")

        emission.inputs['Color'].default_value = (r, g, b, 1)
        value_input.outputs['Value'].default_value = 0.280
        wireframe.inputs['Size'].default_value = 0.001

        r, g, b = self.hex_to_rgb("#D9D6B1")

        principled.inputs['Base Color'].default_value = (r, g, b, 1)
        fresnel.inputs['IOR'].default_value = 1.48
        color_ramp.color_ramp.interpolation = 'LINEAR'
        color_ramp.color_ramp.elements[0].position = 0.0

        r, g, b = self.hex_to_rgb_color_ramp("#878380")

        color_ramp.color_ramp.elements[0].color = (r, g, b, 1)
        color_ramp.color_ramp.elements[1].position = 1.0
        color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)


        links.new(transparent.outputs['BSDF'], mix_shader1.inputs[1])
        links.new(emission.outputs['Emission'], mix_shader1.inputs[2])
        links.new(value_input.outputs['Value'], emission.inputs['Strength'])
        links.new(wireframe.outputs['Fac'], mix_shader1.inputs[0])
        links.new(mix_shader1.outputs['Shader'], mix_shader2.inputs[1])
        links.new(principled.outputs['BSDF'], mix_shader2.inputs[2])
        links.new(color_ramp.outputs['Color'], mix_shader2.inputs[0])
        links.new(fresnel.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(mix_shader2.outputs['Shader'], output.inputs['Surface'])

        self.write_message("Wireframe")
        return material

    def material_custom(self):
        color_add_1_hex = '#5D4B00'
        color_add_2_hex = '#A7BAB4'

        material = bpy.data.materials.new(name="Custom")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        voronoi_1 = nodes.new(type='ShaderNodeTexVoronoi')
        voronoi_2 = nodes.new(type='ShaderNodeTexVoronoi')
        mapping_1 = nodes.new(type='ShaderNodeMapping')
        mapping_2 = nodes.new(type='ShaderNodeMapping')
        texture_coord = nodes.new(type='ShaderNodeTexCoord')
        invert_1 = nodes.new(type='ShaderNodeInvert')
        invert_2 = nodes.new(type='ShaderNodeInvert')
        value = nodes.new(type='ShaderNodeValue')
        add_math = nodes.new(type='ShaderNodeMath')
        add_1 = nodes.new(type='ShaderNodeMixRGB')
        add_2 = nodes.new(type='ShaderNodeMixRGB')
        multiply = nodes.new(type='ShaderNodeMixRGB')
        brightness_contrast = nodes.new(type='ShaderNodeBrightContrast')
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        bump = nodes.new(type='ShaderNodeBump')
        subsurface_scattering = nodes.new(type='ShaderNodeSubsurfaceScattering')

        voronoi_1.feature = 'F1'
        voronoi_1.distance = 'EUCLIDEAN'
        voronoi_1.inputs['Scale'].default_value = 6.0
        voronoi_1.inputs['Randomness'].default_value = 0.375
        invert_1.inputs['Fac'].default_value = 1.0

        voronoi_2.feature = 'F1'
        voronoi_2.distance = 'EUCLIDEAN'
        voronoi_2.inputs['Scale'].default_value = 6.0
        voronoi_2.inputs['Randomness'].default_value = 0.98
        invert_2.inputs['Fac'].default_value = 1.0

        value.outputs[0].default_value = 1.4
        add_math.operation = 'ADD'
        add_math.inputs[1].default_value = 0.5

        multiply.blend_type = 'MULTIPLY'
        multiply.inputs[0].default_value = 1.0
        color_ramp.color_ramp.elements[0].position = 0.116
        color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)

        brightness_contrast.inputs['Bright'].default_value = -0.2
        brightness_contrast.inputs['Contrast'].default_value = -0.8

        add_1.blend_type = 'ADD'
        add_1.inputs[1].default_value = (*self.hex_to_rgb(color_add_1_hex), 1)
        add_2.blend_type = 'ADD'
        add_2.inputs[1].default_value = (*self.hex_to_rgb(color_add_2_hex), 1)


        principled.inputs['Roughness'].default_value = 0.5

        bump.inputs['Strength'].default_value = 0.85
        subsurface_scattering.inputs['Scale'].default_value = 1.0
        subsurface_scattering.inputs['Radius'].default_value = (1.0, 0.2, 0.1)
        subsurface_scattering.inputs['IOR'].default_value = 1.4

        links.new(texture_coord.outputs['Object'], mapping_1.inputs['Vector'])
        links.new(mapping_1.outputs['Vector'], voronoi_1.inputs['Vector'])
        links.new(voronoi_1.outputs['Distance'], invert_1.inputs['Color'])
        links.new(texture_coord.outputs['Object'], mapping_2.inputs['Vector'])
        links.new(mapping_2.outputs['Vector'], voronoi_2.inputs['Vector'])
        links.new(voronoi_2.outputs['Distance'], invert_2.inputs['Color'])
        links.new(value.outputs[0], mapping_1.inputs['Scale'])
        links.new(value.outputs[0], add_math.inputs[0])
        links.new(add_math.outputs["Value"], mapping_2.inputs['Scale'])
        links.new(invert_1.outputs['Color'], multiply.inputs[1])
        links.new(invert_2.outputs['Color'], multiply.inputs[2])
        links.new(multiply.outputs['Color'], brightness_contrast.inputs['Color'])
        links.new(brightness_contrast.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], principled.inputs['Normal'])
        links.new(color_ramp.outputs['Color'], add_1.inputs[2])
        links.new(add_1.outputs['Color'], principled.inputs['Base Color'])
        links.new(color_ramp.outputs['Color'], add_2.inputs[2])
        links.new(add_2.outputs['Color'], subsurface_scattering.inputs['Color'])
        links.new(principled.outputs['BSDF'], mix_shader.inputs[1])
        links.new(subsurface_scattering.outputs['BSSRDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

        self.write_message("Custom-Material")
        return material

    def material_full_transparency(self):
        material = bpy.data.materials.new(name="FullTransparency")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links


        # B6B6B3, E5E5E1
        color_transparent_hex = '#B6B6B3'
        # FFFFFF, C3C0B8
        color_diffuse_hex = '#FFFFFF'

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
        value = nodes.new(type='ShaderNodeValue')

        if not self.color_trasparent_bsdf and not self.color_diffuse_bsdf:
            transparent.inputs['Color'].default_value = (*self.hex_to_rgb(color_transparent_hex), 1)
            diffuse.inputs['Color'].default_value = (*self.hex_to_rgb(color_diffuse_hex), 1)
        else:
            transparent.inputs['Color'].default_value = (self.color_trasparent_bsdf[0], self.color_trasparent_bsdf[1],
                                                         self.color_trasparent_bsdf[2], 1)
            diffuse.inputs['Color'].default_value = (self.color_diffuse_bsdf[0], self.color_diffuse_bsdf[1],
                                                     self.color_diffuse_bsdf[2], 1)
        value.outputs[0].default_value = 0.080

        links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        links.new(diffuse.outputs['BSDF'], mix_shader.inputs[2])
        links.new(value.outputs['Value'], mix_shader.inputs['Fac'])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

        self.write_message("Full-Transparency")
        return material

    def material_white_plane(self):
        material = bpy.data.materials.new(name="WhitePlane")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        principled_bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')

        principled_bsdf_node.inputs["Base Color"].default_value = (1, 1, 1, 1)
        principled_bsdf_node.inputs["Metallic"].default_value = 0.0
        principled_bsdf_node.inputs["Roughness"].default_value = 0.1

        links.new(principled_bsdf_node.outputs['BSDF'], output.inputs['Surface'])

        self.write_message("White-Plane", False)

        return material

    def material_white_plane_emission(self):
        material = bpy.data.materials.new(name="WhitePlaneEmission")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        emission = nodes.new(type='ShaderNodeEmission')
        value = nodes.new(type='ShaderNodeValue')

        principled.inputs['Base Color'].default_value = (1, 1, 1, 1)
        principled.inputs['Roughness'].default_value = 0.1
        emission.inputs['Color'].default_value = (1, 1, 1, 1)
        emission.inputs['Strength'].default_value = 0.2
        value.outputs[0].default_value = 0.5

        links.new(principled.outputs['BSDF'], mix_shader.inputs[1])
        links.new(emission.outputs['Emission'], mix_shader.inputs[2])
        links.new(value.outputs['Value'], mix_shader.inputs['Fac'])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

        self.write_message("White-Plane-Emission", False)

        return material

    # Create a variable where to write the material that has been applied, in order to write it on the file
    def write_message(self, messaggio="None", type_value=True):
        if type_value:
            self.message_material = "Material choosed: " + messaggio + "\n"
        else:
            self.message_material += "Material Plane choosed: " + messaggio + "\n"
    # Get the message variable
    def get_message(self):
        return self.message_material

    # Convert the HEX to RGB : due to some value-offset that BLENDER applies, the good offset value is: 2.26
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')

        if len(hex_color) != 6:
            raise ValueError(f"The value: {hex_color} is not acceptable")

        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0

        r = r ** (2.26)
        g = g ** (2.26)
        b = b ** (2.26)
        return r, g, b

    # Convert the HEX t RGB for color ramp : offset value 2.246
    def hex_to_rgb_color_ramp(self, hex_color):
        hex_color = hex_color.lstrip('#')

        if len(hex_color) != 6:
            raise ValueError(f"The value: {hex_color} is not acceptable")

        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0

        #2.23
        r = r ** (2.246)
        g = g ** (2.246)
        b = b ** (2.246)
        return r, g, b

