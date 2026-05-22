# iOS Screen Template — Figma Plugin API

Complete annotated template for creating a full iOS screen (iPhone 15 Pro, 393×852) in Figma through the Plugin API.

## Full Screen Creation Code

```javascript
// ═══════════════════════════════════════════════════
// iOS Screen Template for Figma Plugin API
// Device: iPhone 15 Pro (393×852)
// ═══════════════════════════════════════════════════

const FILE_KEY = 'YOUR_FILE_KEY';

// ── Prerequisites ──
const page = figma.root.children.find(p => p.name === 'Screens');
await figma.setCurrentPageAsync(page);

// Load all fonts we'll need
const fonts = [
  { family: "Inter", style: "Regular" },
  { family: "Inter", style: "Medium" },
  { family: "Inter", style: "Semi Bold" },
  { family: "Inter", style: "Bold" },
];
for (const font of fonts) {
  await figma.loadFontAsync(font);
}

// ── Color helpers ──
function hex(h) {
  h = h.replace('#', '');
  return {
    r: parseInt(h.slice(0,2), 16) / 255,
    g: parseInt(h.slice(2,4), 16) / 255,
    b: parseInt(h.slice(4,6), 16) / 255,
  };
}

const isLight = true; // Toggle for Light/Dark

const C = isLight ? {
  bg:         hex('FFFFFF'),
  surface:    hex('F9FAFB'),
  textPri:    hex('111827'),
  textSec:    hex('6B7280'),
  border:     hex('E5E7EB'),
  accent:     hex('0D9488'),
  accentText: hex('FFFFFF'),
  tabInact:   hex('9CA3AF'),
  statusBar:  hex('000000'),
} : {
  bg:         hex('111827'),
  surface:    hex('1F2937'),
  textPri:    hex('FFFFFF'),
  textSec:    hex('9CA3AF'),
  border:     hex('374151'),
  accent:     hex('0D9488'),
  accentText: hex('FFFFFF'),
  tabInact:   hex('6B7280'),
  statusBar:  hex('FFFFFF'),
};

// ═══ 1. OUTER FRAME ═══
const screen = figma.createFrame();
screen.name = `ScreenName - ${isLight ? 'Light' : 'Dark'}`;
screen.resize(393, 852);
screen.fills = [{ type: 'SOLID', color: C.bg }];
screen.clipsContent = true;

// Position on canvas (adjust based on existing frames)
screen.x = 0;
screen.y = 0;

// ═══ 2. STATUS BAR (0–54pt) ═══
const statusBar = figma.createFrame();
statusBar.name = 'Status Bar';
statusBar.resize(393, 54);
statusBar.fills = []; // Transparent
screen.appendChild(statusBar);
statusBar.x = 0;
statusBar.y = 0;

// Time (left)
const time = figma.createText();
time.characters = "9:41";
time.fontSize = 15;
time.fontName = { family: "Inter", style: "Semi Bold" };
time.fills = [{ type: 'SOLID', color: C.statusBar }];
time.x = 21;
time.y = 18;
statusBar.appendChild(time);

// Dynamic Island placeholder (center)
const island = figma.createRectangle();
island.name = 'Dynamic Island';
island.resize(126, 37);
island.x = 134;
island.y = 0;
island.cornerRadius = 19;
island.fills = [{ type: 'SOLID', color: hex('000000') }];
statusBar.appendChild(island);

// Battery/Signal indicators (right) — simplified
const indicators = figma.createText();
indicators.characters = "📶 🔋";
indicators.fontSize = 12;
indicators.fills = [{ type: 'SOLID', color: C.statusBar }];
indicators.x = 330;
indicators.y = 20;
statusBar.appendChild(indicators);

// ═══ 3. NAVIGATION BAR (54–98pt) ═══
const navBar = figma.createFrame();
navBar.name = 'Navigation Bar';
navBar.resize(393, 44);
navBar.fills = [{ type: 'SOLID', color: C.bg }];
screen.appendChild(navBar);
navBar.x = 0;
navBar.y = 54;

// Back button (optional)
const backBtn = figma.createText();
backBtn.characters = "‹";
backBtn.fontSize = 28;
backBtn.fontName = { family: "Inter", style: "Regular" };
backBtn.fills = [{ type: 'SOLID', color: C.accent }];
backBtn.x = 16;
backBtn.y = 6;
navBar.appendChild(backBtn);

// Title
const navTitle = figma.createText();
navTitle.characters = "Screen Title";
navTitle.fontSize = 17;
navTitle.fontName = { family: "Inter", style: "Semi Bold" };
navTitle.fills = [{ type: 'SOLID', color: C.textPri }];
navTitle.textAlignHorizontal = "CENTER";
navTitle.textAutoResize = "WIDTH_AND_HEIGHT";
navBar.appendChild(navTitle);
// Center the title
navTitle.x = (393 - navTitle.width) / 2;
navTitle.y = 12;

// ═══ 4. CONTENT AREA (98–769pt) ═══
const content = figma.createFrame();
content.name = 'Content';
content.resize(393, 671); // 852 - 54 (status) - 44 (nav) - 83 (tab)
content.fills = []; // Transparent, inherits from screen
screen.appendChild(content);
content.x = 0;
content.y = 98;

// === YOUR SCREEN CONTENT GOES HERE ===
//
// Examples of common patterns:
//
// Card:
//   const card = figma.createFrame();
//   card.resize(353, 120); // 393 - 20*2 margin
//   card.cornerRadius = 12;
//   card.fills = [{ type: 'SOLID', color: C.surface }];
//   card.x = 20; card.y = 16;
//   content.appendChild(card);
//
// Full-width button:
//   const btn = figma.createFrame();
//   btn.resize(353, 50);
//   btn.cornerRadius = 25;
//   btn.fills = [{ type: 'SOLID', color: C.accent }];
//   btn.x = 20; btn.y = 600;
//   content.appendChild(btn);
//   const btnText = figma.createText();
//   btnText.characters = "Continue";
//   btnText.fontSize = 17;
//   btnText.fontName = { family: "Inter", style: "Semi Bold" };
//   btnText.fills = [{ type: 'SOLID', color: C.accentText }];
//   btnText.textAutoResize = "WIDTH_AND_HEIGHT";
//   btn.appendChild(btnText);
//   btnText.x = (353 - btnText.width) / 2;
//   btnText.y = 14;

// ═══ 5. TAB BAR (769–852pt) ═══
const tabBar = figma.createFrame();
tabBar.name = 'Tab Bar';
tabBar.resize(393, 83); // 49 bar + 34 home indicator
tabBar.fills = [{ type: 'SOLID', color: C.bg }];
// Top border
tabBar.strokes = [{ type: 'SOLID', color: C.border }];
tabBar.strokeWeight = 0.5;
tabBar.strokeAlign = "INSIDE";
// Only top stroke (workaround: use a rectangle)
screen.appendChild(tabBar);
tabBar.x = 0;
tabBar.y = 769;

// Tab items — standard 5-tab layout
const tabs = [
  { icon: '🏠', label: 'Home', active: true },
  { icon: '💊', label: 'Meds', active: false },
  { icon: '📋', label: 'Log', active: false },
  { icon: '👨‍👩‍👧', label: 'Family', active: false },
  { icon: '⚙️', label: 'Settings', active: false },
];

const tabWidth = 393 / tabs.length;
tabs.forEach((tab, i) => {
  const tabItem = figma.createFrame();
  tabItem.name = `Tab - ${tab.label}`;
  tabItem.resize(tabWidth, 49);
  tabItem.fills = [];
  tabItem.x = i * tabWidth;
  tabItem.y = 0;
  tabBar.appendChild(tabItem);

  // Icon (placeholder — replace with actual SF Symbol or component)
  const icon = figma.createText();
  icon.characters = tab.icon;
  icon.fontSize = 22;
  icon.textAutoResize = "WIDTH_AND_HEIGHT";
  tabItem.appendChild(icon);
  icon.x = (tabWidth - icon.width) / 2;
  icon.y = 6;

  // Label
  const label = figma.createText();
  label.characters = tab.label;
  label.fontSize = 10;
  label.fontName = { family: "Inter", style: "Medium" };
  label.fills = [{ type: 'SOLID', color: tab.active ? C.accent : C.tabInact }];
  label.textAutoResize = "WIDTH_AND_HEIGHT";
  tabItem.appendChild(label);
  label.x = (tabWidth - label.width) / 2;
  label.y = 32;
});

// Home indicator
const homeIndicator = figma.createRectangle();
homeIndicator.name = 'Home Indicator';
homeIndicator.resize(134, 5);
homeIndicator.cornerRadius = 3;
homeIndicator.fills = [{ type: 'SOLID', color: C.textPri, opacity: 0.3 }];
homeIndicator.x = (393 - 134) / 2;
homeIndicator.y = 70;
tabBar.appendChild(homeIndicator);

// ═══ DONE ═══
return JSON.stringify({
  id: screen.id,
  name: screen.name,
  msg: 'Screen created. Use get_screenshot to verify.'
});
```

