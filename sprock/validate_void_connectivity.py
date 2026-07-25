# Iron rule 4 validator: ONE CONNECTED VOID, NO DEAD ENDS.
# Rasterises the void plan and flood-fills from the mouth. Proves the exit is
# reachable and reports any pocket that isn't part of the main passage.
import math

W, D = 180.0, 140.0
RES  = 0.5                      # mm per cell

def rect(cx, cy, w, h, deg=0.0):
    r = math.radians(deg)
    def inside(x, y):
        dx, dy = x - cx, y - cy
        lx =  dx*math.cos(-r) - dy*math.sin(-r)
        ly =  dx*math.sin(-r) + dy*math.cos(-r)
        return abs(lx) <= w/2 and abs(ly) <= h/2
    return inside
def ellipse(cx, cy, rx, ry):
    return lambda x, y: ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1.0

VOID = [
    ("chamber",      ellipse(22, -14, 42, 42*0.72)),
    ("throat_mouth", rect(74, -25, 42, 24)),
    ("gallery",      rect(-39.5, -34.5, 62, 17, 25)),
    ("throat_exit",  rect(-64, -60, 18, 30, -8)),
]

nx, ny = int(W/RES), int(D/RES)
def wx(i): return -W/2 + (i+0.5)*RES
def wy(j): return -D/2 + (j+0.5)*RES

grid = [[False]*ny for _ in range(nx)]
for i in range(nx):
    for j in range(ny):
        x, y = wx(i), wy(j)
        grid[i][j] = any(f(x, y) for _, f in VOID)

# seed at the MOUTH, on the right face
seed = None
for j in range(ny):
    i = nx-1
    if grid[i][j]: seed = (i, j); break
assert seed, "mouth does not reach the right face"

seen = [[False]*ny for _ in range(nx)]
stack=[seed]; seen[seed[0]][seed[1]]=True; n=0
while stack:
    i,j = stack.pop(); n += 1
    for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
        a,b = i+di, j+dj
        if 0<=a<nx and 0<=b<ny and grid[a][b] and not seen[a][b]:
            seen[a][b]=True; stack.append((a,b))

total = sum(1 for i in range(nx) for j in range(ny) if grid[i][j])
orphan = total - n

# does the flood reach the FRONT face (the exit)?
reaches_exit = any(seen[i][0] for i in range(nx))
# does it reach the glass faces it must NOT breach?
hits_back = any(seen[i][ny-1] for i in range(nx))
hits_left = any(seen[0][j] for j in range(ny))

print(f"void cells            : {total}")
print(f"reachable from mouth  : {n}")
print(f"ORPHANED (dead pocket): {orphan}   -> {'PASS' if orphan==0 else 'FAIL'}")
print(f"mouth -> exit reaches front face : {'PASS' if reaches_exit else 'FAIL'}")
print(f"void breaches BACK glass  : {'FAIL' if hits_back else 'PASS'}")
print(f"void breaches LEFT glass  : {'FAIL' if hits_left else 'PASS'}")
print(f"void volume fraction (plan): {100.0*total/(nx*ny):.1f}%")
