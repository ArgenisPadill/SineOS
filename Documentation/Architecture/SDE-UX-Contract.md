# SineOS Desktop Experience — UX Contract

**Decision date:** 2026-10-07  
**Status:** frozen planning / mandatory for SDE 1.0  
**Master issue:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Target:** Debian 13 + XFCE 4.20 + X11 + LightDM

## Purpose

This document defines the user-experience contract for SineOS Desktop Experience (SDE).

SDE is not considered correct merely because it renders the intended visual design. It must also be predictable, responsive, recoverable, accessible and consistent under real daily use.

The contract exists to prevent recurring desktop UX failures seen across Windows, macOS and Linux environments: delayed feedback, surprise window movement, fragile customization, fragmented settings, display scaling problems, notification leaks while presenting, inconsistent toolkit behavior and recovery failures.

Community reports are treated as qualitative evidence, not statistical proof. The binding requirements are the rules and acceptance criteria defined below.

---

# Core UX rules

## 1. Immediate Feedback

Every user action must produce visible or otherwise perceptible feedback quickly enough that the user knows the input was received.

Examples:
- launching an app;
- opening Super+P;
- changing a display layout;
- mounting/unmounting storage;
- starting a capture or recording;
- applying SDE settings;
- repair/recovery actions.

An action that is accepted but produces no feedback is considered a UX defect.

## 2. No Dead Clicks

A click, keybinding or menu action must never appear to be ignored.

If the requested operation is still preparing, SDE must show an intermediate state such as:
- opening;
- detecting;
- applying;
- connecting;
- starting;
- waiting.

The intermediate state must not create a duplicate background operation when the same control is pressed repeatedly.

## 3. No Surprise Movement

SDE must not move, resize, maximize, minimize or change the workspace/monitor of a window without:
- explicit user intent; or
- a recovery condition that would otherwise leave the window inaccessible.

Valid recovery example:
- external monitor is disconnected;
- a window is now completely outside the visible desktop;
- SDE returns it to the primary visible work area.

Invalid example:
- reorganizing visible windows automatically because a new layout is considered aesthetically preferable.

## 4. Persistence

A normal reboot, logout/login, suspend/resume or package update must not arbitrarily reorganize:
- panel;
- dock;
- workspaces;
- visual preset;
- display preferences;
- application-state indicators.

Validated state changes must persist predictably.

## 5. One Setting, One Home

Each user-facing preference has exactly one authoritative owner and one documented source of truth.

SDE must avoid exposing the same setting independently through several conflicting interfaces.

Examples:
- blur intensity belongs to SDE appearance configuration;
- display topology belongs to SDE display configuration;
- SDE shortcuts belong to SDE shortcut configuration.

Underlying XFCE/Picom/Rofi configuration may still exist, but SDE-generated values must not create competing sources of truth.

## 6. Safe Automation

Automation must be:
- understandable;
- reversible when practical;
- limited to the smallest necessary scope;
- visible to the user when it changes meaningful state.

Important automatic changes should offer Undo/Revert where feasible.

Examples:
- changing HDMI audio output;
- applying a display layout;
- repairing a panel profile.

## 7. Graceful Failure

A visual or optional component may fail without making the desktop unusable.

The existing degradation contract remains mandatory:
- Picom failure -> XFWM compositor;
- Global Menu failure/incompatibility -> application-local menu;
- Docklike failure -> usable XFCE panel/window access;
- Rofi failure -> Whisker;
- Flameshot failure -> xfce4-screenshooter;
- wireless display failure -> wired display remains usable.

## 8. State Recovery

SDE maintains an operational **Last Known Good** state separate from historical backups.

Last Known Good exists to recover normal desktop operation quickly after:
- failed configuration apply;
- bad display topology;
- broken visual setting;
- incomplete migration;
- failed resume repair.

Historical backup and Last Known Good are separate concepts.

## 9. Accessible State

Important state must never be communicated by color alone.

Use a combination of:
- shape;
- position;
- icon;
- label;
- line/indicator weight;
- color.

This applies especially to:
- Docklike active/inactive state;
- attention requests;
- selected workspace;
- success/warning/error;
- display selection.

## 10. Context Awareness

SDE may adapt behavior to context when that adaptation is predictable and reversible.

