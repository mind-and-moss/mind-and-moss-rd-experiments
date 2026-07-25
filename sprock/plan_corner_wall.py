# MONSTER8 plan, traced from Isaiah's sketch.
# RED = glass (BACK + RIGHT).  BLUE = rock perimeter.  GREEN = fish space.
# Key change from my earlier plan: this is NOT a block with a hole. It is a
# curved WALL that sits in the tank corner; the void is closed on two sides
# by the tank glass itself.
import zlib, struct, math

W, D = 180.0, 170.0          # footprint, mm.  x -90..90, y -85..85
PX   = 3                      # pixels per mm

# Rock perimeter, traced off the sketch (mm). Starts on the BACK glass,
# wanders out and down, ends on the RIGHT glass.
PERIM = [(-46, 85), (-46, 76), (-30, 47), (-27, 15), (-8, -6), (-22, -33),
         (1, -46), (27, -61), (56, -72), (80, -80), (90, -83)]

def seg_dist(px, py, ax, ay, bx, by):
    vx, vy = bx-ax, by-ay
    L2 = vx*vx + vy*vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px-ax)*vx + (py-ay)*vy)/L2))
    dx, dy = px-(ax+t*vx), py-(ay+t*vy)
    return math.hypot(dx, dy), t

def perim_dist(px, py):
    best, bt, seg = 1e9, 0.0, 0
    for i in range(len(PERIM)-1):
        d, t = seg_dist(px, py, *PERIM[i], *PERIM[i+1])
        if d < best: best, bt, seg = d, t, i
    return best, (seg + bt) / (len(PERIM)-1)     # distance, 0..1 along path

def inside_corner(px, py):
    """Is this point on the glass-corner side of the perimeter?
    Ray-cast upward against the closed polygon formed by the perimeter plus
    the two glass runs."""
    poly = PERIM + [(90, 85), (-46, 85)]
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        if (y1 > py) != (y2 > py):
            xint = x1 + (py-y1)*(x2-x1)/(y2-y1)
            if px < xint: c = not c
    return c

# wall thickness: thin near the back glass, heavier toward the front-right toe
def wall_t(s):  return 13.0 + 15.0 * (s ** 1.3)

# OPENINGS. Isaiah's rule: "where the green passes the blue = opening".
# So an opening is simply a stretch of perimeter with no wall. Positions are
# given along the run (0 = back glass end, 1 = the front-right toe).
# (name, centre s, width along the perimeter in mm)
PERIM_LEN = 256.0
OPENINGS = [
    ("upper_vent", 0.17, 20.0),   # high and small - draught in
    ("MOUTH",      0.52, 42.0),   # the big one, mid-wall, faces front-left
    ("tail_exit",  0.83, 24.0),   # low, far from the mouth - flow-through out
]
def in_opening(s):
    for name, cs, w in OPENINGS:
        if abs(s - cs) * PERIM_LEN <= w/2:
            return name
    return None

nx, ny = int(W*PX), int(D*PX)
rows = []
for j in range(ny):
    y = 85.0 - (j + 0.5)/PX
    row = bytearray()
    for i in range(nx):
        x = -90.0 + (i + 0.5)/PX
        d, s = perim_dist(x, y)
        on_back  = y > 85 - 3.5
        on_right = x > 90 - 3.5
        if on_back or on_right:            rgb = (235, 33, 33)      # RED glass
        elif d < 2.4:                      rgb = (30, 90, 240)      # BLUE perimeter
        elif d < wall_t(s) and inside_corner(x, y) and not in_opening(s):
                                           rgb = (108, 108, 116)    # rock wall
        elif inside_corner(x, y):          rgb = (40, 205, 65)      # GREEN space
        elif d < wall_t(s) and in_opening(s):
                                           rgb = (40, 205, 65)      # green passes blue
        else:                              rgb = (26, 26, 30)       # outside
        row += bytes(rgb)
    rows.append(bytes(row))

raw = b''.join(b'\x00' + r for r in rows)
def chunk(t, d):
    c = struct.pack('>I', len(d)) + t + d
    return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', nx, ny, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
open('/tmp/claude-0/-home-user-mind-and-moss-rd-experiments/ac8953e1-d8e8-5161-837f-51a9bd350496/scratchpad/plan_isaiah.png', 'wb').write(png)

# --- measurements -------------------------------------------------------
cell = 1.0/PX
area_void = area_rock = 0
for j in range(ny):
    y = 85.0 - (j+0.5)/PX
    for i in range(nx):
        x = -90.0 + (i+0.5)/PX
        if not inside_corner(x, y): continue
        d, s = perim_dist(x, y)
        if d < wall_t(s): area_rock += 1
        else:             area_void += 1
print(f"void  plan area : {area_void*cell*cell/100:.1f} cm2")
print(f"rock  plan area : {area_rock*cell*cell/100:.1f} cm2")
print(f"wall thickness  : {wall_t(0):.0f} mm at the back glass -> {wall_t(1):.0f} mm at the toe")
win_back = win_right = 0
for k in range(int(W*PX)):
    x = -90.0 + (k+0.5)/PX
    if inside_corner(x, 84.0) and perim_dist(x, 84.0)[0] >= wall_t(perim_dist(x,84.0)[1]):
        win_back += 1
for k in range(int(D*PX)):
    y = 85.0 - (k+0.5)/PX
    if inside_corner(89.0, y) and perim_dist(89.0, y)[0] >= wall_t(perim_dist(89.0,y)[1]):
        win_right += 1
print(f"WINDOW on back glass  : {win_back/PX:.0f} mm wide")
print(f"WINDOW on right glass : {win_right/PX:.0f} mm tall")
print(f"frost film patch      : {win_back/PX:.0f} x {win_right/PX:.0f} mm, L-shaped over the corner")
for name, cs, w in OPENINGS:
    print(f"opening {name:<11}: {w:.0f} mm wide at s={cs}")
print(f"perimeter run   : {sum(math.dist(PERIM[i],PERIM[i+1]) for i in range(len(PERIM)-1)):.0f} mm")
