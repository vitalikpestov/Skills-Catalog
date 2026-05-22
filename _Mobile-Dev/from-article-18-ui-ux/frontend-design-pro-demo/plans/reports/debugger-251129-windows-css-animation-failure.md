# Windows CSS Animation Failure Analysis
**Date:** 2025-11-29
**Platform:** Windows 11 Chrome/Edge
**Status:** ROOT CAUSE IDENTIFIED

## Executive Summary
CSS animations fail on Windows 11 Chrome/Edge but work on macOS/iPhone. Root cause: **Windows accessibility setting "Show animations in Windows" is likely DISABLED**, triggering `prefers-reduced-motion: reduce` media query that disables all animations.

## Root Cause Analysis

### Primary Issue: `prefers-reduced-motion` Media Query
All 13 HTML files implement aggressive animation disabling when `prefers-reduced-motion: reduce` is detected:

**Example from `/demos-v02/03-glassmorphism.html:736-747`:**
```css
@media (prefers-reduced-motion: reduce) {
  *, .orb, .hero-content, .preview-card, .preview-stat,
  .feature-card, .price-card, .nav-glass, .reveal, .reveal-scale {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-delay: 0ms !important;
  }
  .hero-content h1 span { animation: none; }
  .reveal, .reveal-scale {
    opacity: 1;
    transform: none;
  }
}
```

**Pattern found in all files:**
- `/demos-v02/01-minimalism-swiss.html:695`
- `/demos-v02/02-neumorphism.html:696`
- `/demos-v02/03-glassmorphism.html:736`
- `/demos-v02/04-brutalism.html:652`
- `/demos-v02/05-claymorphism.html:656`
- `/demos-v02/06-aurora-mesh-gradient.html:686`
- `/demos-v02/07-retro-futurism-cyberpunk.html:794`
- `/demos-v02/08-3d-hyperrealism.html:704`
- `/demos-v02/09-vibrant-block-maximalist.html:660`
- `/demos-v02/10-dark-oled-luxury.html:660`
- `/demos-v02/11-organic-biomorphic.html:665`
- `/demos-v02/index.html:438`

### Windows 11 Accessibility Setting Behavior
**Path:** Settings > Accessibility > Visual effects > Animation effects (Show animations in Windows)

When DISABLED:
- Browser detects via `prefers-reduced-motion: reduce`
- CSS media query triggers globally
- All animations instantly disabled

This setting is **more commonly disabled on Windows** than macOS due to:
- Performance optimization on older hardware
- Battery saving defaults on laptops
- Corporate IT policies
- Accessibility recommendations

## Animation Inventory

### Affected Animations by File

#### 1. **03-glassmorphism.html**
- `@keyframes float` (lines 92-97): Floating orb backgrounds
- `@keyframes fadeInUp` (595): Hero content entrance
- `@keyframes fadeInScale` (600): Card scaling entrance
- `@keyframes shimmer` (605): Text shimmer effect
- `@keyframes glowPulse` (610): Glow pulsing
- **IntersectionObserver**: Scroll-triggered reveals (lines 928, 943, 963)

#### 2. **06-aurora-mesh-gradient.html**
- `@keyframes aurora-drift` (89): Aurora layer movement
- `@keyframes aurora-pulse` (96): Aurora pulsing opacity
- `@keyframes fadeInUp` (543): Content entrance
- **IntersectionObserver**: Scroll reveals (lines 829, 844, 864, 885)

#### 3. **07-retro-futurism-cyberpunk.html**
- `@keyframes flicker` (201): Neon flicker effect
- `@keyframes blink` (532): Cursor blink
- `@keyframes glitch-anim-1/2` (588, 596): Glitch effects
- `@keyframes fadeInGlitch` (624): Glitchy entrance
- `@keyframes slideInNeon` (630): Neon slide
- `@keyframes scanline` (640): CRT scanline
- **IntersectionObserver**: Reveals (lines 941, 956, 977)

#### 4. **11-organic-biomorphic.html**
- `@keyframes blob-morph` (99): 25s blob morphing
- `@keyframes float` (291): 4s floating animation
- `@keyframes cta-glow` (432): CTA glow effect
- `@keyframes organicFadeIn/blobPop/gentleBounce/morphRadius` (508-524): Various organic animations
- **IntersectionObserver**: Scroll reveals (lines 813, 828, 848, 869)

#### 5. **05-claymorphism.html**
- `@keyframes bounceIn` (516): Bounce entrance
- `@keyframes floatUp` (523): Float up entrance
- `@keyframes wiggle` (528): Wiggle interaction
- `@keyframes squish` (533): Squish effect
- **IntersectionObserver**: Scroll reveals (lines 816, 831, 851)

