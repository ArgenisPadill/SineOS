#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path


DNSCRYPT_ADDRESS = "127.0.2.1"

STATE_DIR = Path.home() / ".local/state/sineos-network-privacy"
STATE_FILE = STATE_DIR / "profiles.json"


class NetworkPolicyError(Exception):
    pass


def run(command, timeout=15):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise NetworkPolicyError(str(exc)) from exc

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise NetworkPolicyError(
            message or f"Falló: {' '.join(command)}"
        )

    return result.stdout.strip()


def read_value(profile, property_name):
    return run([
        "nmcli",
        "-g",
        property_name,
        "connection",
        "show",
        profile,
    ])


def load_state():
    STATE_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)

    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise NetworkPolicyError(
            "No se pudo leer el estado guardado de SineOS."
        ) from exc

    if not isinstance(data, dict):
        raise NetworkPolicyError(
            "El archivo de estado de SineOS no es válido."
        )

    return data


def save_state(data):
    STATE_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)

    temporary = STATE_FILE.with_suffix(".json.tmp")

    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(
                data,
                handle,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            handle.write("\n")

        os.chmod(temporary, 0o600)
        os.replace(temporary, STATE_FILE)
        os.chmod(STATE_FILE, 0o600)

    except OSError as exc:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass

        raise NetworkPolicyError(
            "No se pudo guardar el estado de SineOS."
        ) from exc


def normalize_bool(value):
    return value.strip().lower() in (
        "yes",
        "sí",
        "si",
        "true",
        "1",
    )


def current_profile_state(profile):
    return {
        "ipv4_dns": read_value(profile, "ipv4.dns"),
        "ipv4_ignore_auto_dns": normalize_bool(
            read_value(profile, "ipv4.ignore-auto-dns")
        ),
    }


def is_dnscrypt_configured(profile):
    current = current_profile_state(profile)

    dns = [
        item.strip()
        for item in current["ipv4_dns"].replace(";", ",").split(",")
        if item.strip()
    ]

    return (
        DNSCRYPT_ADDRESS in dns
        and current["ipv4_ignore_auto_dns"]
    )


def remember_original(profile):
    state = load_state()

    if profile in state:
        return

    original = current_profile_state(profile)

    state[profile] = {
        "ipv4_dns": original["ipv4_dns"],
        "ipv4_ignore_auto_dns": original["ipv4_ignore_auto_dns"],
        "managed_by_sineos": True,
    }

    save_state(state)



def wifi_is_active(profile):
    output = run([
        "nmcli",
        "-t",
        "-f",
        "NAME,TYPE",
        "connection",
        "show",
        "--active",
    ])

    return any(
        line == f"{profile}:802-11-wireless"
        for line in output.splitlines()
    )


def dnscrypt_responds():
    try:
        output = run([
            "dig",
            "@127.0.2.1",
            "debian.org",
            "+short",
            "+time=3",
            "+tries=1",
        ], timeout=5)

        return bool(output.strip())

    except NetworkPolicyError:
        return False


def system_dns_responds():
    try:
        output = run([
            "getent",
            "ahostsv4",
            "debian.org",
        ], timeout=5)

        return bool(output.strip())

    except NetworkPolicyError:
        return False


def validate_dnscrypt(profile):
    if not wifi_is_active(profile):
        raise NetworkPolicyError(
            "La red Wi-Fi no volvió a conectarse."
        )

    if not is_dnscrypt_configured(profile):
        raise NetworkPolicyError(
            "NetworkManager no conservó la configuración DNSCrypt."
        )

    if not dnscrypt_responds():
        raise NetworkPolicyError(
            "DNSCrypt está configurado, pero no responde consultas DNS."
        )

    if not system_dns_responds():
        raise NetworkPolicyError(
            "La resolución DNS del sistema no funciona."
        )


def validate_restored_network(profile):
    if not wifi_is_active(profile):
        raise NetworkPolicyError(
            "La red Wi-Fi no volvió a conectarse."
        )

    if not system_dns_responds():
        raise NetworkPolicyError(
            "La red se conectó, pero la resolución DNS no funciona."
        )


def activate_dnscrypt(profile):
    # Guardamos el estado original antes del primer cambio.
    remember_original(profile)

    previous = current_profile_state(profile)

    try:
        run([
            "nmcli",
            "connection",
            "modify",
            profile,
            "ipv4.dns",
            DNSCRYPT_ADDRESS,
            "ipv4.ignore-auto-dns",
            "yes",
        ])

        run([
            "nmcli",
            "connection",
            "up",
            profile,
        ], timeout=30)

        validate_dnscrypt(profile)

    except Exception as exc:
        # Intento de reversión al estado inmediatamente anterior.
        try:
            restore_values(
                profile,
                previous["ipv4_dns"],
                previous["ipv4_ignore_auto_dns"],
                reactivate=True,
            )
        except Exception:
            pass

        if isinstance(exc, NetworkPolicyError):
            raise

        raise NetworkPolicyError(str(exc)) from exc


def restore_values(profile, dns, ignore_auto_dns, reactivate=True):
    command = [
        "nmcli",
        "connection",
        "modify",
        profile,
        "ipv4.dns",
        dns,
        "ipv4.ignore-auto-dns",
        "yes" if ignore_auto_dns else "no",
    ]

    run(command)

    if reactivate:
        run([
            "nmcli",
            "connection",
            "up",
            profile,
        ], timeout=30)


def restore_original(profile):
    state = load_state()

    if profile not in state:
        raise NetworkPolicyError(
            "SineOS no tiene guardada la configuración original "
            "de esta red."
        )

    original = state[profile]

    previous = current_profile_state(profile)

    try:
        restore_values(
            profile,
            original.get("ipv4_dns", ""),
            bool(original.get("ipv4_ignore_auto_dns", False)),
            reactivate=True,
        )

        validate_restored_network(profile)

    except Exception as exc:
        try:
            restore_values(
                profile,
                previous["ipv4_dns"],
                previous["ipv4_ignore_auto_dns"],
                reactivate=True,
            )
        except Exception:
            pass

        if isinstance(exc, NetworkPolicyError):
            raise

        raise NetworkPolicyError(str(exc)) from exc


def has_saved_original(profile):
    state = load_state()
    return profile in state
