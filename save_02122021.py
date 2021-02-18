bl_info = {
    "name": "Face counter",
    "description": "Counts the amount of face each object has and prints it into a message box",
    "author": "mirkan1",
    "category": "3D View",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }
    
import bpy
arr = []
# for i in bpy.data.materials: i


def take_second(elem):
    return elem[1]

def fece_count():
    objects = bpy.data.scenes[0].objects
    arr = []
    for i in objects:
        data = i.data
        try:
            arr.append([f'{data.name}', len(data.polygons)])
            # print(f'object {data.name} has {len(data.polygons)} faces')
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


class Qury_Props(bpy.types.PropertyGroup):
    pr_enums: bpy.props.EnumProperty(
        name="Texture Resolation", 
        description="Pick desired resoliton to resize", 
        items = [
            ("8192", "8192", "Decrease texture resolation to 8192 pixels"),
            ("4096", "4096", "Decrease texture resolation to 4096 pixels"),
            ("2048", "2048", "Decrease texture resolation to 2048 pixels"),
            ("1024", "1024", "Decrease texture resolation to 1024 pixels"),
            ("512", "512", "Decrease texture resolation to 512 pixels"),
            ("256", "256", "Decrease texture resolation to 256 pixels"),
            ("128", "128", "Decrease texture resolation to 128 pixels"),
            ("64", "64", "Decrease texture resolation to 64 pixels"),
        ]
    )
    
## Property group for holding previous image data
class ImageDataCopy(bpy.types.PropertyGroup):
    object : bpy.props.PointerProperty(type=bpy.types.Image)

    def mama(self):
        print("mama")
        return True
    
    def copy(self):
        self.object = self.id_data.copy()
        self.name = self.object.name
        return self.object

    def add(self, ob):
        print("add", self, ob)
        self.object = ob
        self.name = ob.name
        return self.object
    
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
        props = bpy.context.scene.Qury_Props
        
        # EXECUTE BUTTON
        row = layout.row()
        #row.label(text="Face Count")
        row.operator("object.ratio_save_button", text="Face Counts")
        
        # Image Resise
        row = layout.row()
        row = layout.row()
        row.label(text="Texture Limit")
        row.prop(props, "pr_enums", text="")
        row = layout.row()
        row.label(text="Resize Function")
        row.operator("object.image_resise", text="Resize")
        
        # Previos Image Get
        #row.label(text="Previous Size")
        row = layout.row()
        row = layout.row()
        row.operator("object.return_prev_image", text="Get Previous Texture Back")
                
# EXECUTER BUTTON               
class executeButton(bpy.types.Operator):
    bl_idname = "object.ratio_save_button"
    bl_label = "Ratio and savebutton functions"

    def execute(self, context):
        arr = fece_count()
        ShowMessageBox(arr) 
        return {'FINISHED'}  

# Image Resise               
class ImageResise(bpy.types.Operator):
    bl_idname = "object.image_resise"
    bl_label = "resize an image and save its value for a further call"

    def execute(self, context):
        props = bpy.context.scene.Qury_Props
        res_ = int(props.pr_enums)
        object = bpy.context.active_object
        objects = bpy.context.selected_objects
        for j in objects:
            mat = j.active_material
            try:
                node_tree = mat.node_tree
                nodes = node_tree.nodes
            except (NameError, AttributeError):
                 # NoneType error
                pass
            # 'bpy.types.ShaderNodeTexImage'
            for i in nodes: 
                tur = str(type(i))
                if tur == "<class 'bpy.types.ShaderNodeTexImage'>":
                    image = i.image
                    if image.generated_width + image.generated_height  < res_ + res_:
                        self.report({"ERROR"}, "Selected object(s)'s dimension is lesser than given texture size")
                        return {'CANCELLED'} 
                    if len(i.image.copies) < 1:
                        # creating same image inside the image if not exist
                        i.image.copies.add().copy()
                    image.generated_width = res_
                    image.generated_height = res_
                    image.scale(res_, res_)
        return {'FINISHED'}  
    
class GetPreviousImage_OP(bpy.types.Operator):
    bl_idname = "object.return_prev_image"
    bl_label = "checks if image is previously worked, if so changing its values back to the previous one"
    
    def execute(self, context):
        #objects = bpy.data.scenes[0].objects
        object = bpy.context.active_object
        objects = bpy.context.selected_objects
        for j in objects:        
            mat = j.active_material
            try:
                node_tree = mat.node_tree
                nodes = node_tree.nodes
            except (NameError, AttributeError):
                # NoneType error
                pass
            # 'bpy.types.ShaderNodeTexImage'
            for i in nodes: 
                tur = str(type(i))
                if tur == "<class 'bpy.types.ShaderNodeTexImage'>":
                    image = i.image
                    try:
                        prev_data = i.image.copies[-1].object.copy()
                        prev_data.pack()
                        prev_data.save()
                        split_ = i.image.copies[-1].object.name[:-4].split(".")
                        path_ = prev_data.filepath.split("\\")
                        path_ = "\\".join(path_[:-1]+[""])
                        prev_data.filepath = path_ + split_[0] + "_." + split_[1]
                        prev_data.save()
                        i.image = prev_data
                        i.image.copies.clear()
                        # print(len(i.image.copies))
                        # bpy.data.images.remove(image)
                    except IndexError:
                        # wrong object selected // pass it
                        pass
        return {'FINISHED'} 
    
classes = (
    executeButton,
    MessageBoxOperator,
    ImageResise,
    ImageDataCopy,
    GetPreviousImage_OP,
    Qury_Props,
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
    # Register QueryProps
    bpy.types.Image.copies = bpy.props.CollectionProperty(type=ImageDataCopy)
    bpy.types.Scene.Qury_Props = bpy.props.PointerProperty(type=Qury_Props)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    del(bpy.types.Image.copies)

if __name__ == "__main__":
    register();
    
    
# img = bpy.data.images["Tiles48_diffuse_xtm.jpg"]
# img.scale(128, 128)
# img.save()
# img.scale(12800, 12800)
# img.save()
# img = bpy.data.images["Tiles47_diffuse_xtm.jpg"]
# img.scale[0] # X
# img.scale[1] # Y
# save those values then use for backup