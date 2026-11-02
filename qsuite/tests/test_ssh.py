"""Credential-selection tests for qsuite. AI-generated test.

Run with: python -m unittest discover -s qsuite/tests -v
"""
import contextlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import paramiko

from qsuite.ssh import get_ssh_key


class SSHAuthenticationTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.enterContext(contextlib.chdir(directory))
        self.enterContext(patch.dict(os.environ, {'HOME': directory}))
        self.agent = self.enterContext(patch('qsuite.ssh.paramiko.Agent')).return_value
        self.agent.get_keys.return_value = (object(),)

    def test_explicit_key_overrides_agent_with_or_without_passphrase(self):
        key = paramiko.RSAKey.generate(2048)
        for password in (None, 'test-passphrase'):
            with self.subTest(password=password):
                key.write_private_key_file('explicit_rsa', password=password)
                config = 'pkey_file=explicit_rsa\n'
                if password:
                    config += 'password=' + password + '\n'
                Path('.env').write_text(config)
                self.assertEqual(get_ssh_key().asbytes(), key.asbytes())

    def test_agent_without_dotenv_or_with_unrelated_dotenv_overrides_legacy(self):
        self.assertIsNone(get_ssh_key())
        Path('.env').write_text('UNRELATED=value\n')
        Path('.ssh').mkdir()
        Path('.ssh/id_rsa_groot').write_text('must not be loaded')
        self.assertIsNone(get_ssh_key())

    def test_legacy_key_when_agent_is_empty(self):
        self.agent.get_keys.return_value = ()
        Path('.ssh').mkdir()
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file('.ssh/id_rsa_groot')
        self.assertEqual(get_ssh_key().asbytes(), key.asbytes())

    def test_invalid_explicit_key_does_not_fall_back_to_agent(self):
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file('protected_rsa', password='test-passphrase')
        for config, error in (
            ('pkey_file=missing_rsa\n', FileNotFoundError),
            ('pkey_file=\n', ValueError),
            ('pkey_file=protected_rsa\npassword=wrong\n', paramiko.SSHException),
        ):
            with self.subTest(config=config):
                Path('.env').write_text(config)
                with self.assertRaises(error):
                    get_ssh_key()

    def test_missing_credentials_explain_how_to_proceed(self):
        self.agent.get_keys.return_value = ()
        with self.assertRaisesRegex(FileNotFoundError, 'ssh-add'):
            get_ssh_key()
