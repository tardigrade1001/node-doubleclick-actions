bl_info = {
    "name": "Node DoubleClick Actions",
    "author": "Community",
    "version": (1, 5, 0),
    "blender": (4, 0, 0),
    "location": "Node Editor",
    "description": "Double-click nodes to mute, double-click empty space to open search.",
    "category": "Interface",
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty


# -------------------------------------------------------------------
# Preferences
# -------------------------------------------------------------------

class NODE_DOUBLECLICK_Prefs(AddonPreferences):
    bl_idname = __package__ if __package__ else __name__

    enable_mute: BoolProperty(
        name="Double-Click to Mute Nodes",
        default=True,
    )

    enable_search: BoolProperty(
        name="Double-Click Empty Space to Search",
        default=True,
    )

    enable_debug: BoolProperty(
        name="Enable Debug Logging",
        description="Print debug messages to the system console",
        default=False,
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Node Editor Behavior", icon='NODETREE')
        box.prop(self, "enable_mute", icon='MUTE_IPO_OFF')
        box.prop(self, "enable_search", icon='VIEWZOOM')

        box = layout.box()
        box.label(text="Debug", icon='CONSOLE')
        box.prop(self, "enable_debug")


def get_prefs():
    addon_id = __package__ if __package__ else __name__
    addon = bpy.context.preferences.addons.get(addon_id)
    return addon.preferences if addon else None


def debug_print(*args):
    prefs = get_prefs()
    if prefs and prefs.enable_debug:
        print("[Node DoubleClick]", *args)


# -------------------------------------------------------------------
# Safe Node Search Invocation (Blender 5.1 proof)
# -------------------------------------------------------------------

def invoke_node_search():
    """
    Safely invoke node search across Blender 4.x – 5.1.
    """
    try:
        debug_print("Trying bpy.ops.node.add_search")
        return bpy.ops.node.add_search('INVOKE_DEFAULT')
    except Exception as e:
        debug_print("node.add_search failed:", repr(e))

    try:
        debug_print("Falling back to bpy.ops.wm.search_menu")
        return bpy.ops.wm.search_menu('INVOKE_DEFAULT')
    except Exception as e:
        debug_print("wm.search_menu failed:", repr(e))

    debug_print("No valid search operator available")
    return {'PASS_THROUGH'}


# -------------------------------------------------------------------
# Operator
# -------------------------------------------------------------------

class NODE_OT_doubleclick(Operator):
    """Node Editor Double Click"""
    bl_idname = "node.doubleclick_actions"
    bl_label = "Node Double Click Actions"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        # ---- Context guard ----
        if not context.area or context.area.type != 'NODE_EDITOR':
            debug_print("Not in Node Editor, passing through")
            return {'PASS_THROUGH'}

        prefs = get_prefs()
        if not prefs:
            debug_print("Preferences not found")
            return {'PASS_THROUGH'}

        space = context.space_data

        # --------------------------------------------------
        # Case 1: No node tree → global search only
        # --------------------------------------------------
        if not space or not space.node_tree:
            debug_print("No node tree detected")
            if prefs.enable_search:
                return invoke_node_search()
            return {'PASS_THROUGH'}

        # --------------------------------------------------
        # Case 2: Node muting
        # --------------------------------------------------
        active = context.active_node
        node_clicked = bool(active and active.select)

        if prefs.enable_mute and node_clicked:
            if getattr(active, "type", None) != 'FRAME':
                try:
                    active.mute = not active.mute
                    debug_print("Toggled mute on node:", active.name)
                    return {'FINISHED'}
                except Exception as e:
                    debug_print("Failed to toggle mute:", repr(e))
                    return {'PASS_THROUGH'}

        # --------------------------------------------------
        # Case 3: Empty space → search
        # --------------------------------------------------
        if prefs.enable_search:
            debug_print("Empty space double-click → search")
            return invoke_node_search()

        return {'PASS_THROUGH'}


# -------------------------------------------------------------------
# Registration
# -------------------------------------------------------------------

classes = (
    NODE_DOUBLECLICK_Prefs,
    NODE_OT_doubleclick,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(
            name='Node Editor',
            space_type='NODE_EDITOR'
        )
        kmi = km.keymap_items.new(
            NODE_OT_doubleclick.bl_idname,
            'LEFTMOUSE',
            'DOUBLE_CLICK'
        )
        addon_keymaps.append((km, kmi))

    debug_print("Addon registered")


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    debug_print("Addon unregistered")


if __name__ == "__main__":
    register()
