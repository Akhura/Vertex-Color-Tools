# Vertex-Color-Tools
Tool for convenient assigning vertex colors to mesh faces

This simple tool allows assigning vertex color and alpha values to selected faces directly in Edit Mode, as well as change the order Vertex Color Layers. Works in blender 2.80+

Update 11.06.2022: Uploaded Vertex_Color_Tools_v1.5. Due to recent changed in Blender's 3.2.0 API, there are 4 types of vertex colors: 2 variations for color_depth (8-bit and 32-bit float) and 2 geometry domains of vertex color existence (the most relevant part of the change). As for now, you can still tweak the vertex color list order of the same geometry domain, i.e if there 2 "Face Corner" type layers, they can swap their position on the list, while of there are 2 layers of different geometry domains "Face Cornere" and "Vertex" - there will be an INFO message that layers of different type..and another workaround for this issue is still undergoes some thinking, alas. But there is a way to convert one geometry domain data to another, but not in code yet.

Installation process is standard:
1. Launch Blender.
2. Edit -> Preferences -> Add-ons -> Install.
3. Locate the downloaded file of the add-on, select it and press "Install Add-on".
4. As soon as it appears in the add-on stack, tick the box to "Enable Add-on".It is located in the 3D Viewport, while in Edit Mode, open the N-Panel, and you shall find it in "Tool" Tab -> "Vertex Color Assign" Panel.
5. Verex Color Layer Reordering is in the Object Data Properties section, under Vertex Colors Layer.

In order to see changes as_you_go - switch the shading mode to "Vertex" in the top right drop down Shading Properties Menu.

Download link:
https://github.com/Akhura/Vertex-Color-Tool-for-Edit-Mode/archive/refs/heads/main.zip
