# Figma Plugin API Gotchas

Hard-won lessons from building 57+ iOS screens through the Figma Plugin API. Read this before writing any `use_figma` code.

## Table of Contents

1. [Page Access](#1-page-access)
2. [Font Loading](#2-font-loading)
3. [Color System](#3-color-system)
4. [Auto-Layout Traps](#4-auto-layout-traps)
5. [Text Nodes](#5-text-nodes)
6. [Frame Sizing](#6-frame-sizing)
7. [Node Traversal](#7-node-traversal)
8. [Performance](#8-performance)
9. [Common Error Messages](#9-common-error-messages)

---

## 1. Page Access

**Problem:** `page.children` returns empty array `[]` even when the page has frames.

**Cause:** Figma lazy-loads page content. You must set a page as current before accessing its children.

**Fix:**
```javascript
// WRONG — children will be empty
const page = figma.root.children.find(p => p.name === 'Screens');
console.log(page.children.length); // 0 !!!

// CORRECT
const page = figma.root.children.find(p => p.name === 'Screens');
await figma.setCurrentPageAsync(page);
console.log(page.children.length); // 57
```

**Rule:** Every `use_figma` call that reads from a page must start with `figma.setCurrentPageAsync(page)`.

---

## 2. Font Loading

**Problem:** Setting `node.characters` throws an error or silently fails.

**Cause:** Figma requires fonts to be loaded into memory before any text manipulation.

**Fix:**
```javascript
// Load ALL font variants you'll use BEFORE any text ops
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });

// Now safe to modify text
textNode.characters = "Hello World";
textNode.fontSize = 16;
textNode.fontName = { family: "Inter", style: "Medium" };
```

**Rule:** If your code touches `.characters`, `.fontSize`, `.fontName`, `.textDecoration`, or any text property — load fonts first. Even just reading `.fontName` on a node can fail without loading.

**Multi-font gotcha:** If a text node uses mixed fonts (e.g., part Bold, part Regular), you need to load ALL variants before modifying:
```javascript
// Check what fonts are used in a mixed node
const fonts = textNode.getRangeAllFontNames(0, textNode.characters.length);
for (const font of fonts) {
  await figma.loadFontAsync(font);
}
```

---

## 3. Color System

**Problem:** Colors look wrong or invisible after setting fills.

**Cause:** Figma uses 0.0–1.0 floats for RGB, not 0–255.

**Conversion:**
```javascript
// HEX → Figma RGB
function hexToFigma(hex) {
  hex = hex.replace('#', '');
  return {
    r: parseInt(hex.slice(0, 2), 16) / 255,
    g: parseInt(hex.slice(2, 4), 16) / 255,
    b: parseInt(hex.slice(4, 6), 16) / 255,
  };
}

// Common iOS palette (Tailwind-based):
const COLORS = {
  white:    { r: 1, g: 1, b: 1 },
  gray50:   hexToFigma('F9FAFB'),
  gray100:  hexToFigma('F3F4F6'),
  gray200:  hexToFigma('E5E7EB'),
  gray300:  hexToFigma('D1D5DB'),
  gray400:  hexToFigma('9CA3AF'),
  gray500:  hexToFigma('6B7280'),
  gray700:  hexToFigma('374151'),
  gray800:  hexToFigma('1F2937'),
  gray900:  hexToFigma('111827'),
  teal500:  hexToFigma('0D9488'),
  red500:   hexToFigma('EF4444'),
  green500: hexToFigma('22C55E'),
};
```

**Setting fills correctly:**
```javascript
// WRONG — fills is readonly, modifying in place doesn't work
node.fills[0].color = { r: 1, g: 0, b: 0 };

// CORRECT — replace the entire fills array
node.fills = [{ type: 'SOLID', color: { r: 1, g: 0, b: 0 } }];

// With opacity
node.fills = [{ type: 'SOLID', color: hexToFigma('0D9488'), opacity: 0.1 }];
```

---

## 4. Auto-Layout Traps

**Problem:** Frame shrinks to tiny size or content disappears after setting auto-layout.

**Cause:** Auto-layout frames resize to fit their content. If children are positioned absolutely or have zero size, the frame collapses.

**Scenarios and fixes:**

### Fixed-size elements inside auto-layout
```javascript
// OTP input boxes that must be exactly 48×56
const box = figma.createFrame();
box.layoutMode = "NONE"; // Disable auto-layout on the box itself
box.resize(48, 56);
box.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
box.strokes = [{ type: 'SOLID', color: hexToFigma('E5E7EB') }];
box.strokeWeight = 1;
box.cornerRadius = 12;
```

### Container with auto-layout
```javascript
const container = figma.createFrame();
container.layoutMode = "VERTICAL";
container.primaryAxisSizingMode = "AUTO";  // Height grows with content
container.counterAxisSizingMode = "FIXED"; // Width stays fixed
container.resize(393, 100); // Width will stay 393, height adjusts
container.itemSpacing = 16;
container.paddingTop = 16;
container.paddingBottom = 16;
container.paddingLeft = 20;
container.paddingRight = 20;
```

### Full-width buttons
```javascript
const button = figma.createFrame();
button.layoutMode = "HORIZONTAL";
button.primaryAxisAlignItems = "CENTER"; // Center text horizontally
button.counterAxisAlignItems = "CENTER"; // Center text vertically
button.layoutAlign = "STRETCH"; // Fill parent width (if parent is auto-layout)
button.resize(353, 50); // 393 - 20*2 padding
button.cornerRadius = 25;
button.fills = [{ type: 'SOLID', color: hexToFigma('0D9488') }];
```

---

## 5. Text Nodes

**Creating text:**
```javascript
const text = figma.createText();
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
text.fontName = { family: "Inter", style: "Regular" };
text.characters = "Hello World";
text.fontSize = 16;
text.lineHeight = { value: 24, unit: "PIXELS" };
text.fills = [{ type: 'SOLID', color: hexToFigma('111827') }];
```

**Text auto-resize modes:**
```javascript
// Fixed width, height adjusts (most common for paragraphs)
text.textAutoResize = "HEIGHT";
text.resize(353, text.height); // Set width, height auto

// Both width and height auto (for labels)
text.textAutoResize = "WIDTH_AND_HEIGHT";

// Fixed box (for constrained areas)
text.textAutoResize = "NONE";
text.resize(200, 50);
```

**Text alignment:**
```javascript
text.textAlignHorizontal = "CENTER"; // "LEFT" | "CENTER" | "RIGHT" | "JUSTIFIED"
text.textAlignVertical = "CENTER";   // "TOP" | "CENTER" | "BOTTOM"
```

---

## 6. Frame Sizing

**iPhone models:**

| Device | Width | Height | Safe Area |
|--------|-------|--------|-----------|
| iPhone 15 Pro | 393 | 852 | top: 59, bottom: 34 |
| iPhone 15 Pro Max | 430 | 932 | top: 59, bottom: 34 |
| iPhone SE 3 | 375 | 667 | top: 20, bottom: 0 |
| iPhone 15 | 393 | 852 | top: 59, bottom: 34 |

**Standard recommendation:** Design for iPhone 15 Pro (393×852) as the default.

**iOS Widget sizes:**
| Widget | Width | Height |
|--------|-------|--------|
| Small | 170 | 170 |
| Medium | 364 | 170 |
| Large | 364 | 382 |

Note: widget sizes vary by device. The above are iPhone 15 Pro values.

**Resize vs. setting dimensions:**
```javascript
// Use resize() for frames
frame.resize(393, 852);

// Don't set width/height directly — it doesn't work on all node types
// frame.width = 393; // May not work!
```

---

## 7. Node Traversal

**Finding nodes:**
```javascript
// Find all text nodes in a frame
const textNodes = frame.findAll(n => n.type === 'TEXT');

// Find by name (exact)
const nav = frame.findOne(n => n.name === 'Navigation Bar');

// Find by name (partial)
const buttons = frame.findAll(n => n.name.toLowerCase().includes('button'));

// Find by type
const frames = frame.findAll(n => n.type === 'FRAME');
const instances = frame.findAll(n => n.type === 'INSTANCE');
```

**Safe node access:**
```javascript
// Always check if node exists
const node = figma.getNodeById("145:3");
if (node && node.type === 'TEXT') {
  await figma.loadFontAsync(node.fontName);
  node.characters = "Updated text";
}
```

**Cloning and positioning:**
```javascript
const clone = original.clone();
clone.name = "New Name";
clone.x = original.x + original.width + 47; // 47pt gap between screens
clone.y = original.y;
// Clone is automatically added to the same parent
```

---

## 8. Performance

**Return data efficiently:** The `use_figma` tool has a response size limit. Don't dump entire node trees.

```javascript
// WRONG — too much data
return JSON.stringify(frame);

// CORRECT — return only what you need
const summary = frame.children.map(c => ({
  id: c.id, name: c.name, type: c.type,
  x: Math.round(c.x), y: Math.round(c.y),
  w: Math.round(c.width), h: Math.round(c.height)
}));
return JSON.stringify(summary);
```

**Batch operations:** If modifying many frames, do it in one `use_figma` call rather than multiple calls.

**Skip invisible:** For large files, skip invisible nodes:
```javascript
figma.skipInvisibleInstanceChildren = true;
```

---

## 9. Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot read property 'children' of undefined` | Page not found by name | Check page names: `figma.root.children.map(p => p.name)` |
| `children is empty array` | Page not set as current | Add `await figma.setCurrentPageAsync(page)` |
| `Error: Cannot set characters` | Font not loaded | Add `await figma.loadFontAsync(...)` |
| `fills is not writable` | Modifying fills in place | Replace entire array: `node.fills = [...]` |
| `Expected type "INTEGER"` | Float where int expected | Use `Math.round()` for positions and sizes |
| `Node not found` | Wrong node ID or deleted | Verify ID exists: `figma.getNodeById(id)` |
| Response too large | Returning too much data | Filter and summarize before returning |
