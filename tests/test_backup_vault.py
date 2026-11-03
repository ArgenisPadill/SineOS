#!/usr/bin/env python3
"""Pruebas sin acceso al host productivo: SINEOS_VAULT y rutas de restore."""

import importlib.util
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


MODULE_FILE = Path(__file__).resolve().parents[1] / "Apps/Maintenance/backup_engine.py"
SPEC = importlib.util.spec_from_file_location("sineos_backup_engine_test", MODULE_FILE)
backup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(backup)


class VaultConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="sineos-test-vault-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home" / "testuser"
        self.repo = self.home / "Workspace" / "SineOS-test"
        self.vault = self.base / "external" / "MyVault"
        self.vault.mkdir(parents=True)
        (self.vault / ".obsidian").mkdir()
        self.repo.mkdir(parents=True)
        self.staging = (
            self.home / ".local/state/sineos/backup/staging/postgresql-test"
        )
        self.staging.mkdir(parents=True)
        (self.home / ".config/sineos").mkdir(parents=True)
        (self.home / ".local/state/sineos/health").mkdir(parents=True)
        (self.home / ".local/state/sineos/security").mkdir(parents=True)
        (self.home / ".local/state/sineos-maintenance").mkdir(parents=True)

        self.context = (
            patch.dict(os.environ, {"SINEOS_VAULT": str(self.vault)}),
            patch.object(backup.Path, "home", return_value=self.home),
            patch.object(backup, "REPO_ROOT", self.repo),
        )
        for ctx in self.context:
            ctx.__enter__()
            self.addCleanup(ctx.__exit__, None, None, None)

    def test_absent_or_empty_environment_fails_closed(self):
        for value in ("", "  "):
            with patch.dict(os.environ, {"SINEOS_VAULT": value}):
                with self.assertRaises(backup.BackupError):
                    backup.configured_vault_root()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(backup.BackupError):
                backup.configured_vault_root()

    def test_relative_or_non_vault_path_is_rejected(self):
        with patch.dict(os.environ, {"SINEOS_VAULT": "relative/vault"}):
            with self.assertRaises(backup.BackupError):
                backup.configured_vault_root()
        (self.vault / ".obsidian").rmdir()
        with self.assertRaises(backup.BackupError):
            backup.configured_vault_root()

    def test_sources_and_exclusions_use_configured_vault(self):
        self.assertEqual(backup.configured_vault_root(), self.vault)
        sources = backup.backup_sources(self.staging)
        excludes = backup.backup_excludes()
        self.assertIn(self.vault, sources)
        self.assertIn(self.vault / ".opencode/node_modules", excludes)
        self.assertNotIn(self.home / "Obsidian/SineOS", sources)

    def test_restore_layout_uses_actual_absolute_paths(self):
        destination = self.base / "restore"
        for original in (
            self.repo,
            self.vault,
            self.home / ".config/sineos",
            self.home / ".local/state/sineos-maintenance",
        ):
            restored = destination / original.relative_to(original.anchor)
            restored.mkdir(parents=True)

        result = backup.validate_restored_layout(destination)
        self.assertEqual(Path(result["repository"]), destination / self.repo.relative_to("/"))
        self.assertEqual(Path(result["vault"]), destination / self.vault.relative_to("/"))

        forbidden = (
            destination / self.repo.relative_to("/")
            / "Containers/volumes/postgres/data"
        )
        forbidden.mkdir(parents=True)
        with self.assertRaises(backup.BackupError):
            backup.validate_restored_layout(destination)


if __name__ == "__main__":
    unittest.main()
