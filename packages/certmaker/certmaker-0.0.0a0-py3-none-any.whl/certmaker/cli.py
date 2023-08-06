"""
    certmaker.cli
    ~~~~~~~~~~~~~

    This module implements the **certmaker** CLI command.
"""
import logging
import click

from click.types import STRING

from .pki import CertMaker
from .config import OpenSslConfig, CaConfigNode, CaDefaultConfigNode

logger = logging.getLogger("certmaker.cli")

stdout_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


@click.command()
@click.option("--passphrase", type=STRING)
@click.option("--private-key", type=STRING)
@click.option("--public-key", type=STRING)
@click.option("--subject", type=STRING)
@click.option("--csr", type=STRING)
@click.option("--certificate", type=STRING)
@click.option("--asn", type=STRING)
def main(passphrase, private_key, public_key, subject, csr, certificate, asn):
    """CertMaker"""
    certMaker = CertMaker()
    certMaker.generate_private_key(private_key, passphrase)
    certMaker.generate_public_key(public_key, private_key, passphrase, "/CN=certmaker-ca-root")
    # certMaker.create_csr(csr, private_key, passphrase, certificate)
    # certMaker.sign_csr(csr, certificate + "signed.pem", private_key, passphrase, certificate, "12345")
    logger.info(f"\n{CaConfigNode()}")
