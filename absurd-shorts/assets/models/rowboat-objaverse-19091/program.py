import sand3d as s3d


def rowboat():
    base = s3d.at(hull(), x=-64, y=187, z=-1)
    rim = s3d.at(gunwale(), x=-64, y=187, z=390)
    stern = s3d.at(stern_crossbar(), x=-70, y=-825, z=356)
    middle = s3d.at(middle_crossbar(), x=-64, y=-95, z=356)
    bow = s3d.at(bow_crossbar(), x=-58, y=654, z=356)
    return s3d.assembly('rowboat', base, rim, stern, middle, bow)


def hull(w=1536, d=4004, h=612, floor=185, inset=104):
    outer = hull_form('outer', w=w, d=d, h=h)
    inner = interior_form('inside', w=w-inset*2, h=h-floor+10)
    outer = s3d.cut(outer, s3d.at(inner, z=floor))
    top_trim = s3d.at(s3d.box('top_trim', w=w*2, d=d*2, h=h), z=h-12)
    outer = s3d.cut(outer, top_trim)
    s3d.material(outer, 'plastic', color='#b4b4b4')
    return s3d.group('hull', outer)


def hull_form(name, w, d, h, ratio=0.47):
    # Measured half-plan coordinates as fractions of beam and length, rounded to hundredths.
    half_plan = [(0.33*w,-d/2), (0.41*w,-0.37*d), (0.47*w,-0.21*d), (w/2,-0.04*d), (0.46*w,0.17*d), (0.35*w,0.31*d), (0.19*w,0.41*d), (0,d/2)]
    outline = half_plan + [(-x,y) for x,y in reversed(half_plan[:-1])]
    bottom = s3d.poly([(x*ratio,y) for x,y in outline])
    return s3d.loft(name, bottom, s3d.at(s3d.poly(outline), z=h))


def interior_form(name, w, h, ratio=0.69, end_taper=0.895):
    # Half-opening measurements: transverse half-width and longitudinal coordinate from the hull origin.
    half_opening = [(0.32*w,-1687), (0.42*w,-1310), (w/2,-117), (0.46*w,539), (0.35*w,1111), (0.19*w,1477)]
    outline = half_opening + [(-x,y) for x,y in reversed(half_opening)]
    bottom = s3d.poly([(x*ratio,y*end_taper) for x,y in outline])
    return s3d.loft(name, bottom, s3d.at(s3d.poly(outline), z=h))


def gunwale(w=1536, d=4004, h=224, t=14):
    outer = hull_form('rim_outer', w=w, d=d, h=612)
    inner = interior_form('rim_inner', w=w-208, h=437)
    rim = s3d.cut(outer, s3d.at(inner, z=185))
    clip = s3d.at(s3d.box('clip', w=w*2, d=d*2, h=t+2), z=612-t)
    rim = s3d.intersect(rim, clip)
    rim = s3d.at(rim, z=-390)
    s3d.material(rim, 'plastic', color='#00a2e7')
    return s3d.group('gunwale', rim)


def stern_crossbar(w=1390, d=124, h=258):
    return s3d.group('stern_crossbar', crossbar_form(w=w, d=d, h=h))


def crossbar_form(w, d, h, thickness=44):
    bar = s3d.at(s3d.box('bar', w=w-180, d=d, h=thickness), z=162)
    support = s3d.extrude('support', s3d.poly([(90,0),(-90,h), (0,h), (120,h-80)]), h=d)
    support = s3d.at(support, x=-w/2+90, y=d/2, rx=90)
    twin = s3d.transform(s3d.copy(support), mirror='x')
    bar = s3d.join(bar, support, twin)
    s3d.material(bar, 'plastic', color='#e76000')
    return bar


def middle_crossbar(w=1536, d=124, h=258):
    return s3d.group('middle_crossbar', crossbar_form(w=w, d=d, h=h))


def bow_crossbar(w=1450, d=124, h=258):
    return s3d.group('bow_crossbar', crossbar_form(w=w, d=d, h=h))
