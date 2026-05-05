# Blender vs Plasticity — CAD Tooling Decision

Research on switching from Blender to Plasticity for precision modeling, plus iPad-native sculpting options that bridge into the desktop pipeline.

---

Source: RESEARCH-004 Thread 13 — "Switching from Blender to Plasticity"

### Context
Isaiah is over Blender — finds workflow clunky, hard to model, hard to interact with Claude on. Heard good things about Plasticity. Wants iPad+Apple Pencil workflow that goes straight to Bambu Lab printer.

### Plasticity vs Blender
- **Plasticity strengths:** direct/intuitive editing (push/pull geometry), smart fillets/blending, designed for natural design thinking
- More CAD-focused than Blender — better for **precision modeling and product design**
- **Desktop only** — no iPad version
- Exports STL directly for 3D print pipeline

### iPad + Apple Pencil Workflow
Plasticity doesn't have iPad app. For iPad-native modeling:
- **Shapr3D** — subscription-based
- **Nomad Sculpt** — ~$30 one-time, sculpting-focused

Ideal pipeline (proposed): iPad sketch → desktop modeling → Bambu STL export. Open question on which iPad app to bridge with desktop tool.

### Recommendation
For The Machine (precision parts, brackets, connectors): Plasticity wins for CAD-style precision over Blender's polygon focus.
For The Gem (organic glass/clay forms): Either tool works; sculpting-style apps (Blender, Nomad) better for organic forms.

---

Source: RESEARCH-005 Thread "3D Modeling Apps iPad" + "3D modeling software options" (chats #54 + #58)

## iPad CAD pipeline (duplicate questions across two chats)
- Both chats asked the same fundamental question: how to do CAD work on iPad and translate to Blender / Bambu Lab
- Confirms Isaiah is actively trying to find an iPad-first workflow
- Suggested apps in earlier excavation: Shapr3D (subscription) and Nomad Sculpt (~$30 one-time)

## The unresolved question
> "Can I make 3D art on the iPad and then transport it to Blender or [the printer]?"

Answer (synthesizing across all CAD threads): yes, but the workflow has handoffs.
- iPad: sketch / sculpt in Shapr3D or Nomad Sculpt
- Export: STL or OBJ
- Desktop: open in Plasticity or Blender for refinement / Boolean ops / parametric edits
- Slicer: Bambu Studio
- Printer: Bambu Lab

The handoff between iPad and desktop is the friction point. No single tool covers the full chain.
