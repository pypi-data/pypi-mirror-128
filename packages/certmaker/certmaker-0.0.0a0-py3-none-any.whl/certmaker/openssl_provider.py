# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.

    .. spelling::

       pki
"""
import os
import sys
import uuid
import time
import logging
import tempfile
import argparse
import contextlib
import subprocess

from typing import List, Generator, Optional, Tuple

from .utils import bytes_
from .constants import COMMA
from .config import (
    ReqConfigNode, 
    ReqExtensionConfigNode, 
    OpenSslConfigNode,
    OpenSslConfig,
)


logger = logging.getLogger(__name__)


def remove_passphrase(
        key_in_path: str,
        password: str,
        key_out_path: str,
        timeout: int = 10,
) -> bool:
    """Remove passphrase from a private key."""
    command = [
        'openssl', 'rsa',
        '-passin', 'pass:%s' % password,
        '-in', key_in_path,
        '-out', key_out_path,
    ]
    return run_openssl_command(command, timeout)


def gen_private_key(
        key_path: str,
        password: str,
        bits: int = 2048,
        timeout: int = 10,
) -> bool:
    """Generates a private key."""
    command = [
        'openssl', 'genrsa', '-aes256',
        '-passout', 'pass:%s' % password,
        '-out', key_path, str(bits),
    ]
    return run_openssl_command(command, timeout)


def gen_public_key(
        public_key_path: str,
        private_key_path: str,
        private_key_password: str,
        subject: str,
        alt_subj_names: Optional[List[str]] = None,
        extended_key_usage: Optional[str] = None,
        validity_in_days: int = 365,
        timeout: int = 10,
) -> bool:
    """For a given private key, generates a corresponding public key."""
    config_node = ReqConfigNode()
    extension_node = None

    if (alt_subj_names is not None and len(alt_subj_names) > 0) or extended_key_usage is not None:
        san_node = OpenSslConfigNode("req_san")
        san_node.entries = {"DNS." + str(k): v for k, v in enumerate(alt_subj_names)}
        extension_node = ReqExtensionConfigNode()
        extension_node.entries["extendedKeyUsage"] = extended_key_usage
        extension_node.entries["subjectAltName"] = san_node
    
    with OpenSslConfig().write(config_node) as config_path:
        command = [
            'openssl', 'req', '-new', '-x509', '-sha256',
            '-days', str(validity_in_days), '-subj', subject,
            '-passin', 'pass:%s' % private_key_password,
            '-config', config_path,
            '-key', private_key_path, '-out', public_key_path,
        ]
        if extension_node:
            command.extend(['-extensions', extension_node.name])
        return run_openssl_command(command, timeout)


def gen_csr(
        csr_path: str,
        key_path: str,
        password: str,
        crt_path: str,
        timeout: int = 10,
) -> bool:
    """Generates a CSR based upon existing certificate and key file."""
    command = [
        'openssl', 'x509', '-x509toreq',
        '-passin', 'pass:%s' % password,
        '-in', crt_path, '-signkey', key_path,
        '-out', csr_path,
    ]
    return run_openssl_command(command, timeout)


def sign_csr(
        csr_path: str,
        crt_path: str,
        ca_key_path: str,
        ca_key_password: str,
        ca_crt_path: str,
        serial: str,
        alt_subj_names: Optional[List[str]] = None,
        extended_key_usage: Optional[str] = None,
        validity_in_days: int = 365,
        timeout: int = 10,
) -> bool:
    """Sign a CSR using CA key and certificate."""
    extension_node = OpenSslConfigNode()

    if (alt_subj_names is not None and len(alt_subj_names) > 0) or extended_key_usage is not None:
        san_node = OpenSslConfigNode("req_san")
        san_node.entries = {"DNS." + str(k): v for k, v in enumerate(alt_subj_names)}
        extension_node = ReqExtensionConfigNode()
        extension_node.entries["extendedKeyUsage"] = extended_key_usage
        extension_node.entries["subjectAltName"] = san_node
    
    with OpenSslConfig().write(extension_node) as config_path:
        command = [
            'openssl', 'x509', '-req', '-sha256',
            '-CA', ca_crt_path,
            '-CAkey', ca_key_path,
            '-passin', 'pass:%s' % ca_key_password,
            '-set_serial', serial,
            '-days', str(validity_in_days),
            '-extfile', config_path,
            '-in', csr_path,
            '-out', crt_path,
        ]
        return run_openssl_command(command, timeout)


def run_openssl_command(command: List[str], timeout: int) -> bool:
    print(' '.join(command))
    cmd = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    cmd.communicate(timeout=timeout)
    return cmd.returncode == 0
