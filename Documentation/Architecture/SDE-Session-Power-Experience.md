# SineOS Session & Power Experience

**Decision date:** 2026-10-07  
**Status:** frozen planning / mandatory for SDE 1.0  
**Master project:** SineOS Desktop Experience (SDE)  
**Master issue:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Target platform:** Debian 13 (Trixie) + XFCE 4.20 + X11 + LightDM

## Purpose

SineOS must present a coherent system experience from power-on to power-off.

The graphical identity must not disappear during:
- boot;
- login;
- lock;
- hibernation;
- resume;
- reboot;
- shutdown.

Normal use should not expose kernel/systemd status text unless diagnostic detail is explicitly requested or the system cannot continue normally.

Security and recovery always take priority over aesthetics.

---

# 1. Boot experience

## Normal boot

Use Plymouth as the graphical boot layer.

Expected flow:

```text
Firmware / UEFI
      ↓
GRUB (normally hidden/short)
      ↓
SineOS Plymouth
      ↓
LightDM / SineOS Login
      ↓
SDE Desktop
```

Normal graphical boot should show:
- SineOS branding;
- a subtle loading animation;
- optional short state text such as `Iniciando…`.

It should not normally show:
- kernel command output;
- initramfs messages;
- systemd unit status;
- scrolling boot logs.

## Diagnostic access

Boot messages are hidden, not removed.

Requirements:
- diagnostics remain accessible when needed;
- emergency/failure states must expose useful system output;
- recovery must not depend on Plymouth working;
- GRUB remains available as a recovery path.

A graphical failure must never hide a critical boot failure indefinitely.

---

# 2. Login experience

## Display manager

Keep LightDM.

Use Slick Greeter as the preferred greeter base unless implementation testing discovers a blocking limitation.

## User identity behavior

The normal login screen should:
- show/preselect the last valid local user or configured primary user;
- display the user name/avatar area;
- require the password every time;
- never store or autofill the password;
- provide a secondary `Cambiar usuario` path for multi-user systems.

The user must not normally retype the username on each login.

Autologin is not part of the default SDE experience.

## Visual integration

The login should use the same visual language as SDE:
- SineOS branding;
- SineOS wallpaper/background;
- Inter typography;
- SineOS accent/tokens;
- coherent spacing/radii;
- accessible contrast;
- keyboard focus states.

Login must remain usable if the optional visual layer fails.

---

# 3. Lock screen

## Locker

Use `xfce4-screensaver` as the preferred SDE locker.

Do not run competing lockers at the same time.

## Manual lock

`Super + L` locks the current session immediately.

Manual lock behavior:
- does not suspend;
- does not hibernate;
- does not log the user out;
- preserves running applications;
- hides sensitive desktop content;
- requires the current user's password to unlock.

## Lock screen UX

The lock screen should show:
- SineOS branding;
- current user identity;
- password field;
- time/date;
- battery/power status where useful;
- keyboard/layout indicator when relevant;
- accessibility entry point where supported.

It should not expose:
- window previews;
- message contents;
- terminal output;
- notifications with sensitive content.

Visual concept:

```text
SineOS
time / date

User
[ Password ]

Unlock
```

The lock screen should look related to login but remain clearly a locked-session state.

## Unlock security

Requirements:
- password is always required;
- Esc must not bypass lock;
- closing the prompt must not expose the session;
- authentication uses normal PAM/system mechanisms;
- visual customization must never replace or weaken authentication.

---

# 4. Hibernate on lid close

Closing the laptop lid should request **hibernation**, not suspension.

Default SDE policy:

```text
lid close
   ↓
hibernate
```

Before enabling this policy on a machine, SDE certification must verify:
- hibernation is supported;
- swap/resume configuration is valid;
- resume restores the session correctly;
- display state recovers;
- audio state recovers;
- panel/dock recover;
- compositor recovers.

SDE must not silently fall back to suspend if hibernation fails.

If hibernation is unavailable or broken, report it as a configuration/certification failure.

---

# 5. Resume experience

Expected flow:

```text
Power on / resume
      ↓
SineOS resume visual
      ↓
Resume Validation
      ↓
SineOS Lock Screen
      ↓
Password
      ↓
Existing session
```

After hibernation the user must authenticate before returning to the desktop.

## Resume Validation

Run one-shot validation after resume.

Check, as applicable:
- panel alive;
- compositor state;
- dock state;
- visible display topology;
- windows not stranded off-screen;
- valid audio output;
- no stale overlays;
- sane DPI/display configuration.

The validator exits when finished and must not become a permanent polling daemon.

Repairs should be scoped to the failed component.

---

# 6. AC power policy

