# Automation & Control Techniques (Inspiration File)

A running collection of electronics/control techniques spotted in the wild that could plug into Mind and Moss builds — embedded mechanics in The Machine, RPM monitoring on the bike grinder, future products with reactive/animated elements.

This file is a staging ground. When a technique here gets adopted into an actual build, move the spec into the relevant product/tool folder and link back here.

---

## CyberBrick (Bambu Lab)

**Source:** spotted on a 3D-print project page (BOM-driven build, "CyberBrick version is the default"; alternative non-electronic version also offered).

**What it is:** Bambu Lab's modular embedded electronics platform aimed at 3D-printed maker projects. Smart modules (servos, motors, a controller hub) designed to be press-fit or screw-mounted into printed parts. BLE-based remote control. The hub speaks to all the modules, you author the behavior in their app/tool.

**Why it matters for Mind and Moss:**
- **The Machine** — pillared concrete with "embedded machines (filtration, mechanics, visible systems)." Servos/motors driven by CyberBrick could power visible mechanical elements: animated valves, cycling water mechanisms, kinetic art atop the concrete pillars, automated feeding systems, scheduled lighting transitions.
- **Bike grinder** — RPM sensor was already in the locked spec. CyberBrick could integrate the sensor + display in one neat module instead of an Amazon-bought meter cabled in.
- **Future reactive products** — anything that responds to time, sensor input, or remote command without needing an Arduino + custom firmware learning curve.

**Trade-offs vs DIY (Arduino/ESP32 + servos + custom firmware):**
- **Pro:** assembled, debugged, app-authored. Days not weeks. BOM is published, parts are sourceable.
- **Pro:** fits the "boutique end of market" thesis from R005 — buying mature components for the smart parts, hand-crafting the artistic parts.
- **Con:** higher per-unit cost than rolling your own. Project pages note this explicitly ("the default version's cost is higher due to servos, motors & CyberBrick electronics").
- **Con:** vendor lock-in to Bambu's ecosystem and app. If they discontinue or break compatibility, projects bricked.
- **Mitigation:** for one-of products (The Machine commission units) the cost premium is small relative to total build value. For volume products it's a problem.

**When to use:**
- Prototype phase — get a working animated/automated thing fast, iterate the artistic shell, swap to custom electronics later if volume justifies.
- Demo/show pieces — convention floor, gallery installs, Patreon-funded one-offs.
- The CyberBrick BOM is a useful starting point even if you reverse-engineer to discrete parts later.

**Open question:** can CyberBrick modules survive the wet/humid environment around an aquarium/terrarium? Look for IP-rated housing options or plan a sealed sub-chassis.

**Action:** save the BOM Isaiah is looking at right now to this folder when he's done so we have it for reference.

---

## (template — add more techniques here)

### Technique name

**Source:** where you saw it.

**What it is:** one-paragraph description.

**Why it matters for Mind and Moss:** specific connections to current/future builds.

**Trade-offs:** pros, cons, things to watch.

**When to use:** application contexts.

**Action:** what to capture / try / link.