## Grandparent Mode Variant

For simplified UI (55+ users):

- 2 tabs instead of 5 (Home + Log)
- Minimum font size: `title3` (20pt)
- Larger touch targets: 56×56 minimum
- High contrast colors
- Simplified content — only essential actions

```javascript
// Grandparent tab bar — 2 tabs
const gpTabs = [
  { icon: '🏠', label: 'Home', active: true },
  { icon: '📋', label: 'Log', active: false },
];
const gpTabWidth = 393 / 2;
// ... same pattern but with gpTabWidth and larger fonts
```

## Cover Frame Template

```javascript
// Cover frame for handoff navigation
const cover = figma.createFrame();
cover.name = '📋 Cover — Handoff Index';
cover.resize(800, 1200);
cover.x = -900;
cover.y = 0;
cover.fills = [{ type: 'SOLID', color: hex('F8F8F8') }];
cover.cornerRadius = 16;
cover.clipsContent = true;

// Project title
const title = figma.createText();
title.characters = "ProjectName";
title.fontSize = 48;
title.fontName = { family: "Inter", style: "Bold" };
title.fills = [{ type: 'SOLID', color: hex('0D9488') }];
title.x = 48;
title.y = 48;
cover.appendChild(title);

// Subtitle
const subtitle = figma.createText();
subtitle.characters = "App Description — Design Handoff";
subtitle.fontSize = 20;
subtitle.fontName = { family: "Inter", style: "Regular" };
subtitle.fills = [{ type: 'SOLID', color: hex('111827') }];
subtitle.x = 48;
subtitle.y = 110;
cover.appendChild(subtitle);

// Divider
const divider = figma.createRectangle();
divider.resize(704, 1);
divider.fills = [{ type: 'SOLID', color: hex('E5E7EB') }];
divider.x = 48;
divider.y = 155;
cover.appendChild(divider);

// Version info
const version = figma.createText();
version.characters = "ТЗ v1.0 · Date · iOS 17+ · iPhone 15 Pro (393×852)";
version.fontSize = 14;
version.fontName = { family: "Inter", style: "Regular" };
version.fills = [{ type: 'SOLID', color: hex('6B7280') }];
version.x = 48;
version.y = 175;
cover.appendChild(version);

// Screen index, section headers, task list — continue pattern...
```
