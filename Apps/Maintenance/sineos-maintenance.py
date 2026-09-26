#!/usr/bin/env python3

import argparse
import subprocess
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import maintenance_core as core

APP_TITLE = "SineOS · Mantenimiento"


def fmt_day(value):
    return value.strftime("%d-%m-%Y") if value else "—"


def short_commit(value):
    return value[:12] if value else "—"


class StatusRow(Gtk.Box):
    def __init__(self, title):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.set_hexpand(True)
        text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        text.set_hexpand(True)
        self.title = Gtk.Label(label=title)
        self.title.set_xalign(0)
        self.title.get_style_context().add_class("row-title")
        self.detail = Gtk.Label()
        self.detail.set_xalign(0)
        self.detail.set_line_wrap(True)
        self.detail.get_style_context().add_class("secondary")
        text.pack_start(self.title, False, False, 0)
        text.pack_start(self.detail, False, False, 0)
        self.badge = Gtk.Label()
        self.badge.get_style_context().add_class("badge")
        self.pack_start(text, True, True, 0)
        self.pack_end(self.badge, False, False, 0)

    def set_state(self, detail, badge, css):
        self.detail.set_text(detail)
        self.badge.set_text(badge)
        ctx = self.badge.get_style_context()
        for name in ("badge-ok", "badge-warn", "badge-pending", "badge-neutral"):
            ctx.remove_class(name)
        ctx.add_class(css)


class MaintenanceWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_TITLE)
        self.set_default_size(680, 570)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.load_css()
        self.build_ui()
        self.refresh()

    def load_css(self):
        css = b"""
        window { background-color: @theme_bg_color; }
        .page { padding: 26px 30px; }
        .title { font-size: 22px; font-weight: 700; }
        .subtitle, .secondary, .technical { color: @theme_fg_color; opacity: 0.68; }
        .hero { padding: 17px 18px; border-radius: 11px; border: 1px solid alpha(@theme_fg_color, 0.12); background-color: alpha(@theme_fg_color, 0.035); }
        .hero-title { font-size: 17px; font-weight: 700; }
        .section { font-size: 11px; font-weight: 700; letter-spacing: 1px; opacity: 0.58; }
        .row-title { font-weight: 700; }
        .status-row { padding: 12px 0; }
        .badge { font-size: 11px; font-weight: 700; padding: 5px 9px; border-radius: 12px; }
        .badge-ok { background-color: alpha(@success_color, 0.20); }
        .badge-warn { background-color: alpha(@error_color, 0.18); }
        .badge-pending { background-color: alpha(@warning_color, 0.18); }
        .badge-neutral { background-color: alpha(@theme_fg_color, 0.08); }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def build_ui(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        page.get_style_context().add_class("page")
        self.add(page)

        title = Gtk.Label(label="Mantenimiento de SineOS")
        title.set_xalign(0)
        title.get_style_context().add_class("title")
        subtitle = Gtk.Label(label="Auditoría trimestral, respaldo externo y validación con GitHub")
        subtitle.set_xalign(0)
        subtitle.get_style_context().add_class("subtitle")
        page.pack_start(title, False, False, 0)
        page.pack_start(subtitle, False, False, 0)

        hero = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        hero.get_style_context().add_class("hero")
        self.hero_title = Gtk.Label()
        self.hero_title.set_xalign(0)
        self.hero_title.get_style_context().add_class("hero-title")
        self.hero_detail = Gtk.Label()
        self.hero_detail.set_xalign(0)
        self.hero_detail.set_line_wrap(True)
        self.hero_detail.get_style_context().add_class("secondary")
        hero.pack_start(self.hero_title, False, False, 0)
        hero.pack_start(self.hero_detail, False, False, 0)
        page.pack_start(hero, False, False, 0)

        health_label = Gtk.Label(label="SALUD TRIMESTRAL")
        health_label.set_xalign(0)
        health_label.get_style_context().add_class("section")
        page.pack_start(health_label, False, False, 0)

        self.health_row = StatusRow("Auditoría profunda")
        self.health_row.get_style_context().add_class("status-row")
        page.pack_start(self.health_row, False, False, 0)

        health_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.audit_button = Gtk.Button(label="Ejecutar auditoría")
        self.audit_button.connect("clicked", self.on_run_audit)
        self.adopt_button = Gtk.Button(label="Adoptar validación actual")
        self.adopt_button.connect("clicked", self.on_adopt)
        self.sync_button = Gtk.Button(label="Registrar y sincronizar con GitHub")
        self.sync_button.connect("clicked", self.on_sync)
        health_actions.pack_start(self.audit_button, False, False, 0)
        health_actions.pack_start(self.adopt_button, False, False, 0)
        health_actions.pack_start(self.sync_button, False, False, 0)
        page.pack_start(health_actions, False, False, 0)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        page.pack_start(sep, False, False, 0)

        backup_label = Gtk.Label(label="RESPALDO EXTERNO")
        backup_label.set_xalign(0)
        backup_label.get_style_context().add_class("section")
        page.pack_start(backup_label, False, False, 0)

        self.backup_row = StatusRow("SineOsBackups")
        self.backup_row.get_style_context().add_class("status-row")
        page.pack_start(self.backup_row, False, False, 0)

        self.backup_button = Gtk.Button(label="Ejecutar respaldo externo")
        page.pack_start(self.backup_button, False, False, 0)

        self.details = Gtk.Expander(label="Detalles técnicos")
        details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.git_detail = Gtk.Label()
        self.git_detail.set_xalign(0)
        self.git_detail.set_selectable(True)
        self.git_detail.get_style_context().add_class("technical")
        self.report_detail = Gtk.Label()
        self.report_detail.set_xalign(0)
        self.report_detail.set_selectable(True)
        self.report_detail.set_line_wrap(True)
        self.report_detail.get_style_context().add_class("technical")
        details_box.pack_start(self.git_detail, False, False, 0)
        details_box.pack_start(self.report_detail, False, False, 0)
        self.details.add(details_box)
        page.pack_start(self.details, False, False, 0)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        refresh = Gtk.Button(label="Actualizar")
        refresh.connect("clicked", lambda *_: self.refresh())
        close = Gtk.Button(label="Cerrar")
        close.connect("clicked", lambda *_: self.close())
        footer.pack_start(refresh, False, False, 0)
        footer.pack_end(close, False, False, 0)
        page.pack_end(footer, False, False, 0)

    def message(self, title, detail, error=False):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.ERROR if error else Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(detail)
        dialog.run()
        dialog.destroy()

    def confirm(self, title, detail, action):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.NONE,
            text=title,
        )
        dialog.format_secondary_text(detail)
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button(action, Gtk.ResponseType.OK)
        result = dialog.run() == Gtk.ResponseType.OK
        dialog.destroy()
        return result

    def refresh(self):
        try:
            info = core.summary()
        except core.MaintenanceError as exc:
            self.hero_title.set_text("No se pudo comprobar el estado")
            self.hero_detail.set_text(str(exc))
            return

        state = info["state"]
        health = info["health"]
        git = info["git"]
        report = health["report"]

        last = health["last"]
        due = health["due"]
        commit = state["health"].get("commit")

        if last is None:
            valid, _ = core.latest_health_is_valid()
            if valid and git["synced"] and git["clean"]:
                self.health_row.set_state(
                    "Existe una auditoría OK sincronizada. Adóptala para iniciar el ciclo trimestral.",
                    "LISTA PARA ADOPTAR", "badge-pending"
                )
                self.adopt_button.set_sensitive(True)
            else:
                self.health_row.set_state(
                    "Todavía no existe una validación trimestral registrada localmente.",
                    "PENDIENTE", "badge-warn"
                )
                self.adopt_button.set_sensitive(False)
        elif health["overdue"]:
            self.health_row.set_state(
                f"Última validación {fmt_day(last)} · venció {fmt_day(due)} · commit {short_commit(commit)}",
                "VENCIDA", "badge-warn"
            )
            self.adopt_button.set_sensitive(False)
        else:
            self.health_row.set_state(
                f"Última validación {fmt_day(last)} · próxima {fmt_day(due)} · commit {short_commit(commit)}",
                "VALIDADA", "badge-ok"
            )
            self.adopt_button.set_sensitive(False)

        latest_valid, _ = core.latest_health_is_valid()
        report_day = report.get("date") if report else None
        registered_day = core.parse_iso_day(state["health"].get("last_validated"))
        report_is_new = bool(
            report_day and (registered_day is None or report_day > registered_day)
        )
        self.sync_button.set_sensitive(
            bool(latest_valid and report_is_new and git["clean"] and git["synced"])
        )

        backup = info["backup"]
        cfg = backup["config"]
        if not backup["enabled"]:
            self.backup_row.set_state(
                "El respaldo externo no está habilitado en esta instalación. Automatización pendiente en TD-023.",
                "PENDIENTE TD-023", "badge-neutral"
            )
        elif not cfg["valid_name"]:
            self.backup_row.set_state(
                "SINEOS_BACKUP_ROOT debe terminar exactamente en SineOsBackups.",
                "CONFIGURACIÓN", "badge-warn"
            )
        elif backup["overdue"]:
            self.backup_row.set_state(
                f"Último respaldo {fmt_day(backup['last'])} · próximo {fmt_day(backup['due'])}",
                "PENDIENTE", "badge-warn"
            )
        else:
            self.backup_row.set_state(
                f"Último respaldo {fmt_day(backup['last'])} · próximo {fmt_day(backup['due'])}",
                "VALIDADO", "badge-ok"
            )

        if health["overdue"] or (backup["enabled"] and backup["overdue"]):
            self.hero_title.set_text("SineOS requiere mantenimiento")
            self.hero_detail.set_text("El estado pendiente seguirá recordándose hasta completar y sincronizar la validación.")
        else:
            self.hero_title.set_text("SineOS está al día")
            self.hero_detail.set_text("Los ciclos habilitados están dentro de su periodo de validez.")

        self.git_detail.set_text(
            f"Git: branch={git['branch'] or '—'} · limpio={'sí' if git['clean'] else 'no'} · sincronizado={'sí' if git['synced'] else 'no'} · HEAD={short_commit(git['local_head'])}"
        )
        self.report_detail.set_text(
            "Último reporte: " + (str(report["path"]) if report else "—")
        )

    def on_run_audit(self, _button):
        if not core.INTERACTIVE_AUDIT.exists():
            self.message("No se encontró el lanzador", str(core.INTERACTIVE_AUDIT), error=True)
            return
        try:
            subprocess.Popen([
                "exo-open", "--launch", "TerminalEmulator", "bash", str(core.INTERACTIVE_AUDIT)
            ])
        except OSError as exc:
            self.message("No se pudo abrir la auditoría", str(exc), error=True)

    def on_adopt(self, _button):
        if not self.confirm(
            "Adoptar validación actual",
            "Se guardará localmente la fecha de la última auditoría OK y el commit actualmente sincronizado con GitHub como inicio del ciclo trimestral.",
            "Adoptar",
        ):
            return
        try:
            commit = core.adopt_current_validation()
            self.message("Validación adoptada", f"Commit validado: {commit}")
        except core.MaintenanceError as exc:
            self.message("No se pudo adoptar", str(exc), error=True)
        self.refresh()

    def on_sync(self, _button):
        if not self.confirm(
            "Registrar y sincronizar salud",
            "SineOS actualizará únicamente Health-Status.md, creará un commit específico, hará push a origin/main y solo después cerrará el recordatorio.",
            "Registrar y sincronizar",
        ):
            return
        try:
            commit = core.sync_health_validation()
            self.message("Salud sincronizada", f"GitHub confirmó el commit {commit}.")
        except core.MaintenanceError as exc:
            self.message("La validación sigue pendiente", str(exc), error=True)
        self.refresh()


def cli_status():
    info = core.summary()
    state = info["state"]
    _, due, overdue = core.health_schedule(state)
    print("SineOS · Mantenimiento")
    print(f"Salud validada : {state['health'].get('last_validated') or 'no'}")
    print(f"Próxima salud  : {due.isoformat() if due else '—'}")
    print(f"Salud vencida  : {'sí' if overdue else 'no'}")
    print(f"Commit salud   : {state['health'].get('commit') or '—'}")
    print(f"Backup activo  : {'sí' if state['backup'].get('enabled') else 'no'}")
    print(f"Git sincronizado: {'sí' if info['git']['synced'] else 'no'}")


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--adopt-current", action="store_true")
    args = parser.parse_args()

    if args.notify:
        core.send_due_notification()
        return 0
    if args.status:
        cli_status()
        return 0
    if args.adopt_current:
        try:
            print(core.adopt_current_validation())
            return 0
        except core.MaintenanceError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    window = MaintenanceWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