Contexts include:
- fullscreen;
- projector/external display;
- duplicate display;
- battery state;
- suspend/resume;
- recording/capture;
- reduced motion.

Context awareness must never silently change unrelated preferences.

## 11. Toolkit Tolerance

GTK3, GTK4, Qt5, Qt6, Chromium/Electron and other toolkits may not look identical.

SDE prioritizes:
1. correct behavior;
2. legibility;
3. predictable keyboard/mouse interaction;
4. visual coherence.

Forcing perfect visual uniformity is forbidden when it breaks application behavior.

## 12. Performance Is UX

A visually polished feature that causes visible lag, delayed input, stutter or excessive resource use is considered defective.

Performance testing is part of UX certification, not a separate optional optimization stage.

---

# Latency budget

Initial engineering targets:

| Interaction | Target |
|---|---:|
| input acknowledgement | <= 100 ms |
| menu / Rofi / Super+P visible response | <= 150 ms target |
| short local operation | <= 500 ms without blocking interaction |
| operation > 500 ms | show visible state/progress |
| operation > 2 s | show progress and Cancel when technically safe |

Rules:
- animations must not delay command execution;
- input must be processed before decorative motion completes;
- repeated input must not spawn duplicate operations;
- expensive status collection must not run on the UI path.

These are SDE engineering targets and must be validated on the supported hardware matrix.

---

# Display Transaction

Display changes are transactional.

Applicable to:
- resolution;
- refresh rate;
- duplicate;
- extend;
- primary display;
- major topology changes.

Flow:

```text
capture current known-good display state
        ↓
apply proposed state
        ↓
validate outputs
        ↓
show confirmation
        ↓
Keep / Revert
        ↓
timeout -> automatic revert
```

Initial confirmation timeout target: approximately 15 seconds; implementation may adjust after usability testing.

A failed graphical confirmation must not permanently strand the user on an unusable display state.

Display recovery must also be available from TTY/recovery tooling.

---

# Last Known Good desktop state

SDE should track a compact operational state containing, as applicable:
- panel profile;
- dock layout;
- visual preset;
- SDE schema version;
- compositor mode;
- display topology;
- DPI/scale state;
- workspaces;
- display-associated audio preference.

After a configuration passes validation, it may be promoted to Last Known Good.

On startup or repair:
- validate current state;
- repair only the broken area when possible;
- avoid resetting unrelated preferences.

---

# Resume Validation

After suspend/resume, SDE performs a one-shot validation.

Checks may include:
- xfce4-panel alive;
- compositor state valid;
- display outputs/topology valid;
- no windows fully outside visible work areas;
- audio output still valid;
- dock state valid;
- no stale SDE overlay;
- DPI state sane.

The validator exits after completion. It is not a permanent polling daemon.

Repairs must be scoped and logged locally.

---

# Display and audio coordination

Display topology and audio output are related but distinct.

SDE may remember a local preference for a known display context, for example:

```text
Projector
- extended
- native/common certified resolution
- audio remains on laptop
```

or:

```text
TV
- duplicate
- audio over HDMI
```

Rules:
- never export device identifiers as portable profile data;
- automatic audio changes should provide visible feedback;
- offer Undo when practical;
- a missing audio device must fall back to a valid output rather than fail the display transaction.

---

# Notification privacy and interruption policy

External display presence changes privacy risk.

SDE must support a projection-safe notification policy without creating a separate "teacher mode".

When duplicating/projecting:
- sensitive notification content may be hidden;
- generic app notification may still be shown;
- the original notification remains available on the primary system where technically viable.

Fullscreen behavior:
- non-urgent banners should not cover fullscreen content unnecessarily;
- notifications should remain retrievable rather than being silently lost.

Privacy behavior must be explicit and user-configurable.

---

# Edit Mode

Panel/dock structural editing must not be accidentally available during normal use.

Normal state:
- layout locked against accidental dragging/removal.

Edit flow:
```text
SineOS Settings
  -> Personalize desktop
  -> Edit layout
```

Entering Edit Mode should create a lightweight restore point.

Required controls:
- Save;
- Undo/Revert;
- Restore SineOS layout.

Exiting Edit Mode re-locks protected structure.

---

# Interaction target sizes

Small visual icons may have larger invisible/transparent hit targets.

