bl_info = {
    "name": "Face counter",
    "description": "Counts the amount of face each object has and prints it into a message box",
    "author": "mirkan1",
    "category": "3D View",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    #"warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }
    
import bpy
arr = []
# for i in bpy.data.materials: i

def take_second(elem):
    return elem[1]

def fece_count(message = "", title = "FACE COUNT", icon = 'INFO'):
    objects = bpy.data.scenes[0].objects
    arr = []
    len_arr = []
    for i in objects:
        data = i.data
        try:
            arr.append([f'{data.name}', len(data.polygons)])
            print(f'object {data.name} has {len(data.polygons)} faces')
        except AttributeError:
            pass
    arr = sorted(arr, key=take_second, reverse=True)
    arr = [f'{i[0]}: {i[1]}' for i in arr]
    return arr

#for i in objects:
#    data = i.data
#    for j in data.materials:
#        print(j)
#        arr.append(j)    

def ShowMessageBox(messages, title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for n in messages:
            self.layout.label(text=n)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GUI
class MessageBoxOperator(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Face count'
    bl_options = {'HIDE_HEADER'}
    bl_idname = "ui.show_message_box"
    bl_label = "Minimal Operator"

    def draw(self, context):
        layout = self.layout
        
        # EXECUTE BUTTON
        row = layout.row()
        row.operator("object.ratio_save_button", text="Execute")
        
# EXECUTER BUTTON               
class executeButton(bpy.types.Operator):
    bl_idname = "object.ratio_save_button"
    bl_label = "Ratio and savebutton functions"

    def execute(self, context):
        arr = fece_count()
        ShowMessageBox(arr) 
        return {'FINISHED'}  

classes = (
    executeButton,
    MessageBoxOperator,
)
addon_keymaps = [] 

def register():
    from bpy.utils import register_class
    # register_class(MessageBoxOperator)
    for cls in classes:
        register_class(cls)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(executeButton.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Screen Editing', space_type='EMPTY')
        kmi = km.keymap_items.new(executeButton.bl_idname, 'Q', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

if __name__ == "__main__":
    register();