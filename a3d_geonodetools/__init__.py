# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "A3D GeoNodeTools",
    "author" : "Ashlee3Dee", 
    "description" : "",
    "blender" : (3, 6, 1),
    "version" : (0, 0, 1),
    "location" : "Geometry Nodes Editor N Panel",
    "warning" : "",
    "doc_url": "https://github.com/ashlee3dee/a3d-b3d-tools/", 
    "tracker_url": "", 
    "category" : "User Interface" 
}


import bpy
import bpy.utils.previews


addon_keymaps = {}
_icons = None
class SNA_OT_Hideunusedinputs_F3533(bpy.types.Operator):
    bl_idname = "sna.hideunusedinputs_f3533"
    bl_label = "HideUnusedInputs"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        for i_F6F00 in range(len(bpy.context.active_object.modifiers.active.node_group.nodes)):
            if (bpy.context.active_object.modifiers.active.node_group.nodes[i_F6F00].type == 'GROUP_INPUT'):
                bpy.context.active_object.modifiers.active.node_group.nodes[i_F6F00].select = True
        prev_context = bpy.context.area.type
        bpy.context.area.type = 'NODE_EDITOR'
        bpy.ops.node.hide_socket_toggle('INVOKE_DEFAULT', )
        bpy.context.area.type = prev_context
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_TOOLS_93655(bpy.types.Panel):
    bl_label = 'Tools'
    bl_idname = 'SNA_PT_TOOLS_93655'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'A3D NodeTools'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((bpy.context.area.ui_type != 'GeometryNodeTree'))

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.hideunusedinputs_f3533', text='Toggle Unused Inputs', icon_value=254, emboss=True, depress=False)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_OT_Hideunusedinputs_F3533)
    bpy.utils.register_class(SNA_PT_TOOLS_93655)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_OT_Hideunusedinputs_F3533)
    bpy.utils.unregister_class(SNA_PT_TOOLS_93655)
