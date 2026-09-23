#!/usr/bin/env python3

import subprocess
import gi

import network_policy

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


APP_TITLE = "SineOS · Privacidad de red"
DNSCRYPT_ADDRESS = "127.0.2.1"


def run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def active_wifi():
    output = run([
        "nmcli", "-t", "-f", "NAME,TYPE",
        "connection", "show", "--active"
    ])

    for line in output.splitlines():
        if line.endswith(":802-11-wireless"):
            return line.rsplit(":", 1)[0]

    return None


def proton_connection():
    output = run([
        "nmcli", "-t", "-f", "NAME,TYPE,DEVICE",
        "connection", "show", "--active"
    ])

    for line in output.splitlines():
        parts = line.rsplit(":", 2)

        if len(parts) == 3:
            name, connection_type, device = parts

            if connection_type == "wireguard" and device == "proton0":
                return name

    return None


def dnscrypt_service_active():
    return run([
        "systemctl", "is-active", "dnscrypt-proxy"
    ]) == "active"


def dnscrypt_configured(wifi):
    if not wifi:
        return False

    dns = run([
        "nmcli", "-g", "ipv4.dns",
        "connection", "show", wifi
    ])

    ignore = run([
        "nmcli", "-g", "ipv4.ignore-auto-dns",
        "connection", "show", wifi
    ]).lower()

    dns_servers = [
        item.strip()
        for item in dns.replace(";", ",").split(",")
        if item.strip()
    ]

    return (
        DNSCRYPT_ADDRESS in dns_servers
        and ignore in ("yes", "sí")
    )


def effective_dns():
    servers = []

    try:
        with open("/etc/resolv.conf", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()

                if line.startswith("nameserver "):
                    parts = line.split()

                    if len(parts) >= 2:
                        servers.append(parts[1])
    except OSError:
        pass

    return servers


def symbolic_icon(name, size=Gtk.IconSize.DIALOG):
    image = Gtk.Image.new_from_icon_name(name, size)
    image.set_valign(Gtk.Align.START)
    return image


def section_label(text):
    label = Gtk.Label(label=text)
    label.set_xalign(0)
    label.get_style_context().add_class("section-label")
    return label


class StatusBadge(Gtk.Label):
    def __init__(self):
        super().__init__()
        self.set_valign(Gtk.Align.CENTER)
        self.get_style_context().add_class("badge")

    def set_state(self, text, css_class=None):
        context = self.get_style_context()

        for class_name in (
            "badge-active",
            "badge-standby",
            "badge-warning",
            "badge-neutral",
        ):
            context.remove_class(class_name)

        self.set_text(text)

        if css_class:
            context.add_class(css_class)


class ProtectionRow(Gtk.Box):
    def __init__(self, icon_name, title):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=14
        )

        self.get_style_context().add_class("protection-row")

        icon = symbolic_icon(icon_name, Gtk.IconSize.BUTTON)
        icon.get_style_context().add_class("row-icon")

        text_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=3
        )
        text_box.set_hexpand(True)

        self.title = Gtk.Label(label=title)
        self.title.set_xalign(0)
        self.title.get_style_context().add_class("row-title")

        self.description = Gtk.Label()
        self.description.set_xalign(0)
        self.description.set_line_wrap(True)
        self.description.get_style_context().add_class("secondary")

        text_box.pack_start(self.title, False, False, 0)
        text_box.pack_start(self.description, False, False, 0)

        self.badge = StatusBadge()

        self.pack_start(icon, False, False, 0)
        self.pack_start(text_box, True, True, 0)
        self.pack_end(self.badge, False, False, 0)


class NetworkPrivacyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_TITLE)

        self.set_default_size(560, 600)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.load_css()
        self.build_ui()
        self.refresh()

        # Mantener la interfaz sincronizada con NetworkManager y Proton.
        self._refresh_timer = GLib.timeout_add_seconds(
            2,
            self.auto_refresh
        )

    def load_css(self):
        css = b"""
        window {
            background-color: @theme_bg_color;
        }

        .page {
            padding: 26px 30px 24px 30px;
        }

        .title {
            font-size: 22px;
            font-weight: 700;
        }

        .subtitle,
        .secondary,
        .technical-value {
            color: @theme_fg_color;
            opacity: 0.66;
        }

        .section-label {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            color: @theme_fg_color;
            opacity: 0.55;
        }

        .hero {
            padding: 17px 18px;
            border-radius: 11px;
            border: 1px solid alpha(@theme_fg_color, 0.12);
            background-color: alpha(@theme_fg_color, 0.035);
        }

        .hero-title {
            font-size: 17px;
            font-weight: 700;
        }

        .network-name {
            font-size: 15px;
            font-weight: 700;
        }

        .row-title {
            font-weight: 700;
        }

        .protection-row {
            padding: 13px 0;
        }

        .badge {
            font-size: 11px;
            font-weight: 700;
            padding: 5px 9px;
            border-radius: 12px;
            background-color: alpha(@theme_fg_color, 0.08);
        }

        .badge-active {
            background-color: alpha(@success_color, 0.20);
        }

        .badge-standby {
            background-color: alpha(@warning_color, 0.16);
        }

        .badge-warning {
            background-color: alpha(@error_color, 0.18);
        }

        .badge-neutral {
            background-color: alpha(@theme_fg_color, 0.08);
        }

        .dns-card {
            padding: 13px 15px;
            border-radius: 9px;
            background-color: alpha(@theme_fg_color, 0.045);
        }

        .dns-provider {
            font-size: 15px;
            font-weight: 700;
        }

        .details {
            padding: 10px 2px 2px 2px;
        }

        .technical-label {
            font-size: 11px;
            font-weight: 700;
            color: @theme_fg_color;
            opacity: 0.55;
        }

        separator {
            background-color: alpha(@theme_fg_color, 0.10);
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def build_ui(self):
        page = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18
        )
        page.get_style_context().add_class("page")
        self.add(page)

        # Encabezado
        header = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=3
        )

        title = Gtk.Label(label="Privacidad de red")
        title.set_xalign(0)
        title.get_style_context().add_class("title")

        subtitle = Gtk.Label(
            label="Control de privacidad para la conexión actual"
        )
        subtitle.set_xalign(0)
        subtitle.get_style_context().add_class("subtitle")

        header.pack_start(title, False, False, 0)
        header.pack_start(subtitle, False, False, 0)

        page.pack_start(header, False, False, 0)

        # Resumen principal
        hero = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=14
        )
        hero.get_style_context().add_class("hero")

        self.hero_icon = symbolic_icon(
            "security-high-symbolic",
            Gtk.IconSize.DIALOG
        )

        hero_text = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=3
        )

        self.hero_title = Gtk.Label()
        self.hero_title.set_xalign(0)
        self.hero_title.get_style_context().add_class("hero-title")

        self.hero_description = Gtk.Label()
        self.hero_description.set_xalign(0)
        self.hero_description.set_line_wrap(True)
        self.hero_description.get_style_context().add_class("secondary")

        hero_text.pack_start(
            self.hero_title, False, False, 0
        )
        hero_text.pack_start(
            self.hero_description, False, False, 0
        )

        hero.pack_start(self.hero_icon, False, False, 0)
        hero.pack_start(hero_text, True, True, 0)

        page.pack_start(hero, False, False, 0)

        # Red actual
        network_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=9
        )

        network_box.pack_start(
            section_label("RED ACTUAL"),
            False, False, 0
        )

        network_content = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=13
        )

        self.network_icon = symbolic_icon(
            "network-wireless-symbolic",
            Gtk.IconSize.BUTTON
        )

        network_text = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=2
        )

        self.network_name = Gtk.Label()
        self.network_name.set_xalign(0)
        self.network_name.get_style_context().add_class("network-name")

        self.network_description = Gtk.Label()
        self.network_description.set_xalign(0)
        self.network_description.get_style_context().add_class("secondary")

        network_text.pack_start(
            self.network_name, False, False, 0
        )
        network_text.pack_start(
            self.network_description, False, False, 0
        )

        network_content.pack_start(
            self.network_icon, False, False, 0
        )
        network_content.pack_start(
            network_text, True, True, 0
        )

        network_box.pack_start(
            network_content, False, False, 0
        )

        page.pack_start(network_box, False, False, 0)

        # Protección
        protection_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )

        protection_box.pack_start(
            section_label("PROTECCIÓN"),
            False, False, 4
        )

        self.dnscrypt_row = ProtectionRow(
            "changes-prevent-symbolic",
            "DNS cifrado"
        )

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        self.proton_row = ProtectionRow(
            "network-vpn-symbolic",
            "VPN"
        )

        protection_box.pack_start(
            self.dnscrypt_row, False, False, 0
        )
        protection_box.pack_start(
            separator, False, False, 0
        )
        protection_box.pack_start(
            self.proton_row, False, False, 0
        )

        page.pack_start(protection_box, False, False, 0)

        # DNS actual
        dns_section = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        dns_section.pack_start(
            section_label("DNS EN USO"),
            False, False, 0
        )

        dns_card = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=3
        )
        dns_card.get_style_context().add_class("dns-card")

        self.dns_provider = Gtk.Label()
        self.dns_provider.set_xalign(0)
        self.dns_provider.get_style_context().add_class("dns-provider")

        self.dns_summary = Gtk.Label()
        self.dns_summary.set_xalign(0)
        self.dns_summary.get_style_context().add_class("secondary")

        dns_card.pack_start(
            self.dns_provider, False, False, 0
        )
        dns_card.pack_start(
            self.dns_summary, False, False, 0
        )

        dns_section.pack_start(
            dns_card, False, False, 0
        )

        page.pack_start(dns_section, False, False, 0)

        # Detalles técnicos
        self.details_expander = Gtk.Expander(
            label="Detalles técnicos"
        )

        details = Gtk.Grid()
        details.set_column_spacing(16)
        details.set_row_spacing(6)
        details.get_style_context().add_class("details")

        self.detail_wifi = self.add_detail_row(
            details, 0, "Perfil Wi-Fi", ""
        )
        self.detail_dns = self.add_detail_row(
            details, 1, "Servidores DNS", ""
        )
        self.detail_dnscrypt = self.add_detail_row(
            details, 2, "Servicio DNSCrypt", ""
        )
        self.detail_vpn = self.add_detail_row(
            details, 3, "Conexión VPN", ""
        )

        self.details_expander.add(details)

        page.pack_start(
            self.details_expander, False, False, 0
        )

        # Acciones
        footer = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )

        self.policy_button = Gtk.Button()
        self.policy_button.connect(
            "clicked",
            self.on_policy_clicked
        )

        close = Gtk.Button(label="Cerrar")
        close.connect(
            "clicked",
            lambda *_: self.close()
        )

        footer.pack_start(
            self.policy_button,
            False, False, 0
        )
        footer.pack_end(close, False, False, 0)

        page.pack_start(footer, False, False, 0)

    def confirmation_dialog(self, title, message, action_label):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.NONE,
            text=title,
        )

        dialog.format_secondary_text(message)
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button(action_label, Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)

        response = dialog.run()
        dialog.destroy()

        return response == Gtk.ResponseType.OK

    def show_error(self, title, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text=title,
        )

        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def show_success(self, title, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )

        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_policy_clicked(self, _button):
        wifi = active_wifi()

        if not wifi:
            return

        proton = proton_connection()
        configured = dnscrypt_configured(wifi)

        if proton:
            self.show_error(
                "Proton VPN está activo",
                "Proton VPN controla actualmente el DNS. "
                "Desconecta la VPN antes de cambiar la política DNS "
                "guardada para esta red."
            )
            return

        if configured:
            if not network_policy.has_saved_original(wifi):
                self.show_error(
                    "No se puede restaurar automáticamente",
                    "SineOS no tiene guardada la configuración DNS "
                    "original de esta red. No se realizará ningún cambio."
                )
                return

            confirmed = self.confirmation_dialog(
                "Restaurar DNS de la red",
                f"La red «{wifi}» volverá a utilizar la configuración "
                "DNS que tenía antes de activar DNSCrypt.\n\n"
                "La conexión Wi-Fi se reconectará durante unos segundos.",
                "Restaurar",
            )

            if not confirmed:
                return

            self.policy_button.set_sensitive(False)

            try:
                network_policy.restore_original(wifi)

            except network_policy.NetworkPolicyError as error:
                self.show_error(
                    "No se pudo restaurar el DNS",
                    str(error),
                )
                self.refresh()
                return

            self.refresh()

            self.show_success(
                "DNS restaurado",
                f"«{wifi}» volvió a su configuración DNS original."
            )

        else:
            confirmed = self.confirmation_dialog(
                "Activar DNSCrypt",
                f"DNSCrypt se configurará únicamente para la red "
                f"«{wifi}».\n\n"
                "SineOS guardará primero la configuración DNS actual "
                "para poder restaurarla posteriormente. "
                "La conexión Wi-Fi se reconectará durante unos segundos.",
                "Activar",
            )

            if not confirmed:
                return

            self.policy_button.set_sensitive(False)

            try:
                network_policy.activate_dnscrypt(wifi)

            except network_policy.NetworkPolicyError as error:
                self.show_error(
                    "No se pudo activar DNSCrypt",
                    str(error),
                )
                self.refresh()
                return

            self.refresh()

            self.show_success(
                "DNSCrypt activado",
                f"DNSCrypt está protegiendo las consultas DNS "
                f"de «{wifi}»."
            )

    @staticmethod
    def add_detail_row(grid, row, title, value):
        label = Gtk.Label(label=title)
        label.set_xalign(0)
        label.get_style_context().add_class("technical-label")

        value_label = Gtk.Label(label=value)
        value_label.set_xalign(0)
        value_label.set_selectable(True)
        value_label.set_hexpand(True)
        value_label.get_style_context().add_class("technical-value")

        grid.attach(label, 0, row, 1, 1)
        grid.attach(value_label, 1, row, 1, 1)

        return value_label

    def auto_refresh(self):
        self.refresh()
        return True

    def refresh(self):
        wifi = active_wifi()
        proton = proton_connection()
        dnscrypt_active = dnscrypt_service_active()
        configured = dnscrypt_configured(wifi)
        servers = effective_dns()

        # Acción contextual
        policy_style = self.policy_button.get_style_context()
        policy_style.remove_class("suggested-action")

        if not wifi:
            self.policy_button.set_label(
                "Sin red Wi-Fi"
            )
            self.policy_button.set_sensitive(False)

        elif proton:
            self.policy_button.set_label(
                "Política DNS en espera"
            )
            self.policy_button.set_sensitive(False)

        elif configured:
            self.policy_button.set_label(
                "Restaurar DNS de la red"
            )
            self.policy_button.set_sensitive(
                network_policy.has_saved_original(wifi)
            )

        elif dnscrypt_active:
            self.policy_button.set_label(
                "Activar DNSCrypt en esta red"
            )
            self.policy_button.set_sensitive(True)
            policy_style.add_class("suggested-action")

        else:
            self.policy_button.set_label(
                "DNSCrypt no disponible"
            )
            self.policy_button.set_sensitive(False)

        # Red actual
        if wifi:
            self.network_name.set_text(wifi)
            self.network_description.set_text("Wi-Fi")
        else:
            self.network_name.set_text("Sin conexión Wi-Fi")
            self.network_description.set_text(
                "No hay una red inalámbrica activa"
            )

        # VPN
        if proton:
            self.proton_row.description.set_text(proton)
            self.proton_row.badge.set_state(
                "ACTIVADA",
                "badge-active"
            )
        else:
            self.proton_row.description.set_text("Proton VPN")
            self.proton_row.badge.set_state(
                "INACTIVA",
                "badge-neutral"
            )

        # DNSCrypt
        if proton and configured and dnscrypt_active:
            self.dnscrypt_row.description.set_text(
                "DNSCrypt · disponible al desconectar la VPN"
            )
            self.dnscrypt_row.badge.set_state(
                "EN ESPERA",
                "badge-standby"
            )

        elif configured and dnscrypt_active:
            self.dnscrypt_row.description.set_text("DNSCrypt")
            self.dnscrypt_row.badge.set_state(
                "ACTIVADO",
                "badge-active"
            )

        elif configured and not dnscrypt_active:
            self.dnscrypt_row.description.set_text(
                "DNSCrypt está configurado, pero el servicio está detenido"
            )
            self.dnscrypt_row.badge.set_state(
                "ATENCIÓN",
                "badge-warning"
            )

        elif dnscrypt_active:
            self.dnscrypt_row.description.set_text(
                "DNSCrypt · no configurado para esta red"
            )
            self.dnscrypt_row.badge.set_state(
                "DISPONIBLE",
                "badge-neutral"
            )

        else:
            self.dnscrypt_row.description.set_text(
                "DNSCrypt no está disponible"
            )
            self.dnscrypt_row.badge.set_state(
                "INACTIVO",
                "badge-neutral"
            )

        # Resumen principal + DNS efectivo
        if proton:
            self.hero_title.set_text("VPN activa")
            self.hero_description.set_text(
                "Proton protege la conexión y controla actualmente el DNS."
            )

            self.dns_provider.set_text("Proton VPN")
            self.dns_summary.set_text(
                "DNS protegido mediante el túnel VPN"
            )

        elif (
            configured
            and dnscrypt_active
            and DNSCRYPT_ADDRESS in servers
        ):
            self.hero_title.set_text("Conexión protegida")
            self.hero_description.set_text(
                "DNSCrypt protege tus consultas DNS en esta red."
            )

            self.dns_provider.set_text("DNSCrypt")
            self.dns_summary.set_text(
                "Resolución DNS cifrada"
            )

        elif configured and not dnscrypt_active:
            self.hero_title.set_text("Requiere atención")
            self.hero_description.set_text(
                "Esta red espera usar DNSCrypt, "
                "pero el servicio no está funcionando."
            )

            self.dns_provider.set_text("DNS no verificado")
            self.dns_summary.set_text(
                "Comprueba el servicio DNSCrypt"
            )

        elif wifi:
            self.hero_title.set_text("DNS automático")
            self.hero_description.set_text(
                "La conexión utiliza los servidores DNS "
                "proporcionados por la red."
            )

            self.dns_provider.set_text("DNS de la red")
            self.dns_summary.set_text(
                "Configuración automática"
            )

        else:
            self.hero_title.set_text("Sin conexión")
            self.hero_description.set_text(
                "Conéctate a una red Wi-Fi para consultar "
                "su estado de privacidad."
            )

            self.dns_provider.set_text("Sin DNS activo")
            self.dns_summary.set_text(
                "No hay una conexión Wi-Fi disponible"
            )

        # Detalles técnicos
        self.detail_wifi.set_text(
            wifi if wifi else "No disponible"
        )

        self.detail_dns.set_text(
            " · ".join(servers)
            if servers
            else "No detectados"
        )

        self.detail_dnscrypt.set_text(
            "Activo"
            if dnscrypt_active
            else "Inactivo"
        )

        self.detail_vpn.set_text(
            proton
            if proton
            else "Desconectada"
        )


window = NetworkPrivacyWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
