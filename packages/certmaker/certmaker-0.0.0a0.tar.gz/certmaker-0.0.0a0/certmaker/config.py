import os
import tempfile
import uuid
import contextlib

class OpenSslConfig:
    def __init__(self):
        pass

    def create(self, config_node):
        return config_node.__str__()

    @contextlib.contextmanager
    def write(self, config_node):
        config_path = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        with open(config_path, "wb") as config_file:
            config_file.write(config_node.__str__().encode('utf-8'))

        yield config_path

        # Delete temp file
        # os.remove(config_path)


class CaRootConfig(OpenSslConfig):
    pass


class SaRootServerConfig(OpenSslConfig):
    pass


class SaRootClientConfig(OpenSslConfig):
    pass


class OpenSslConfigNode:
    def __init__(self, name=None):
        self.name = name
        if self.name is None:
            self.name = ""
        self.entries = {}
        self._config_nodes = []

    def __str__(self):
        self._config_nodes = []
        self._config_nodes.append(self)
        self.find_config_nodes(self)

        return "".join(
            [
                self.config_node_to_str(config_node) + "\n"
                for config_node in set(self._config_nodes)
            ]
        )

    def find_config_nodes(self, root_config_node):
        for value in root_config_node.entries.values():
            if isinstance(value, OpenSslConfigNode) and value != root_config_node:
                self._config_nodes.append(value)
                self.find_config_nodes(value)

    def config_node_to_str(self, node):
        return (
            "[ "
            + node.name
            + " ]\n"
            + "".join(
                [
                    self.config_entry_to_str(entry) + "\n"
                    for entry in node.entries.items()
                ]
            )
        )

    def config_entry_to_str(self, entry):
        if isinstance(entry[1], OpenSslConfigNode):
            return entry[0] + " = " + entry[1].name
        else:
            return entry[0] + " = " + entry[1]


class CaConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("ca")
        self.entries = {
            "default_ca": CaDefaultConfigNode(),
            "default_startdate": "700101000000Z",
            "default_enddate": "700101000000Z",
        }


class CaDefaultConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("CA_default")
        self.entries = {
            # Directory and file locations.
            "dir": "root/ca",
            "certs": "$dir/certs",
            "crl_dir": "$dir/crl",
            "new_certs_dir": "$dir/newcerts",
            "database": "$dir/index.txt",
            "serial": "$dir/serial",
            "RANDFILE": "$dir/private/.rand",
            # The root key and root certificate.
            "private_key": "$dir/private/denisvasilik-ca-root1.key.pem",
            "certificate": "$dir/certs/denisvasilik-ca-root1.cert.pem",
            # For certificate revocation lists.
            "crlnumber": "$dir/crlnumber",
            "crl": "$dir/crl/denisvasilik-ca-root1.crl.pem",
            "crl_extensions": CrlConfigNode(),
            "default_crl_days": "30",
            # SHA-1 is deprecated, so use SHA-2 instead.
            "default_md": "sha256",
            "name_opt": self,
            "cert_opt": self,
            "default_days": "375",
            "preserve": "no",
            "policy": PolicyStrictConfigNode(),
        }


class PolicyStrictConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("policy_strict")
        self.entries = {
            # The root CA should only sign intermediate certificates that match.
            # See the POLICY FORMAT section of `man ca`.
            "countryName": "match",
            "stateOrProvinceName": "match",
            "localityName": "optional",
            "organizationName": "match",
            "organizationalUnitName": "optional",
            "commonName": "supplied",
            "emailAddress": "optional",
        }


class PolicyLooseConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("policy_loose")
        self.entries = {
            # Allow the intermediate CA to sign a more diverse range of certificates.
            # See the POLICY FORMAT section of the `ca` man page.
            "countryName": "optional",
            "stateOrProvinceName": "optional",
            "localityName": "optional",
            "organizationName": "optional",
            "organizationalUnitName": "optional",
            "commonName": "supplied",
            "emailAddress": "optional",
        }


class ReqConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("req")
        self.entries = {
            # Options for the `req` tool (`man req`).
            "default_bits": "2048",
            "distinguished_name": ReqDistinguishedNameConfigNode(),
            "string_mask": "utf8only",
            # SHA-1 is deprecated, so use SHA-2 instead.
            "default_md": "sha256",
            # Extension to add when the -x509 option is used.
            "x509_extensions": V3CaConfigNode(),
            "attributes": ReqAttributesConfigNode(),
        }


class ReqDistinguishedNameConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("req_distinguished_name")
        self.entries = {
            "countryName": "Country Name (2 letter code)",
            "countryName_min": "2",
            "countryName_max": "2",
            "stateOrProvinceName": "State or Province Name (full name)",
            "localityName": "Locality Name (eg, city)",
            "organizationName": "Organization Name (eg, company)",
            "organizationalUnitName": "Organizational Unit Name (eg, section)",
            "commonName": "Common Name (eg, fully qualified host name)",
            "commonName_max": "64",
            "emailAddress": "Email Address",
            "emailAddress_max": "64",
            # Optionally, specify some defaults.
            "countryName_default": "DE",
            "stateOrProvinceName_default": "Germany",
            "localityName_default": "",
            "0.organizationName_default": "",
            "organizationalUnitName_default": "",
            "emailAddress_default": "",
        }


class ReqAttributesConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("req_attributes")
        self.entries = {
            "challengePassword": "A challenge password",
            "challengePassword_min": "4",
            "challengePassword_max": "20",
        }


class V3CaConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("v3_ca")
        self.entries = {
            # Extensions for a typical CA (`man x509v3_config`).
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid:always,issuer",
            "basicConstraints": "critical, CA:true",
            "keyUsage": "critical, digitalSignature, cRLSign, keyCertSign",
        }


class V3IntermediateCaConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("v3_intermediate_ca")
        self.entries = {
            # Extensions for a typical intermediate CA (`man x509v3_config`).
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid:always,issuer",
            "basicConstraints": "critical, CA:true, pathlen:0",
            "keyUsage": "critical, digitalSignature, cRLSign, keyCertSign",
        }


class UserCertificateConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("usr_cert")
        self.entries = {
            # Extensions for client certificates (`man x509v3_config`).
            "basicConstraints": "CA:FALSE",
            "nsCertType": "client, email",
            "nsComment": "",
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid,issuer",
            "keyUsage": "critical, nonRepudiation, digitalSignature, keyEncipherment",
            "extendedKeyUsage": "clientAuth, emailProtection",
        }


class ServerCertificateConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("usr_cert")
        self.entries = {
            # Extensions for client certificates (`man x509v3_config`).
            "basicConstraints": "CA:FALSE",
            "nsCertType": "server",
            "nsComment": "",
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid,issuer:always",
            "keyUsage": "critical, digitalSignature, keyEncipherment",
            "extendedKeyUsage": "serverAuth",
        }


class MtlsServerCertificateConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("usr_cert")
        self.entries = {
            # Extensions for client certificates (`man x509v3_config`).
            "basicConstraints": "CA:FALSE",
            "nsCertType": "client, server",
            "nsComment": "",
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid,issuer:always",
            "keyUsage": "critical, nonRepudiation, digitalSignature, keyEncipherment",
            "extendedKeyUsage": "clientAuth, serverAuth",
        }


class CrlConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("crl_ext")
        self.entries = {
            # Extension for CRLs (`man x509v3_config`).
            "authorityKeyIdentifier": "keyid:always",
        }


class OcspConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("ocsp")
        self.entries = {
            # Extension for OCSP signing certificates (`man ocsp`).
            "basicConstraints": "CA:FALSE",
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid,issuer",
            "keyUsage": "critical, digitalSignature",
            "extendedKeyUsage": "critical, OCSPSigning",
        }


class ReqExtensionConfigNode(OpenSslConfigNode):
    def __init__(self):
        super().__init__("req_ext")
        self.entries = {
            # Extensions for server certificates (`man x509v3_config`).
            "basicConstraints": "CA:FALSE",
            "nsCertType": "server",
            "nsComment": "",
            "subjectKeyIdentifier": "hash",
            "authorityKeyIdentifier": "keyid,issuer:always",
            "keyUsage": "critical, digitalSignature, keyEncipherment",
            "extendedKeyUsage": "serverAuth",
            "subjectAltName": "",
        }
