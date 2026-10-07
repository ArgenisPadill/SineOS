# SineOS Desktop Experience — Packaging, Recovery, Certification and Release Policy

**Decision date:** 2026-10-07  
**Status:** frozen planning / implementation pending  
**Master issue:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Target platform:** Debian 13 (Trixie) + XFCE 4.20 + X11 + LightDM

## Principle

SineOS Desktop Experience (SDE) is treated as an operational subsystem of SineOS, not as cosmetic theming.

Every SDE feature must have:
- a declared package owner;
- an install path;
- a validation path;
- a failure mode;
- a rollback path;
- a recovery path;
- a documented support status.

Visual improvements are accepted only when they preserve XFCE as a usable fallback.

---

# Package architecture

SDE will be split into small Debian packages instead of one monolithic installer.

## 1. sineos-desktop

Meta-package for the supported SDE experience.

Responsibilities:
- depend on the required SDE packages;
- provide one entry point for install/upgrade/remove;
- contain no fragile runtime logic of its own.

Expected relationship:
- Depends: sineos-desktop-core, sineos-desktop-visual, sineos-desktop-assets, sineos-desktop-recovery
- Recommends: sineos-desktop-tools
- Suggests: optional modules such as advanced recording, wireless display and experimental overview where appropriate.

## 2. sineos-desktop-core

Critical desktop integration.

Contains or manages:
- SDE configuration schema;
- CLI;
- XFCE integration;
- panel/layout application logic;
- Global Menu policy/fallback;
- display backend integration;
- config generation;
- safe-area calculations;
- migration framework;
- health/status interfaces.

It must remain usable without optional visual tools.

## 3. sineos-desktop-visual

Visual integration layer.

Contains or manages:
- Picom configuration;
- XFWM decoration;
- GTK CSS;
- Qt integration templates;
- Docklike/Genmon layout definitions;
- Rofi visual definitions used by SDE;
- SineOS Materials;
- Motion/Focus/Reduced Motion policies;
- OSD visual definitions.

A failure here must not prevent XFCE from starting.

## 4. sineos-desktop-assets

Architecture-independent assets.

Contains:
- SineOS logo assets;
- wallpapers;
- cursor sources and compiled XCursor assets;
- SineOS-specific icons;
- theme overlays;
- reusable SVG sources.

Do not duplicate fonts already distributed by Debian when a package dependency is sufficient.

## 5. sineos-desktop-tools

Meta/integration package for user tools.

Default tools may include:
- Flameshot;
- vokoscreenNG;
- Gromit-MPX;
- capture/display helper scripts.

Advanced or non-essential tools should remain Recommends/Suggests where appropriate.

Examples of optional tools:
- OBS;
- wireless display backend;
- experimental/candidate Overview implementation.

## 6. sineos-desktop-recovery

Minimal recovery package. This package is critical and must have as few dependencies as possible.

Contains:
- known-good XFCE fallback configuration;
- backup/restore logic;
- SDE health checks;
- safe-mode command;
- rollback command;
- repair command;
- local recovery metadata.

It must not depend on Picom, Rofi, Docklike, OBS, wireless display or other optional visual components.

The recovery package remains installed while SDE is installed.

---

# Debian dependency policy

Use package relationship semantics intentionally:

- **Depends**: SDE cannot provide its defined function without the dependency.
- **Recommends**: part of the normal supported experience but SDE remains operable without it.
- **Suggests**: optional enhancement.

Reference:
- Debian Policy, package relationships: https://www.debian.org/doc/debian-policy/ch-relationships.html

Packages and maintainer scripts must be idempotent. Running installation or recovery again must converge toward the desired state rather than duplicate or corrupt configuration.

Reference:
- Debian Policy, maintainer script idempotency: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html

---

# Recovery model

The recovery experience intentionally preserves the proven SineOS pattern:

> Clone a known SineOS state from GitHub and execute a recovery shell script.

