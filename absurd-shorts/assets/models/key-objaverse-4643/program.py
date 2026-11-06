import sand3d as s3d


def key():
    placed = s3d.at(head(), x=4.3, y=11.7, z=-0.4)
    return s3d.assembly("key", placed)


def head(w=29.2, d=26, h=3, corner=3, hole_w=14, hole_d=5.5, hole_y=5.2, recess_w=13.7, recess_d=10.5, recess_y=-5, recess_depth=0.55):
    outline = s3d.poly([(-w/2,0),(-w/4,-d/2),(w/4,-d/2),(w/2,0),(w/4,d/2),(-w/4,d/2)], fillet=corner)
    solid = s3d.extrude("bow", outline, h=h)
    solid = s3d.pocket(solid, s3d.rect(w=hole_w,d=hole_d,r=hole_d/2-0.2), on=solid.face("top").move(y=hole_y))
    solid = s3d.pocket(solid, s3d.rect(w=recess_w,d=recess_d),depth=recess_depth,on=solid.face("top").move(y=recess_y))
    solid = s3d.pocket(solid, s3d.rect(w=recess_w,d=recess_d),depth=recess_depth,on=solid.face("bottom").move(y=-recess_y))
    s3d.material(solid,"brass",color="#e6e6e6")
    carried = s3d.at(blade(), x=-4.3, y=-11.7, z=0.2)
    return s3d.group("head",solid,carried)


def blade(h=2.2, base=0.8, straight=1, crest=9, root=6.5, tip=-35.5, groove_x=2.9, groove_w=1.4, groove_depth=0.9, tooth_x=8, tooth_w=5, tooth_depth=0.7, underside_x=3.8, underside_w=2.2, underside_depth=0.3):
    outline = s3d.poly([(base,0),(straight,tip+2),(3,tip),(6,tip),(6,tip+2),(8,-32),(crest,-27),(root,-25),(7,-23),(7,-21),(root,-20),(crest,-15),(7,-15),(7,-11),(root,-11),(7,-7),(6,-6),(8,-3),(crest,-3),(crest,0)])
    solid=s3d.extrude("blade",outline,h=h)
    solid=s3d.pocket(solid,s3d.rect(w=groove_w,d=-tip*2),depth=groove_depth,on=solid.face("top").move(x=groove_x,y=tip/2))
    solid=s3d.pocket(solid,s3d.rect(w=tooth_w,d=-tip*2),depth=tooth_depth,on=solid.face("top").move(x=tooth_x,y=tip/2))
    solid=s3d.pocket(solid,s3d.rect(w=underside_w,d=-tip*2),depth=underside_depth,on=solid.face("bottom").move(x=underside_x,y=-tip/2))
    s3d.material(solid,"brass",color="#e6e6e6")
    return s3d.group("blade",solid)
