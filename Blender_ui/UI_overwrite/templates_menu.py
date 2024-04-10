import bpy
from bpy.types import Menu
# il faut créer le dosser blender/4.0/script/template_cl et
# Il faut placer les template dans le dossier blender/4.0/script/template_cl

class TEXT_MT_templates_cl(Menu):
    bl_label = "Open Computing Language"

    def draw(self, _context):
        self.path_menu(
            bpy.utils.script_paths(subdir="templates_cl"),
            "text.open",
            props_default={"internal": True},
            filter_ext=lambda ext: (ext.lower() == ".cl"),
        )


class TEXT_MT_templates(Menu):
    bl_label = "Templates"

    def draw(self, _context):
        layout = self.layout
        layout.menu("TEXT_MT_templates_py")
        layout.menu("TEXT_MT_templates_osl")
        layout.menu("TEXT_MT_templates_cl")

def register():
    pass

def unregister():
    pass