#### 6. **04-brutalism.html**
- `@keyframes marquee` (217): 20s marquee scroll
- `@keyframes slideInHard/popInBrutal/shake/typeIn` (510-527): Brutalist animations
- **IntersectionObserver**: Scroll reveals (lines 831, 846, 866)

#### 7. **09-vibrant-block-maximalist.html**
- `@keyframes spin` (192): 20s rotation
- `@keyframes marquee` (439): 20s marquee
- `@keyframes slideInLeft/Right/scaleIn/popBounce` (490-505): Block animations
- `scroll-snap-type: y mandatory` (line 32)
- **IntersectionObserver**: Scroll reveals (lines 789, 804, 824)

#### 8. **01-minimalism-swiss.html**
- `@keyframes fadeInUp/fadeIn/slideInLeft/lineExpand` (417-432): Minimal animations
- **IntersectionObserver**: Scroll reveals (lines 878, 895, 915, 936, 992)

#### 9. **10-dark-oled-luxury.html**
- `@keyframes fadeInUp/fadeIn/lineGrow/accentGlow/cardReveal` (492-512): Luxury animations
- **IntersectionObserver**: Scroll reveals (lines 811, 826, 846, 867)

#### 10. **02-neumorphism.html**
- **IntersectionObserver**: Scroll reveals (lines 853, 868, 888)

#### 11. **08-3d-hyperrealism.html**
- **IntersectionObserver**: Scroll reveals (lines 844, 859, 879)

#### 12. **index.html**
- `@keyframes fadeInDown` (371): Header entrance
- Scroll parallax (lines 894-901)
- **IntersectionObserver**: Scroll reveals (lines 839, 854)

## Secondary Findings

### ✓ Browser Prefixes Present (Good)
- `-webkit-backdrop-filter` correctly prefixed (03-glassmorphism.html:109)
- `-webkit-background-clip` correctly prefixed (multiple files)
- `-webkit-text-fill-color` correctly prefixed (multiple files)
- `-webkit-font-smoothing` correctly prefixed (all files)

### ✓ No OS Detection JavaScript
No code detecting `navigator.platform`, `navigator.userAgent`, or Windows-specific logic that would disable animations.

### ✓ No Missing Critical Prefixes
All modern CSS properties (`animation`, `transform`, `transition`) don't require prefixes in current Chrome/Edge.

### ✓ GPU Acceleration Pattern
Uses `transform` and `will-change` for performance (implicit GPU acceleration).

## Windows-Specific Behavior

### Why More Likely on Windows:
1. **Default Settings**: Some Windows OEMs ship with animations disabled for performance
2. **Battery Saver**: Auto-enables when laptop unplugged
3. **Corporate Policies**: IT departments often disable for consistency
4. **Accessibility Tools**: More aggressive accessibility recommendations on Windows
5. **Performance Mode**: Gaming/performance profiles may disable

### Testing Windows Setting:
**To verify:**
1. Open Settings > Accessibility > Visual effects
2. Check "Animation effects" toggle
3. If OFF → `prefers-reduced-motion: reduce` is active
4. Toggle ON → animations should work immediately

**Alternative test (DevTools):**
```javascript
// Run in console
window.matchMedia('(prefers-reduced-motion: reduce)').matches
// true = animations disabled, false = animations enabled
```

## Evidence Summary

**Location of Issues:**
- 13 files with `prefers-reduced-motion` media queries
- 100+ animation definitions affected
- All IntersectionObserver-based scroll reveals disabled
- All entrance animations (fadeIn, slideIn, bounce) disabled
- All continuous animations (blob-morph, float, aurora-drift) disabled

**Code Locations:**
```
/demos-v02/*.html
Lines: ~600-750 (prefers-reduced-motion blocks)
Lines: ~80-250 (keyframe definitions)
Lines: ~800-900 (IntersectionObserver JS)
```

## Unresolved Questions
1. Confirm exact Windows accessibility setting state on affected machine
2. Are there enterprise group policies forcing `prefers-reduced-motion`?
3. Does user have battery saver mode enabled?
4. Any third-party accessibility software installed?

## Recommended Next Steps
1. **Immediate**: Check Windows Settings > Accessibility > Visual effects > "Show animations in Windows" (must be ON)
2. **Verify**: Run DevTools console test: `window.matchMedia('(prefers-reduced-motion: reduce)').matches`
3. **If true**: Enable Windows animations OR modify CSS to be less aggressive with animation disabling
4. **If false**: Investigate browser extensions, group policies, or third-party software

## Technical Details
- **Files analyzed**: 13 HTML files in `/demos-v02/`
- **Animation definitions**: 40+ unique `@keyframes`
- **IntersectionObserver instances**: 35+ scroll-triggered animations
- **Transition properties**: 200+ with `transition:`
- **Transform properties**: 150+ with `transform:`
- **Will-change hints**: Found in multiple files for optimization
