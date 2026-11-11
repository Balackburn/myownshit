#!/usr/bin/env python3
"""La cravate (story 43, cycle 7 of the cartoon staging): this man caught his tie in the lift door. The lift went up. Not him. The tie did. To the
sixth floor. He called the managing agent. The agent replied: "In the lift shaft, it is a common part." Since then the lady on the third hangs her
washing on it. The kid on the fifth plays it. He is making progress. To unhook it, a vote of the general meeting is needed. Yesterday they voted. One
vote was missing. His. He was downstairs. They voted the repainting all the same. His tie is beige. He pays the service charges.
(work in progress: the sets are being tested)"""
from story_kit import *
import math

st = Story('cravate', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0)])
FH = 2.8
RED = '#C8202A'
NAPE = {'actor': 'mec', 'joint': 'neck', 'offset': [0, 0.04, -0.09]}
SEAM = [0, 2.07, -2.91]
st.shot('S01', 'immeubleHall', setOpts={'doors': [[0, 1], [0.6, 0]], 'floor': [[0, 'RC'], [1.2, '1'], [1.8, '2'], [2.4, '3']]}, actors=[act('mec', [0.05, 0, -2.45], 0, 'stand', 'worried', keys=[k(0.0, look=None), k(0.0, toon={'tie': [0.02, 0, 0]}, toonDur=0.0)])],
        props=[P('rope', 'tieRope', on=NAPE, opts={'to': SEAM, 'pluck': [[1.0, 0.05, 7, 12, 3]]})],
        cams=[cam(0.0, [0.9, 1.5, 2.2], [0.85, 1.5, 2.0], [0, 1.45, -3.0], [0, 1.45, -3.0], lens=44)])
SX = 6.4 / 2 - 1.7 / 2 - 0.12
ME2 = [round(SX - 1.7 / 2 - 0.55, 3), 0, 0.3]
st.shot('S02', 'immeubleCoupe', setOpts={'cabin': [[0, 0], [2.5, 6]]}, actors=[act('mec', ME2, 0, 'stand', 'worried', keys=[k(0.0, look=None), k(0.0, toon={'tie': [0.02, 0, 0]}, toonDur=0.0)])],
        props=[P('rope', 'tieRope', on=NAPE, opts={'via': [[round(SX - 1.7 / 2 - 0.06, 3), 2.1, 0.2], [round(SX - 0.55, 3), 2.25, 0.1]], 'toKeys': [[0, SX - 0.55, 0.3, 0.1], [2.5, SX - 0.55, 6 * FH + 0.3, 0.1]],
                                                    'items': [{'at': 0.45, 'kind': 'shirt', 'color': '#F4F1E8', 'from': 1.0}, {'at': 0.5, 'kind': 'sock', 'color': '#3F7A5A', 'from': 1.2}, {'at': 0.55, 'kind': 'towel', 'color': '#E8C24A', 'from': 1.4}], 'paint': [1.5, 2.5]})],
        cams=[cam(0.0, [0, 10.0, 27.0], [0, 10.0, 26.5], [0, 10.0, 0], [0, 10.0, 0], lens=44)])
st.write("La cravate", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5)
