import sand3d as s3d


def key():
    head = s3d.at(circular_head(), x=-0.1534, y=0.21, z=-0.8327)
    return s3d.assembly("key", head)


def circular_head(d=27.64, h=1.757, bore=9.5):
    head = s3d.cylinder("head", d=d, h=h)
    head = s3d.hole(head, d=bore)
    s3d.material(head, kind="painted_metal", color="#64130d")
    stem = s3d.at(blade(), x=0.1534, y=-28.91, z=0)
    return s3d.group("circular_head", head, stem)


def blade(h=1.757, half=4.8, shoulder=5.8, top=17.2, step=8.7, bottom=-17.27):
    outline = s3d.poly([(-shoulder,top),(half,top),(half,step),(half-1,step),(half-1,2),(half-2,-0.5),(half-1,-2),(half-1,-5),(half-2,-6.3),(half-1,-8),(half-1,bottom+2),(half-3,bottom),(-half+2,bottom),(-half,bottom+2),(-half,step),(-shoulder,step+1)])
    solid = s3d.extrude("blade", outline, h=h)
    s3d.material(solid, kind="steel", color="#59504b")
    return s3d.group("blade", solid)
