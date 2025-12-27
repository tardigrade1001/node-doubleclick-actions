# Node Double Click Actions

Small quality-of-life addon for Blender’s Node Editor that adds intuitive double-click actions:
- **Double-click a node** → toggle mute  
- **Double-click empty space** → open node search  

This addon exists to remove a tiny but persistent friction when switching between node-based tools.

---

## Motivation

In **ComfyUI**, adding nodes via **double-click** is natural and fast.  
When switching back to **Blender’s Node Editor**, having to press **Shift + A** every time felt unnecessarily disruptive.

This addon was created to bridge that gap and make node interaction feel more consistent across tools.

The goal is intentionally narrow:  
**fix one small annoyance and do it reliably.**

---

## Features

- Double-click a node to **toggle mute**
- Double-click empty space to **open node search**
- Works in:
  - Shader Editor
  - Geometry Nodes
  - Compositor
- Uses Blender’s **native keymap system**
- No modal operators
- No timers
- No background handlers
- Optional debug logging for troubleshooting

---

## Compatibility

- **Tested on Blender 5.1**
- Expected to work on **Blender 4.x and later**, as it relies on stable, native keymap behavior

> Note: Blender 5.x changed how some node operators are registered.  
> This addon includes safe fallbacks to avoid crashes or console errors.

---

## Installation

### Method 1: ZIP Install (Recommended)

1. Download the repository as a ZIP
2. Open Blender
3. Go to **Edit → Preferences → Add-ons**
4. Click **Install…**
5. Select the ZIP file
6. Enable **Node Double Click Actions**

---

### Method 2: Manual Install

1. Copy the addon file into:
Blender//scripts/addons/
2. Restart Blender
3. Enable **Node Double Click Actions** in Preferences

---

## Usage

### Node Editor

| Action | Result |
|------|--------|
| Double-click a node | Toggle mute |
| Double-click empty space | Open node search |

There are:
- No modifier keys
- No modes
- No configuration required to start using it

---

## Preferences

Located in **Edit → Preferences → Add-ons → Node Double Click Actions**

### Options

- **Double-Click to Mute Nodes**  
Enable or disable node muting behavior

- **Double-Click Empty Space to Search**  
Enable or disable opening the search menu

- **Enable Debug Logging**  
Prints detailed behavior and fallback information to the system console  
*(OFF by default)*

---

## Debug Logging

Debug logging is **disabled by default**.

When enabled, the addon prints:
- Which operator is being invoked
- When fallbacks are used
- Why certain actions were skipped

Example output:
[Node DoubleClick] node.add_search failed: AttributeError(...)
[Node DoubleClick] Falling back to wm.search_menu

This is useful for:
- Troubleshooting
- Reporting issues
- Verifying behavior across Blender versions

---

## Design Notes / Limitations

This addon intentionally keeps things simple:

- Uses Blender’s **active node logic**, not pixel-level hit testing  
  (avoids complexity and instability)
- Does not override or replace existing keybindings
- Does not attempt to infer user intent beyond the double-click itself
- Behavior follows Blender’s input system, not custom mouse tracking

Rare edge cases may exist when Blender retains a previously active node, but no destructive actions are performed.

---

## License

This project is licensed under the **MIT License**.

You are free to:
- Use
- Modify
- Distribute
- Include in commercial or non-commercial projects

With minimal restrictions. See the `LICENSE` file for full details.

---

## Maintenance

This is a **lightweight utility** with **minimal maintenance intent**.

The code is small, stable, and designed to survive Blender API changes with minimal intervention.  
Community contributions and fixes are welcome.

---

## Acknowledgements

Created with assistance from **Gemini**, used as a coding aid and brainstorming tool.

The final behavior and testing decisions were driven by practical daily use.

---

## Why this addon exists (in one sentence)

Because double-clicking to add nodes felt right in ComfyUI — and going back to **Shift + A** in Blender didn’t.