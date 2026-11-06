import sand3d as s3d


def key():
    blank = s3d.at(key_blank(), x=-14.25, y=-78.61, z=31.3015)
    return s3d.assembly("key", blank)


def key_blank(head_d=24.34, head_y=-18.08, h=1.297, bore=6.8, bore_y=-24.1,
              back=-2.95, neck=-0.75, tip=0.6, crest=3.5, root=0.4,
              base=-8, shoulder=22.9, tip_start=26.6, end=30.245,
              tooth_tip=26.5, notch_tip=22.6, tooth_outer=19.6,
              notch_outer=15.6, tooth_middle=11.6, notch_middle=10.6,
              tooth_inner=4.6, notch_inner=3.6, shaft_start=-2.4):
    head = s3d.at(s3d.cylinder("head", d=head_d, h=h), y=head_y)
    outline = s3d.poly([(back,base), (back,shoulder), (neck,tip_start),
                        (neck,end), (tip,end), (crest,tooth_tip),
                        (root,notch_tip), (crest,tooth_outer),
                        (root,notch_outer), (crest,tooth_middle),
                        (root,notch_middle), (crest,tooth_inner),
                        (root,notch_inner), (crest,shaft_start), (crest,base)])
    shaft = s3d.extrude("shaft", outline, h=h)
    blank = s3d.join(head, shaft)
    blank = s3d.hole(blank, d=bore, on=(0,bore_y))
    s3d.material(blank, kind="brass", color="#a58b46")
    return s3d.group("key_blank", blank)
