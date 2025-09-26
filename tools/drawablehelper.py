import bpy
from mathutils import Vector
from ..sollumz_properties import SollumType, LODLevel, SollumzGame
from ..tools.blenderhelper import create_empty_object
from ..cwxml.drawable import BonePropertiesManager, Drawable, DrawableModel


def set_recommended_bone_properties(bone):
    bone_item = BonePropertiesManager.bones.get(bone.name)
    if bone_item is None:
        return

    bone.bone_properties.tag = bone_item.tag
    bone.bone_properties.flags.clear()
    flags_restricted = set(["LimitRotation", "Unk0"])
    for flag_name in bone_item.flags:
        if flag_name in flags_restricted:
            continue

        flag = bone.bone_properties.flags.add()
        flag.name = flag_name


def convert_obj_to_drawable(obj: bpy.types.Object, sollum_game_type: SollumzGame):
    drawable_obj = create_empty_object(SollumType.DRAWABLE)
    drawable_obj.location = obj.location
    drawable_obj.rotation_mode = obj.rotation_mode
    drawable_obj.rotation_euler = obj.rotation_euler
    drawable_obj.rotation_quaternion = obj.rotation_quaternion
    drawable_obj.rotation_axis_angle = obj.rotation_axis_angle

    obj_name = obj.name

    convert_obj_to_model(obj, sollum_game_type)
    obj.name = f"{obj.name}.model"
    # Set drawable obj name after converting obj to a model to avoid .00# suffix
    drawable_obj.name = obj_name
    drawable_obj.sollum_game_type = sollum_game_type

    drawable_obj.parent = obj.parent
    obj.parent = drawable_obj
    obj.location = Vector()
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
    obj.rotation_axis_angle = (0.0, 0.0, 1.0, 0.0)

    return drawable_obj


def convert_objs_to_single_drawable(objs: list[bpy.types.Object], sollum_game_type: SollumzGame):
    drawable_obj = create_empty_object(SollumType.DRAWABLE)
    drawable_obj.sollum_game_type = sollum_game_type

    for obj in objs:
        convert_obj_to_model(obj, sollum_game_type)
        obj.name = f"{obj.name}.model"
        obj.parent = drawable_obj

    return drawable_obj


def convert_obj_to_model(obj: bpy.types.Object, sollum_game_type: SollumzGame):
    obj.sollum_type = SollumType.DRAWABLE_MODEL
    obj.sollum_game_type = sollum_game_type
    obj.sz_lods.get_lod(LODLevel.HIGH).mesh = obj.data
    obj.sz_lods.active_lod_level = LODLevel.HIGH


def center_drawable_to_models(drawable_obj: bpy.types.Object):
    model_objs = [
        child for child in drawable_obj.children if child.sollum_type == SollumType.DRAWABLE_MODEL]

    center = Vector()

    for obj in model_objs:
        center += obj.location

    center /= len(model_objs)

    drawable_obj.location = center

    for obj in model_objs:
        obj.location -= center


def get_model_xmls_by_lod(drawable_xml: Drawable) -> dict[LODLevel, DrawableModel]:
    return {
        LODLevel.VERYHIGH: drawable_xml.hi_models,
        LODLevel.HIGH: drawable_xml.drawable_models_high,
        LODLevel.MEDIUM: drawable_xml.drawable_models_med,
        LODLevel.LOW: drawable_xml.drawable_models_low,
        LODLevel.VERYLOW: drawable_xml.drawable_models_vlow,
    }
