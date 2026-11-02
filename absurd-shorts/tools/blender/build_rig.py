"""Turn the exported GLB (joint empties + rigid meshes + baked clips) into a reusable Blender
character: a real armature, meshes rigidly parented to bones, every clip baked as an Action.

  blender -b --python tools/blender/build_rig.py -- models/humans/lemec.glb models/blender/lemec.blend [--render out/turnaround.png]

The rig is rigid (no skin weights) on purpose: the source style is a box puppet whose limbs never deform.
Clips are stored as Actions with fake users (Action editor / NLA → pick e.g. "LeMec_run").
"""
import bpy, sys, math
from mathutils import Vector, Matrix, Quaternion

argv = sys.argv[sys.argv.index('--') + 1:]
GLB, OUT = argv[0], argv[1]
RENDER = argv[argv.index('--render') + 1] if '--render' in argv else None
NAME = 'LeMec'

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
scene = bpy.context.scene

JOINTS = ['hips', 'torso', 'neck', 'head', 'shoulderL', 'elbowL', 'handL', 'shoulderR', 'elbowR', 'handR',
          'hipL', 'kneeL', 'footL', 'hipR', 'kneeR', 'footR']
TAIL_CHILD = {'torso': 'neck', 'neck': 'head', 'shoulderL': 'elbowL', 'elbowL': 'handL', 'shoulderR': 'elbowR',
              'elbowR': 'handR', 'hipL': 'kneeL', 'kneeL': 'footL', 'hipR': 'kneeR', 'kneeR': 'footR'}
TAIL_OFFSET = {'hips': Vector((0, 0, 0.12)), 'head': Vector((0, 0, 0.6)), 'handL': Vector((0, 0, -0.13)),
               'handR': Vector((0, 0, -0.13)), 'footL': Vector((0, -0.2, 0)), 'footR': Vector((0, -0.2, 0))}
emp = {j: bpy.data.objects[j] for j in JOINTS}
root = emp['hips'].parent

# --- 1. rest pose: strip animation, zero rotations, read world positions ---------------
clips = sorted({a.name.rsplit('_', 1)[0] for a in bpy.data.actions})
for o in emp.values():
    if o.animation_data:
        o.animation_data.action = None
        for tr in list(o.animation_data.nla_tracks): o.animation_data.nla_tracks.remove(tr)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Quaternion()
rest_loc = {j: Vector(emp[j].location) for j in JOINTS}
bpy.context.view_layer.update()
world = {j: emp[j].matrix_world.translation.copy() for j in JOINTS}

# --- 2. armature -------------------------------------------------------------------------------
arm_data = bpy.data.armatures.new(NAME + '_Armature'); arm_data.display_type = 'STICK'
arm = bpy.data.objects.new(NAME + '_Rig', arm_data); scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
eb = {}
for j in JOINTS:
    b = arm_data.edit_bones.new(j); b.head = world[j]
    b.tail = world[TAIL_CHILD[j]] if j in TAIL_CHILD else world[j] + TAIL_OFFSET[j]
    if (b.tail - b.head).length < 1e-3: b.tail = b.head + Vector((0, 0, 0.1))
    eb[j] = b
for j in JOINTS:
    p = emp[j].parent.name
    if p in eb: eb[j].parent = eb[p]; eb[j].use_connect = False
bpy.ops.object.mode_set(mode='OBJECT')
rest_rot = {j: arm.data.bones[j].matrix_local.to_quaternion() for j in JOINTS}

# --- 3. reparent meshes rigidly to bones ------------------------------------------------------
def joint_of(o):
    p = o.parent
    while p is not None and p.name not in emp: p = p.parent
    return p.name if p else 'hips'
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
mw = {o.name: o.matrix_world.copy() for o in meshes}
for o in meshes:
    if o.parent and o.parent.type == 'MESH': continue  # child meshes (outline-like sub parts) follow their parent mesh
    j = joint_of(o); o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = j
for o in meshes:
    if o.parent == arm: o.matrix_world = mw[o.name]
bpy.context.view_layer.update()