However, recovery must not depend exclusively on Internet access or the moving `main` branch.

## Recovery path A — local recovery

Preferred when available.

Possible interface:

```bash
sineos-desktop safe-mode
sineos-desktop health
sineos-desktop repair
sineos-desktop rollback
```

The recovery package keeps enough local data to:
- stop/disable a failing Picom session;
- restore XFWM compositing;
- restore a known-good panel profile;
- disable broken SDE autostart entries;
- restore the last certified SDE backup;
- restore the pre-SDE XFCE backup;
- report what it changed.

This path must work without network access.

## Recovery path B — GitHub bootstrap

Used from a TTY or functional terminal when local recovery is damaged or unavailable.

Conceptual flow:

```bash
git clone --branch <certified-release-or-tag> <SineOS repository>
cd SineOS
sudo ./<recovery-bootstrap>.sh
```

The final file name is implementation detail, but the script should support operations such as:

```text
diagnose
repair
restore-last-good
restore-pre-sde
verify
```

Rules:
- never recover production from an unpinned `main` checkout;
- use a release tag or explicit certified commit;
- display the commit/tag being used before changing the system;
- verify required files and checksums where applicable;
- create a fresh backup before repair when the filesystem permits;
- print every destructive action;
- be safe to run more than once;
- work from TTY without requiring the graphical session.

## Recovery path C — external/offline media

For complete network failure or repository unavailability, SDE should permit recovery from:
- a cached release bundle;
- a USB copy of the certified release;
- a previously downloaded SDE recovery package.

This avoids turning GitHub into a single point of recovery failure.

## Recovery levels

### Level 0 — Diagnose
Read-only inspection.

### Level 1 — Repair visual session
Restore compositor/panel/autostart without overwriting user data.

### Level 2 — Restore last known-good SDE state
Use the last certified local SDE backup.

### Level 3 — Restore pre-SDE XFCE
Return the user to the backed-up functional XFCE baseline.

### Level 4 — Re-bootstrap from certified GitHub release
Rebuild SDE from a pinned release/tag/commit.

---

# Backup contract

Before installation, migration or repair that changes desktop state, SDE must record:
- SDE version;
- Git commit or package version;
- XFCE configuration backup;
- panel profile;
- Picom state;
- SDE configuration schema version;
- installed SDE package versions;
- timestamp;
- host-local display metadata separately from portable preferences.

Recovery backups must never include secrets unnecessarily.

---

# Release lifecycle

SDE will use four engineering stages.

## Alpha

Purpose:
- architecture;
- package split;
- installer;
- recovery;
- basic visual integration.

Rules:
- may contain incomplete features;
- may change schema;
- not declared daily-use safe;
- must already support recovery.

Suggested Git tag pattern:
`sde-v0.1.0-alpha.1`

Suggested Debian package version:
`0.1.0~alpha1-1`

## Beta

Purpose:
- feature-complete candidate for sustained daily use;
- visual and behavioral integration mostly frozen;
- compatibility bugs still expected.

Entry gate:
- installation is idempotent;
- uninstall works;
- local recovery works;
- GitHub bootstrap recovery works;
- baseline multimonitor works;
- no known critical data-loss/config-loss issue.

Suggested range:
`sde-v0.5.x-beta.N`

## Release Candidate (RC)

Purpose:
- expected final 1.0 behavior;
- no new features unless required to fix a release blocker.

Entry gate:
- hardware certification matrix substantially complete;
- RAM/CPU/GPU budgets measured;
- suspend/resume certified on target hardware;
- HDMI hot-plug certified;
- rollback and clean reinstall certified;
- documentation complete enough to recover without this conversation.

Suggested range:
`sde-v0.9.x-rc.N`

## Stable

First stable:
`sde-v1.0.0`

Stable means:
- reproducible install;
- supported recovery;
- certified compatibility matrix;
- documented dependencies;
- defined resource budget;
- no release-blocking failures;
- migration path to the next supported version.

