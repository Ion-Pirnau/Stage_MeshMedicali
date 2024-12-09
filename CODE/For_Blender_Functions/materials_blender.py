import bpy

class CreationMaterial:
    """
        Class: defining the material to apply to the Mesh and Plane + the ColorMap to the Mesh
    """


    material_type = None
    material_plane_type = None
    message_material = None
    color_transparent_bsdf = []
    color_diffuse_bsdf = []
    color_map_value = None
    hex_color = []

    # Initialize the class with default values or User' values
    def __init__(self, material_type=0, material_plane_type=0, color_map_value=0,
                 hex_color=[], color_transparent_bsdf=[], color_diffuse_bsdf=[], mix_shader_fac=0.5) -> None:
        self.material_type = material_type
        self.material_plane_type = material_plane_type
        self.color_map_value = color_map_value
        self.hex_color = hex_color
        self.color_transparent_bsdf = color_transparent_bsdf
        self.color_diffuse_bsdf = color_diffuse_bsdf
        self.mix_shader_fac = mix_shader_fac

    def check_parameter(self) -> None:
        # Check material_type is between 0 and 4
        if not (0 <= self.material_type <= 6):
            raise ValueError(f"The integer chosen as material type "
                             f"({self.material_type}) is incorrect. It must be between 0 and 6.")

        # Check material_plane_type is between 0 and 1
        if not (0 <= self.material_plane_type <= 1):
            raise ValueError(f"The integer chosen as material plane type "
                             f"({self.material_plane_type}) is incorrect. It must be either 0 or 1.")

    # Based on the material_type, there are 5 material that can be applied on the mesh
    def fetch_material(self):

        """
            Function: fetch the type of material the User choose for the Mesh

            Return:
                bpy.ops.material

        """

        result = None

        if self.material_type == 0:
            result = self.material_dull_yellow()
        elif self.material_type == 1:
            result = self.material_transparent_glass()
        elif self.material_type == 2:
            result = self.material_wireframe()
        elif self.material_type == 3:
            result = self.material_custom()
        elif self.material_type == 4:
            result = self.material_full_transparency()
        elif self.material_type == 5:
            result = self.material_colormap_mesh()
        elif self.material_type == 6:
            result = self.scalar_map_material()
        else:
            raise ValueError(f"Material Type: {self.material_type}, does not exists!")

        return  result

    # As the previous methods: 2 materials for the plane
    def fetch_material_plane(self):
        """
            Function: fetch the type of material the User choose for the Planes

            Return:
                bpy.ops.material

        """

        result = None

        if self.material_plane_type == 0:
            result = self.material_white_plane()
        elif self.material_plane_type == 1:
            result = self.material_white_plane_emission()
        else:
            raise ValueError(f"Material Plane Type: {self.material_type}, does not exists!")

        return result



    # Material Function Section: Create the material and return it
    def material_dull_yellow(self):

        """
            Function: create material Dull-Yellow

            Returns:
                bpy.ops.material
        """

        material = bpy.data.materials.new(name="Dull Yellow")
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

        self.write_message("Dull Yellow")
        return material

    def material_transparent_glass(self):
        """
            Function: create material Transparent-Glass

            Returns:
                bpy.ops.material
        """

        material = bpy.data.materials.new(name="Transparent")
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


        self.write_message("Transparent-Glass")
        return material

    def material_wireframe(self):
        """
            Function: create material Wireframe

            Returns:
                bpy.material.ops

        """

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
        """
            Function: create material Custom

            Returns:
                bpy.ops.material

        """

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
        """
            Function: create material Full Transparency

            Returns:
                bpy.ops.material

        """


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

        if not self.color_transparent_bsdf and not self.color_diffuse_bsdf:
            transparent.inputs['Color'].default_value = (*self.hex_to_rgb(color_transparent_hex), 1)
            diffuse.inputs['Color'].default_value = (*self.hex_to_rgb(color_diffuse_hex), 1)
        else:
            transparent.inputs['Color'].default_value = (self.color_transparent_bsdf[0], self.color_transparent_bsdf[1],
                                                         self.color_transparent_bsdf[2], 1)
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
        """
            Function: create material White Planes

            Returns:
                bpy.ops.material

        """


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

        """
            Function: create material white with Emission

            Returns:
                bpy.ops.material

        """

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



    def material_colormap_mesh(self):

        """
            Function: create a color-map applied to a mesh

            Returns:
                bpy.ops.material
        """

        material = bpy.data.materials.new(name="Color Map")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)


        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        separate_xyz = nodes.new(type='ShaderNodeSeparateXYZ')
        texture_coordinate = nodes.new(type='ShaderNodeTexCoord')


        if self.color_map_value == 0:
            self.propagation_from_origin(links, nodes, output, principled, color_ramp, separate_xyz, texture_coordinate)
        elif self.color_map_value == 1:
            self.curvature_analysis(links, nodes, output, principled, color_ramp, separate_xyz, texture_coordinate)
        elif self.color_map_value == 2:
            self.heat_map_on_axis(links, output, principled, color_ramp, separate_xyz, texture_coordinate, type_of_axes='X')
        elif self.color_map_value == 3:
            self.deformation_on_surface(links, nodes, output, principled, color_ramp, texture_coordinate)
        else:
            raise ValueError(f"ColorMap Type: {self.color_map_value}, does not exists. Values Accepted: 0 to 3!")

        return material



    def propagation_from_origin(self, links, nodes, output, principled, color_ramp, separate_xyz, texture_coordinate):

        """
            Function: create a colormap, type - Propagation from Origin.
            Colors changing based on the distance from the Origin

            Args:
                links : linking the nodes
                output : output node to display the color map on the mesh
                principled : principled node shader
                nodes : nodes in Shader Editor
                color_ramp : color ramp to display on the mesh
                separate_xyz : separate the Three Coordinates to work on
                texture_coordinate : fetch information from the Object

        """



        math_one = nodes.new(type='ShaderNodeMath')
        math_two = nodes.new(type='ShaderNodeMath')
        math_three = nodes.new(type='ShaderNodeMath')
        math_four = nodes.new(type='ShaderNodeMath')
        math_five = nodes.new(type='ShaderNodeMath')
        math_six = nodes.new(type='ShaderNodeMath')

        math_one.operation = 'POWER'
        math_one.inputs[1].default_value = 2.0
        math_two.operation = 'POWER'
        math_two.inputs[1].default_value = 2.0
        math_three.operation  = 'ADD'
        math_four.operation = 'SQRT'
        math_five.operation = 'MULTIPLY'
        math_five.inputs[1].default_value = 2.45
        math_six.operation = 'SINE'

        self.add_color_to_color_ramp(color_ramp, 0.0, self.hex_color[0], is_black=True)
        self.add_color_to_color_ramp(color_ramp, 0.5, self.hex_color[1])
        self.add_color_to_color_ramp(color_ramp, 1.0, self.hex_color[2], flag=1, is_white=True)

        links.new(texture_coordinate.outputs['Object'], separate_xyz.inputs['Vector'])
        links.new(separate_xyz.outputs['X'], math_one.inputs[0])
        links.new(separate_xyz.outputs['Y'], math_two.inputs[0])
        links.new(math_one.outputs['Value'], math_three.inputs[0])
        links.new(math_two.outputs['Value'], math_three.inputs[1])
        links.new(math_three.outputs['Value'], math_four.inputs['Value'])
        links.new(math_four.outputs['Value'], math_five.inputs['Value'])
        links.new(math_five.outputs['Value'], math_six.inputs['Value'])
        links.new(math_six.outputs['Value'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        self.write_message("ColorMap=Propagation_fromOrigin", True)


    def curvature_analysis(self, links, nodes, output, principled, color_ramp, separate_xyz, texture_coordinate):
        """
            Function: create a colormap, type - Curvature Analysis.
            Define the curvature's level on the mesh surface

            Args:
                links : linking the nodes
                output : output node to display the color map on the mesh
                principled : principled node shader
                nodes : nodes in Shader Editor
                color_ramp : color ramp to display on the mesh
                separate_xyz : separate the Three Coordinates to work on
                texture_coordinate : fetch information from the Object

        """

        dot_product_node = nodes.new(type='ShaderNodeVectorMath')
        dot_product_node.operation = 'DOT_PRODUCT'

        self.add_color_to_color_ramp(color_ramp, 0.0, self.hex_color[0], is_black=True)
        self.add_color_to_color_ramp(color_ramp, 0.5, self.hex_color[1])
        self.add_color_to_color_ramp(color_ramp, 1.0, self.hex_color[2], flag=1, is_white=True)

        links.new(texture_coordinate.outputs['Normal'], separate_xyz.inputs['Vector'])
        links.new(separate_xyz.outputs['X'], dot_product_node.inputs[0])
        links.new(separate_xyz.outputs['Y'], dot_product_node.inputs[1])
        links.new(dot_product_node.outputs['Value'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        self.write_message("ColorMap=Curvature_Analysis", True)


    def heat_map_on_axis(self, links, output, principled, color_ramp, separate_xyz, texture_coordinate, type_of_axes='X'):

        """
            Function: create a colormap, type - Heat Map on Axes
            Colors changing based on the position on a particular Axis

            Args:
                links : linking the nodes
                output : output node to display the color map on the mesh
                principled : principled node shader
                color_ramp : color ramp to display on the mesh
                separate_xyz : separate the Three Coordinates to work on
                texture_coordinate : fetch information from the Object
                type_of_axes : type of axes where apply the colormap

        """

        self.add_color_to_color_ramp(color_ramp, 0.0, self.hex_color[0], is_black=True)
        self.add_color_to_color_ramp(color_ramp, 0.5, self.hex_color[1])
        self.add_color_to_color_ramp(color_ramp, 1.0, self.hex_color[2], flag=1, is_white=True)

        links.new(texture_coordinate.outputs['Generated'], separate_xyz.inputs['Vector'])
        links.new(separate_xyz.outputs[type_of_axes], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        self.write_message(f"ColorMap=HeatMap on Axis' {type_of_axes}", True)


    def deformation_on_surface(self, links, nodes, output, principled, color_ramp, texture_coordinate):

        """
            Function: creation of ColorMap, type - Deformation on Surface
            Check the deformation on Mesh's Surface

            Args:
                links : linking the nodes
                output : output node to display the color map on the mesh
                principled : principled node shader
                nodes : nodes in Shader Editor
                color_ramp : color ramp to display on the mesh
                texture_coordinate : fetch information from the Object
        """

        self.add_color_to_color_ramp(color_ramp, 0.0, self.hex_color[0], is_black=True)
        self.add_color_to_color_ramp(color_ramp, 0.5, self.hex_color[1])
        self.add_color_to_color_ramp(color_ramp, 1.0, self.hex_color[2], is_white=True, flag=1)

        geometry_node = nodes.new(type="ShaderNodeNewGeometry")

        math_multiply = nodes.new(type='ShaderNodeMath')
        math_multiply.operation = 'MULTIPLY'

        color_ramp_mask = nodes.new(type='ShaderNodeValToRGB')
        self.add_color_to_color_ramp(color_ramp_mask, 0.705, "000000", is_white=True)
        self.add_color_to_color_ramp(color_ramp_mask, 0.182, "FFFFFF", is_black=True)



        mapping = nodes.new(type='ShaderNodeMapping')
        mapping.inputs['Scale'].default_value = (0.1, 0.1, 0.1)

        gamma_node = nodes.new(type="ShaderNodeGamma")
        gamma_node.inputs[1].default_value = 3.7

        noise_node = nodes.new(type="ShaderNodeTexNoise")
        noise_node.inputs['Scale'].default_value = 10.0
        noise_node.inputs['Detail'].default_value = 15.0

        brightness_contrast = nodes.new(type="ShaderNodeBrightContrast")
        brightness_contrast.inputs["Bright"].default_value = 0.4
        brightness_contrast.inputs["Contrast"].default_value = 0.9

        map_range_node = nodes.new(type="ShaderNodeMapRange")
        map_range_node.data_type = 'FLOAT'
        map_range_node.interpolation_type = 'LINEAR'
        map_range_node.inputs['From Min'].default_value = 0.0
        map_range_node.inputs['From Max'].default_value = 0.1
        map_range_node.inputs['To Min'].default_value = 0.0
        map_range_node.inputs['To Max'].default_value = 1.0


        links.new(geometry_node.outputs["Pointiness"], color_ramp_mask.inputs["Fac"])
        links.new(color_ramp_mask.outputs["Color"], gamma_node.inputs['Color'])
        links.new(gamma_node.outputs["Color"], math_multiply.inputs[0])

        links.new(texture_coordinate.outputs["Normal"], mapping.inputs["Vector"])
        links.new(mapping.outputs['Vector'], noise_node.inputs['Vector'])
        links.new(noise_node.outputs['Fac'], math_multiply.inputs[1])

        links.new(math_multiply.outputs['Value'], map_range_node.inputs['Value'])
        links.new(map_range_node.outputs['Result'], brightness_contrast.inputs['Color'])
        links.new(brightness_contrast.outputs['Color'], color_ramp.inputs['Fac'])

        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        self.write_message("ColorMap=Deformation on Surface", True)


    def scalar_map_material(self):
        """
            Function: material to show better the scalar field values applied to the mesh

            Returns:
                bpy.ops.material

        """

        material = bpy.data.materials.new(name="Scalar Map")
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_two = nodes.new(type='ShaderNodeBsdfPrincipled')
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        attribute_node_scalar = nodes.new(type='ShaderNodeAttribute')
        attribute_node_labels = nodes.new(type='ShaderNodeAttribute')
        bump_node = nodes.new(type='ShaderNodeBump')
        bump_node_two = nodes.new(type='ShaderNodeBump')
        color_ramp_color = nodes.new(type='ShaderNodeValToRGB')
        color_ramp_mask = nodes.new(type='ShaderNodeValToRGB')
        color_ramp_two = nodes.new(type='ShaderNodeValToRGB')
        brightness_contrast = nodes.new(type="ShaderNodeBrightContrast")
        mapping_node = nodes.new(type='ShaderNodeMapping')
        noise_texture = nodes.new(type='ShaderNodeTexNoise')
        separate_rgb = nodes.new(type='ShaderNodeSeparateRGB')
        combine_rgb = nodes.new(type='ShaderNodeCombineRGB')
        rgb_curves = nodes.new(type='ShaderNodeRGBCurve')


        attribute_node_scalar.attribute_name = 'fmap_values'
        attribute_node_labels.attribute_name = 'labels_values'
        bump_node.inputs["Strength"].default_value = 0.88
        bump_node.inputs["Distance"].default_value = 1.0
        bump_node_two.inputs["Strength"].default_value = 0.2
        bump_node_two.inputs["Distance"].default_value = 1.0

        brightness_contrast.inputs["Bright"].default_value = 0.5
        brightness_contrast.inputs["Contrast"].default_value = 2.4

        self.add_color_to_color_ramp(color_ramp_color, 0.0, self.hex_color[0], is_black=True)
        self.add_color_to_color_ramp(color_ramp_color, 0.5, self.hex_color[1])
        self.add_color_to_color_ramp(color_ramp_color, 1.0, self.hex_color[2], is_white=True, flag=1)

        color_ramp_two.color_ramp.elements[0].position = 0.378
        color_ramp_two.color_ramp.elements[1].position = 0.738

        mix_shader.inputs["Fac"].default_value = self.mix_shader_fac
        noise_texture.inputs['Scale'].default_value = 19.0
        noise_texture.inputs['Detail'].default_value = 15.0
        noise_texture.inputs['Roughness'].default_value = 0.3

        curve = rgb_curves.mapping.curves[0]
        curve.points.new(0.556363, 0.46)
        curve = rgb_curves.mapping.curves[1]
        curve.points.new(0.563636, 0.52)
        curve = rgb_curves.mapping.curves[2]
        curve.points.new(0.0, 0.0)
        curve = rgb_curves.mapping.curves[3]
        curve.points.new(0.603636, 0.45)


        links.new(attribute_node_labels.outputs['Fac'], color_ramp_mask.inputs['Fac'])
        links.new(attribute_node_scalar.outputs['Fac'], color_ramp_color.inputs['Fac'])

        links.new(color_ramp_color.outputs['Color'], principled.inputs['Base Color'])
        links.new(color_ramp_mask.outputs['Color'], bump_node.inputs['Height'])
        links.new(bump_node.outputs['Normal'], principled.inputs['Normal'])

        links.new(principled.outputs['BSDF'], mix_shader.inputs[1])

        links.new(attribute_node_labels.outputs['Vector'], mapping_node.inputs['Vector'])
        links.new(mapping_node.outputs['Vector'], noise_texture.inputs['Vector'])
        links.new(noise_texture.outputs['Fac'], color_ramp_two.inputs['Fac'])
        links.new(noise_texture.outputs['Color'], separate_rgb.inputs[0])
        links.new(color_ramp_two.outputs['Color'], bump_node_two.inputs['Height'])
        links.new(bump_node_two.outputs['Normal'], principled_two.inputs['Normal'])
        links.new(separate_rgb.outputs['R'], combine_rgb.inputs['R'])
        links.new(separate_rgb.outputs['G'], combine_rgb.inputs['G'])
        links.new(separate_rgb.outputs['B'], combine_rgb.inputs['B'])
        links.new(combine_rgb.outputs[0], rgb_curves.inputs['Color'])
        links.new(rgb_curves.outputs['Color'], brightness_contrast.inputs['Color'])
        links.new(brightness_contrast.outputs['Color'], principled_two.inputs['Base Color'])

        links.new(principled_two.outputs['BSDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

        self.write_message("ColorMap=Scalar Map", True)

        return material


    def add_color_to_color_ramp(self, node, position, color, flag=None, is_black=False, is_white=False):
        """
            Function: add color to color-ramp

            Args:
                node : refers to the color ramp obj
                position : position of index-color
                color : hex value
                flag : Equal to None if two color are chosen, Not None if multiple colors are set up, change None with the number of colors added e.g. added 1 more color then flag = 1
                is_black : boolean value. Define if it is the Limit at the Left of the Ramp
                is_white : boolean value. Define if it is the Limit at the Right of the Ramp
        """


        if is_black:
            element = node.color_ramp.elements[0]
            element.position = position
        elif is_white:
            if flag is not None:
                element = node.color_ramp.elements[flag+1]
            else:
                element = node.color_ramp.elements[1]
            element.position = position
        else:
            element = node.color_ramp.elements.new(position)

        element.color = (*self.hex_to_rgb_color_ramp(color), 1)


    # Create a variable where to write the material that has been applied, in order to write it on the file
    def write_message(self, messaggio="None", type_value=True) -> None:
        """
            Function: write message about what materials the User choose

            Args:
                messaggio: msg to write
                type_value: bool, define the type of Material:
                    True: Mesh
                    False: Planes

            Returns:
                None

        """

        if type_value:
            self.message_material = "Material on Mesh chosen: " + messaggio + "\n"
        else:
            self.message_material += "Material Plane chosen: " + messaggio + "\n"


    # Get the message variable
    def get_message(self) -> str:
        """
            Function: fetch the msg

            Return:
                str
        """

        return self.message_material



    # Convert the HEX to RGB : due to some value-offset that BLENDER applies, the good offset value is: 2.26
    def hex_to_rgb(self, hex_color):
        """
            Function: convert HEX value to RGB

            Return
                float, float, float
        """

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
        """
            Function: convert HEX value to RBG for Color Ramp

            Returns:
                float, float, float
        """

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