# --- 4. bake every clip into an armature Action -------------------------------------------------
fps = 30; scene.render.fps = fps
arm.animation_data_create()
for clip in clips:
    acts = {j: bpy.data.actions.get(f'{clip}_{j}') for j in JOINTS}
    if not any(acts.values()): continue
    act = bpy.data.actions.new(f'{NAME}_{clip}'); act.use_fake_user = True
    arm.animation_data.action = act
    fr = max(int(a.frame_range[1]) for a in acts.values() if a)
    for f in range(0, fr + 1):
        for j in JOINTS:
            a = acts[j]; pb = arm.pose.bones[j]; pb.rotation_mode = 'QUATERNION'
            q = Quaternion()
            if a:
                comps = [fc for fc in a.fcurves if fc.data_path == 'rotation_quaternion']
                if len(comps) == 4:
                    comps.sort(key=lambda fc: fc.array_index); q = Quaternion([fc.evaluate(f) for fc in comps])
                locs = [fc for fc in a.fcurves if fc.data_path == 'location']
                if j == 'hips' and len(locs) == 3:
                    locs.sort(key=lambda fc: fc.array_index)
                    delta = Vector([fc.evaluate(f) for fc in locs]) - rest_loc['hips']  # parent (root) space == armature space
                    pb.location = rest_rot[j].inverted() @ delta; pb.keyframe_insert('location', frame=f)
            # joint-local rotation (empty frame == armature axes at rest) -> bone rest frame
            pb.rotation_quaternion = rest_rot[j].inverted() @ q @ rest_rot[j]
            pb.keyframe_insert('rotation_quaternion', frame=f)
    act.frame_range = (0, fr)
arm.animation_data.action = bpy.data.actions.get(f'{NAME}_idle')

# --- 5. clean up: remove empties and imported per-node actions ---------------------------------
for a in [a for a in bpy.data.actions if not a.name.startswith(NAME + '_')]: bpy.data.actions.remove(a)
for o in list(emp.values()): bpy.data.objects.remove(o)
if root and root.name in bpy.data.objects: bpy.data.objects.remove(root)
col = bpy.data.collections.new(NAME); scene.collection.children.link(col)
for o in [arm] + [o for o in bpy.data.objects if o.type == 'MESH']:
    for c in o.users_collection: c.objects.unlink(o)
    col.objects.link(o)
arm['source'] = 'absurd-shorts engine/human.js preset lemec'
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('SAVED', OUT, 'clips:', len([a for a in bpy.data.actions if a.name.startswith(NAME)]))

# --- 6. optional turnaround render (Cycles CPU, flat-ish look) ------------------------------------
if RENDER:
    arm.animation_data.action = None
    for pb in arm.pose.bones: pb.rotation_quaternion = Quaternion(); pb.location = Vector()
    scene.render.engine = 'CYCLES'; scene.cycles.samples = 48; scene.cycles.device = 'CPU'; scene.cycles.use_denoising = False
    scene.render.resolution_x, scene.render.resolution_y = 1600, 900
    scene.render.film_transparent = False
    w = bpy.data.worlds.new('W'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.86, 0.83, 0.78, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 1.0; scene.world = w
    bpy.ops.mesh.primitive_plane_add(size=40); floor = bpy.context.active_object
    fm = bpy.data.materials.new('floor'); fm.diffuse_color = (0.8, 0.77, 0.72, 1); fm.use_nodes = True
    fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.8, 0.77, 0.72, 1); floor.data.materials.append(fm)
    sun = bpy.data.objects.new('Key', bpy.data.lights.new('Key', 'SUN')); sun.data.energy = 2.2; sun.data.angle = 0.35
    sun.rotation_euler = (math.radians(50), 0, math.radians(30)); scene.collection.objects.link(sun)
    # five copies at 0/35/90/145/180 degrees, like the character sheet
    objs = [o for o in col.objects]
    for i, ang in enumerate([0, 35, 90, 145, 180]):
        if i == 0: grp = objs; rig = arm
        else:
            rig = arm.copy(); rig.data = arm.data; scene.collection.objects.link(rig)
            for o in objs:
                if o.type == 'MESH' and o.parent == arm:
                    c = o.copy(); c.parent = rig; scene.collection.objects.link(c)
        rig.location.x = (i - 2) * 1.0; rig.rotation_euler.z = math.radians(ang)  # glTF +Z (front) == Blender -Y
    cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); scene.collection.objects.link(cam); scene.camera = cam
    cam.location = (0, -9.5, 1.45); cam.rotation_euler = (math.radians(88), 0, 0); cam.data.lens = 50
    scene.render.filepath = RENDER; bpy.ops.render.render(write_still=True); print('RENDERED', RENDER)