SineOS uses TLP as the power-management policy layer.

Do not add a second competing power-policy daemon by default.

When connected to AC power, SDE intent is:

**Prioritize performance.**

This does not mean hardcoding a specific CPU governor on every machine.

The implementation must choose hardware-appropriate TLP settings based on the certified CPU/driver path.

Normal AC behavior may include:
- allowing CPU boost where appropriate;
- reducing aggressive power-saving constraints;
- prioritizing responsive performance;
- preserving thermal safety;
- preserving existing hardware protections.

User-facing state:

```text
Power connected
Energy mode: Performance
```

Feedback should be brief and non-intrusive.

---

# 7. Battery policy

When AC power is disconnected, SDE intent is:

**Prioritize battery efficiency while preserving usable responsiveness.**

User-facing state:

```text
On battery
Energy mode: Efficient
```

The switch should be automatic through TLP AC/BAT policy.

Initial battery-state policy:

| Battery | Default behavior |
|---|---|
| >20% | normal battery mode |
| <=20% | discreet low-battery warning |
| <=10% | critical warning |
| <=5% | emergency hibernation request |

Thresholds are configuration values, not hardcoded permanent constants.

A future implementation may adjust defaults after real hardware testing.

## Emergency hibernation

Emergency hibernation must only be enabled after hibernation has passed certification on the machine.

If safe hibernation is unavailable, SDE must not pretend that protection exists.

---

# 8. Screen blanking while locked

Locking the session and powering off the display are separate operations.

Expected behavior:
- `Super+L` locks immediately;
- screen may blank after a configurable inactivity interval;
- the machine remains running unless another explicit power policy applies;
- input wakes the display to the SineOS lock screen;
- password remains required.

---

# 9. Reboot and shutdown experience

Plymouth should also provide the graphical transition for reboot and poweroff when technically available.

Normal reboot:

```text
SineOS
Reiniciando…
```

Normal shutdown:

```text
SineOS
Apagando…
```

Normal use should not show scrolling systemd/kernel shutdown output.

However:
- critical shutdown errors must remain diagnosable;
- recovery/debug modes may expose detailed output;
- graphical polish must never prevent a clean shutdown.

---

# 10. Session continuity

The complete SineOS session lifecycle should feel coherent:

```text
POWER ON
   ↓
SineOS Boot
   ↓
SineOS Login
   ↓
SDE Desktop
   ↓
Lock / Hibernate / Resume
   ↓
SineOS Lock
   ↓
SDE Desktop
   ↓
SineOS Shutdown / Reboot
```

The system should not visually appear to switch between unrelated Debian/XFCE components during normal use.

---

# 11. Security rules

Mandatory:
- no password autofill;
- no default autologin;
- lock always requires password;
- resume from hibernation returns to locked session;
- PAM/system authentication remains authoritative;
- lock screen must not leak notification contents;
- logout and lock are distinct actions;
- no visual customization may weaken authentication or recovery.

---

# 12. Failure and recovery behavior

If Plymouth fails:
- boot continues with normal system output.

If Slick Greeter theme/integration fails:
- LightDM must remain usable with a known fallback greeter/configuration.

If xfce4-screensaver fails:
- SDE health/recovery must detect the issue;
- lock failure is considered a security defect;
- SDE must provide a documented fallback path.

If TLP policy application fails:
- system remains usable;
- SDE reports the failure;
- no competing power daemon is automatically enabled.

If hibernation fails certification:
- lid-close hibernation is not enabled until fixed.

---

# 13. SDE 1.0 acceptance criteria

## Boot
- graphical normal boot;
- no routine kernel/systemd text;
- diagnostic path remains available;
- GRUB/recovery remains accessible.

## Login
- last/primary user preselected;
- password always required;
- multi-user switch available;
- no autologin by default;
- visual consistency with SDE.

## Lock
- Super+L locks immediately;
- running session preserved;
- password required;
- sensitive content hidden;
- screen blanking independent from lock.

## Hibernate
- lid close requests hibernation;
- no silent suspend fallback;
- resume restores the existing session;
- lock screen shown after resume.

## Power
- AC policy prioritizes performance;
- BAT policy prioritizes efficiency;
- low/critical battery states visible;
- emergency hibernation only after certification.

## Shutdown / reboot
- graphical SineOS transition;
- normal shutdown text hidden;
- diagnostic output remains available when needed.

## Recovery
- login, lock and power customizations can be reverted to known-good system defaults;
- recovery does not depend on the graphical layer being functional.

---

# Final rule

> SineOS must feel like the same system from power-on to power-off, while authentication, recovery and power safety always remain more important than visual polish.
