bl_info = {
    "name": "Animation Tool",
    "author": "Abdullah Khan",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import os
import json
import bpy
import requests
import pathlib

class OBJECT_PT_AnimateTool(bpy.types.Panel):
   
    bl_label = "Animation Tool"
    bl_idname = "OBJECT_PT_AnimateTool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "nAnimation Tool"

    def draw(self, context):
        layout = self.layout


        row = layout.row()
        row.operator("wm.textop")


class WM_OT_textOp(bpy.types.Operator):
    bl_label = "Animation Tool"
    bl_idname = "wm.textop"
    start_frame : bpy.props.IntProperty(name= "Start Frames:")
    seed_frames : bpy.props.IntProperty(name= "# Seed Frames to use:")
    target_frame : bpy.props.IntProperty(name= "Target Frame:")
    
    
    def execute(self,context):
        save_path = os.path.join(str(pathlib.Path(__file__).parent.parent.resolve()), 'test.bvh')
    
        # TODO: Check if seed, and target frames are valid with start frame    
        if self.target_frame != 0 and self.seed_frames != 0 and self.target_frame > self.seed_frames:
            print(f"cwd:{save_path}")
            print(f"seed frames: {self.seed_frames}")
            print(f"target frame: {self.target_frame}")
            bpy.ops.export_anim.bvh(filepath=save_path, check_existing=True, 
                filter_glob='*.bvh', root_transform_only=True,
                frame_start=self.start_frame,
                frame_end=self.target_frame,
                rotate_mode='YZX'
                )
            
            print("Uploading to server...")
            file = {'file': open(save_path, 'rb')}
            response = requests.post('http://localhost:8000/upload', files=file)
            filename = os.path.join("uploads", json.loads(response.text)["filename"])
            response = requests.post('http://localhost:8000/motion-generation-model/inference', json.dumps({"filename": filename, "seed_frames": self.seed_frames}))
            
            print(response.text)
                    
        
        return {'FINISHED'}
    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OBJECT_PT_AnimateTool)
    bpy.utils.register_class(WM_OT_textOp)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_AnimateTool)
    bpy.utils.unregister_class(WM_OT_textOp)


if __name__ == "__main__":
    register()