No feature is promoted to Stable solely because it looks finished.

## Debian version ordering

Use Debian's tilde convention for pre-releases so they sort before the final release.

Examples:
- `1.0.0~alpha1-1`
- `1.0.0~beta1-1`
- `1.0.0~rc1-1`
- `1.0.0-1`

Debian Policy explicitly defines `~` to sort before the final version.

Reference:
- https://www.debian.org/doc/debian-policy/ch-controlfields.html

---

# Certification model

SDE certification is capability-based, not marketing language.

## C0 — Boot and fallback
Required:
- login;
- logout;
- reboot;
- XFCE starts;
- fallback compositor works;
- SDE can be disabled without losing the desktop.

## C1 — Desktop UX
Required:
- panel;
- dock;
- Global Menu fallback;
- Rofi fallback;
- GTK/Qt baseline;
- OSD;
- CSD/SSD handling;
- Snap/Overview behavior applicable to the tested release.

## C2 — Displays
Required:
- internal display;
- HDMI hot-plug;
- duplicate;
- extend;
- internal-only;
- projector test;
- resolution change;
- lost-window recovery.

Wireless display is certified separately and does not block wired-display certification.

## C3 — Performance
Measure:
- idle RAM delta;
- idle CPU delta;
- compositor GPU load;
- login time;
- fullscreen/video impact;
- dual-monitor impact;
- capture/recording impact.

A test does not pass merely because the system remains responsive; it must meet the defined SDE budget.

## C4 — Suspend and resilience
Required:
- suspend;
- resume;
- display state recovery;
- compositor recovery;
- panel recovery;
- network/audio UI recovers normally;
- no orphaned overlays or stale display geometry.

## C5 — Recovery and replication
Required:
- second install run is safe/idempotent;
- local safe-mode works;
- local rollback works;
- GitHub bootstrap restore works;
- offline recovery bundle works;
- uninstall restores a functional XFCE state;
- clean Debian 13 install can reproduce the certified SDE release.

---

# Hardware support states

A hardware configuration can be labelled:

## Certified
Passed the complete applicable certification suite.

## Compatible
Known to work for core functionality but not fully certified.

## Experimental
A feature/hardware path is under validation and may have known limitations.

## Unsupported
Known not to meet SDE requirements or outside project scope.

The support label must include:
- GPU/vendor/driver path where relevant;
- resolution/display topology;
- SDE release;
- Debian release;
- date of certification.

---

# Release blocking rules

A release cannot advance to Stable with:
- login failure;
- unrecoverable panel failure;
- unrecoverable compositor failure;
- broken rollback;
- broken uninstall;
- regression that leaves windows inaccessible after normal HDMI hot-plug;
- critical CSD/SSD issue that makes common apps unusable;
- resource usage above agreed budget without explicit waiver;
- configuration migration that can destroy the previous working state;
- dependency on an unpinned Git branch;
- undocumented mandatory dependency.

---

# CI and release artifacts

Planning target:
- lint shell/scripts;
- validate package metadata;
- build .deb artifacts;
- validate config schema/templates;
- test idempotence where automatable;
- publish checksums;
- attach release notes;
- attach package manifest;
- record upstream dependency versions;
- preserve recovery bootstrap script with each release.

A release should be reconstructible from repository state plus documented upstream sources.

---

# Naming convention

Project:
**SineOS Desktop Experience (SDE)**

Packages:
- `sineos-desktop`
- `sineos-desktop-core`
- `sineos-desktop-visual`
- `sineos-desktop-assets`
- `sineos-desktop-tools`
- `sineos-desktop-recovery`

Optional modules can use:
- `sineos-desktop-<feature>`

Release stages:
**Alpha → Beta → RC → Stable**

These names describe engineering maturity, not visual quality.

---

# Final rule

> A SineOS Desktop Experience release is not certified because it installs successfully. It is certified only when it can also fail safely, recover predictably and be reproduced from documented inputs.
