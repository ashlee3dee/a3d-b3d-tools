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
    "name": "A3D View Non-Manifold Edges",
    "author": "Ashlee3Dee",
    "description": "Adds Viewport Overlay for Non-Manifold Edges",
    "blender": (3, 6, 1),
    "version": (0, 0, 2),
    "location": "3D View > Header > Overlays > Non-Manifold Edges",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/ashlee3dee/a3d-b3d-tools",
    "category": "3D View"
}


import bpy
import bpy.utils.previews
import bmesh
import gpu
from gpu_extras.batch import batch_for_shader


addon_keymaps = {}
_icons = None
handler_7268F = []


def sna_update_sna_show_1914A(self, context):
    sna_updated_prop = self.sna_show
    prev_context = bpy.context.area.type
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.sna.toggledraw_a5ef8('INVOKE_DEFAULT', )
    bpy.context.area.type = prev_context


class SNA_OT_Toggledraw_A5Ef8(bpy.types.Operator):
    bl_idname = "sna.toggledraw_a5ef8"
    bl_label = "ToggleDraw"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_show:
            handler_7268F.append(bpy.types.SpaceView3D.draw_handler_add(
                sna_drawnonmanifoldedges_534D5, (), 'WINDOW', 'POST_VIEW'))
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        elif handler_7268F:
            bpy.types.SpaceView3D.draw_handler_remove(handler_7268F[0], 'WINDOW')
            handler_7268F.pop(0)
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_to_view3d_pt_overlay_geometry_E729E(self, context):
    layout = self.layout
    layout.label(text='Non-Manifold Edges', icon_value=0)
    layout.prop(bpy.context.scene, 'sna_show', text='Show', icon_value=0, emboss=True)
    layout.prop(bpy.context.scene, 'sna_viewwidth', text='Width', icon_value=0, emboss=True)
    layout.prop(bpy.context.scene, 'sna_viewcolor', text='Color', icon_value=0, emboss=True)


def sna_drawnonmanifoldedges_534D5():
    if not bpy.context.area.spaces[0].overlay.show_overlays:
        return
    bm_68E55 = bmesh.new()
    if bpy.context.view_layer.objects.active:
        if bpy.context.view_layer.objects.active.mode == 'EDIT':
            bm_68E55 = bmesh.from_edit_mesh(bpy.context.view_layer.objects.active.data)
        else:
            bm_68E55.from_mesh(bpy.context.view_layer.objects.active.data)
    bm_68E55.transform(bpy.context.view_layer.objects.active.matrix_world)
    bm_68E55.verts.ensure_lookup_table()
    bm_68E55.faces.ensure_lookup_table()
    bm_68E55.edges.ensure_lookup_table()
    for i_89534 in range(len(bm_68E55.edges)):
        if not bm_68E55.edges[i_89534].is_manifold:
            lines = [(bm_68E55.edges[i_89534].verts[0].co, bm_68E55.edges[i_89534].verts[1].co)]
            coords = []
            indices = []
            for i, line in enumerate(lines):
                coords.extend(line)
                indices.append((i * 2, i * 2 + 1))
            shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
            batch = batch_for_shader(shader, 'LINES', {"pos": coords}, indices=tuple(indices))
            shader.bind()
            shader.uniform_float("color", bpy.context.scene.sna_viewcolor)
            gpu.state.line_width_set(bpy.context.scene.sna_viewwidth)
            gpu.state.depth_test_set('LESS_EQUAL')
            gpu.state.depth_mask_set(True)
            gpu.state.blend_set('ALPHA')
            batch.draw(shader)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_viewcolor = bpy.props.FloatVectorProperty(
        name='ViewColor', description='', size=4, default=(
            0.0, 1.0, 0.0, 1.0), subtype='COLOR', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_viewwidth = bpy.props.IntProperty(name='ViewWidth', description='', default=0, subtype='NONE')
    bpy.types.Scene.sna_show = bpy.props.BoolProperty(
        name='Show', description='', default=False, update=sna_update_sna_show_1914A)
    bpy.utils.register_class(SNA_OT_Toggledraw_A5Ef8)
    bpy.types.VIEW3D_PT_overlay_geometry.append(sna_add_to_view3d_pt_overlay_geometry_E729E)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_show
    del bpy.types.Scene.sna_viewwidth
    del bpy.types.Scene.sna_viewcolor
    bpy.utils.unregister_class(SNA_OT_Toggledraw_A5Ef8)
    if handler_7268F:
        bpy.types.SpaceView3D.draw_handler_remove(handler_7268F[0], 'WINDOW')
        handler_7268F.pop(0)
    bpy.types.VIEW3D_PT_overlay_geometry.remove(sna_add_to_view3d_pt_overlay_geometry_E729E)