Initial desktop target:
- clickable controls should normally provide at least approximately 32x32 px effective pointer target where layout permits.

Future touch-oriented layouts should target approximately 44x44 px or equivalent physical size.

This does not require icons themselves to be visually large.

---

# Snap behavior

Snap Preview must require clear pointer/keyboard intent.

Rules:
- no premature resize while merely approaching an edge;
- preview before apply;
- apply on release/confirmation;
- preserve current window until the operation is committed;
- snap layout must use the active monitor work area;
- Esc cancels overlays when applicable.

SDE prioritizes predictable snapping over aggressive automation.

---

# Dock state semantics

Docklike indicators must be understandable without relying only on accent color.

Conceptual states:

```text
closed             no running indicator
open/inactive      short indicator
active             stronger indicator
multiple windows   indicator + count/shape
attention          temporary pulse/symbol
```

Attention animations:
- short;
- self-terminating;
- no endless flashing;
- disabled/reduced under Reduced Motion.

---

# Settings information architecture

SDE settings should present user concepts, not implementation technologies.

Preferred top-level concepts:
- Appearance;
- Displays;
- Audio;
- Mouse & Keyboard;
- Notifications;
- Accessibility;
- Shortcuts;
- Desktop / Layout;
- Advanced SDE.

Avoid requiring the user to understand:
- Picom internals;
- XRandR syntax;
- XFConf paths;
- GTK CSS;
- Rofi config files.

Advanced technical controls may exist behind an explicit advanced section.

---

# Toolkit workflow certification

Certification must test tasks, not only screenshots.

At minimum validate these workflows across relevant toolkit families:
- Open file;
- Save As;
- Choose folder;
- Cancel dialog;
- keyboard navigation;
- Esc behavior;
- clipboard;
- drag-and-drop;
- fullscreen;
- file picker scaling.

Families:
- XFCE/GTK3;
- GTK4;
- Qt5;
- Qt6;
- Chromium;
- Electron;
- Firefox where behavior differs materially.

---

# UX acceptance tests for SDE 1.0

SDE 1.0 must demonstrate:

## Responsiveness
- no dead clicks in primary shell interactions;
- launcher and Super+P acknowledge input within target budget on certified hardware;
- slow operations expose progress/state.

## Predictability
- no arbitrary window movement;
- normal reboot does not reorganize panel/dock;
- settings have one authoritative owner.

## Displays
- Display Transaction with automatic rollback;
- lost-window recovery;
- display changes do not silently corrupt audio preference;
- projector/duplicate privacy policy works as designed.

## Resume
- one-shot Resume Validation completes;
- repair does not reset unrelated user state.

## Accessibility
- important state is distinguishable without color alone;
- Reduced Motion is respected;
- keyboard navigation remains usable.

## Failure
- broken optional component does not remove desktop access;
- Last Known Good restore works;
- local recovery and certified GitHub recovery remain available.

## Toolkit behavior
- certified workflows pass on the application/toolkit matrix.

## Performance
- UX latency and resource budgets meet certification thresholds.

---

# Design anti-patterns forbidden in SDE baseline

- silent state changes;
- infinite attention flashing;
- UI actions that require clicking twice because the first click has no feedback;
- settings duplicated across competing frontends;
- automatic window rearrangement without recovery necessity;
- irreversible display changes without confirmation;
- mandatory third-party extension for critical desktop function;
- color-only state indicators;
- animations that block input;
- background polling where an event/one-shot action is sufficient;
- update behavior that resets the user's valid layout without migration.

---

# References informing the contract

Normative behavior is defined by this document; external sources are context only.

- Microsoft responsiveness guidance: https://learn.microsoft.com/windows/apps/develop/performance/responsive
- Windows notifications and Do Not Disturb: https://support.microsoft.com/windows/experience/notifications-and-do-not-disturb-in-windows
- Existing SDE specifications:
  - `Documentation/Architecture/SineOS-Desktop-Experience.md`
  - `Documentation/Architecture/SDE-Visual-Interaction-Refinements.md`
  - `Documentation/Architecture/SDE-Packaging-Recovery-Certification.md`

## Final rule

> SineOS should be simple when the user only wants to work, powerful when the user chooses to go deeper, and predictable at all times.
