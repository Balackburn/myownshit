import sand3d as s3d


def screw():
    shaft = s3d.at(threaded_shaft(), x=122.5, y=75.69, z=5.484)
    shank = s3d.at(smooth_shank(), x=122.5, y=118.19, z=5.984)
    return s3d.assembly("screw", shaft, shank)


def threaded_shaft(diameter=5, length=67, pitch=2.35, tip_length=6):
    ridge = s3d.thread("spiral", d=diameter, length=length, pitch=pitch)
    envelope = s3d.revolve("point_envelope", s3d.poly([(0,0), (diameter/20,0), (diameter/2,tip_length), (diameter/2,length), (0,length)]))
    solid = s3d.intersect(ridge, envelope)
    solid = s3d.at(solid, rx=-90, y=-length/2, z=diameter/2)
    s3d.material(solid, "steel", color="#888888")
    return s3d.group("threaded_shaft", solid)


def smooth_shank(diameter=4, length=19):
    solid = s3d.at(s3d.cylinder("shank", d=diameter, h=length), rx=-90, y=-length/2, z=diameter/2)
    s3d.material(solid, "steel", color="#888888")
    head = s3d.at(flared_head(), y=11.5, z=-2.041)
    return s3d.group("smooth_shank", solid, head)


def flared_head(diameter=8.082, length=5, neck=4, rim=0.5):
    solid = s3d.revolve("head", s3d.poly([(0,0), (neck/2,0), (neck/2,length/5), s3d.spline([(neck/2,length/5), (neck/2+0.2,length/2), (diameter/2,length-rim)]), (diameter/2,length), (0,length)]))
    solid = s3d.at(solid, rx=-90, y=-length/2, z=diameter/2)
    s3d.material(solid, "steel", color="#888888")
    return s3d.group("flared_head", solid)
