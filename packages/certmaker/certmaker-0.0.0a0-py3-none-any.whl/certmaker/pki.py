from typing import List, Optional
from .provider import OpenSslPkiProvider


class CertMaker:

    DEFAULT_PKI_PROVIDER = OpenSslPkiProvider()

    def __init__(self, pki_provider=None):
        self.pki_provider = pki_provider
        if self.pki_provider is None:
            self.pki_provider = CertMaker.DEFAULT_PKI_PROVIDER

    def remove_passphrase(
        self,
        key_in_path: str,
        password: str,
        key_out_path: str,
        timeout: int = 10,
    ) -> bool:
        self.pki_provider.remove_passphrase(
            key_in_path, password, key_out_path, timeout
        )

    def generate_private_key(
        self,
        key_path: str,
        password: str,
        bits: int = 2048,
        timeout: int = 10,
    ) -> bool:
        self.pki_provider.generate_private_key(key_path, password, bits, timeout)

    def generate_public_key(
        self,
        public_key_path: str,
        private_key_path: str,
        private_key_password: str,
        subject: str,
        alt_subj_names: Optional[List[str]] = None,
        extended_key_usage: Optional[str] = None,
        validity_in_days: int = 365,
        timeout: int = 10,
    ) -> bool:
        self.pki_provider.generate_public_key(
            public_key_path,
            private_key_path,
            private_key_password,
            subject,
            alt_subj_names,
            extended_key_usage,
            validity_in_days,
            timeout,
        )

    def create_csr(
        self,
        csr_path: str,
        key_path: str,
        password: str,
        crt_path: str,
        timeout: int = 10,
    ) -> bool:
        self.pki_provider.create_csr(csr_path, key_path, password, crt_path, timeout)

    def sign_csr(
        self,
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
        self.pki_provider.sign_csr(
            csr_path,
            crt_path,
            ca_key_path,
            ca_key_password,
            ca_crt_path,
            serial,
            alt_subj_names,
            extended_key_usage,
            validity_in_days,
            timeout,
        )

    def create_ca_root():
        pass

    def create_sa_root():
        pass

    def create_server_certificate():
        pass

    def create_client_certificate():
        pass

    def create_pki(pki):
        """Create keypairs of a PKI using a tree-based PKI model. Visualization of
        the PKI tree is possible trough extensions (e.g. graphviz).
        """
        pass
