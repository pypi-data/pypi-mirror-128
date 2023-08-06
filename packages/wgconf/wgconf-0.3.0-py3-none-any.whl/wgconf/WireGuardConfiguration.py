from abc import ABC, abstractmethod
from ipaddress import IPv4Interface
from pathlib import Path
from shutil import rmtree
import qrcode as qr
import ipaddress

CONFIG_PATH = Path(".") / "configs"


class WireGuardConfiguration(ABC):
    def __init__(self, private_key: str, ip_address: IPv4Interface):
        self.private_key = private_key
        self.ip_address = ip_address
        self.path = CONFIG_PATH

        if self.path.exists():
            rmtree(self.path)
        self.path.mkdir()

    @abstractmethod
    def make_conf(self):
        """abstract method implemented in subclasses"""
        return

    def generate_qr_code(self, filename: str) -> None:
        """generate qr code from configuration file"""
        with open(self.path / f"{filename}.conf", "r") as input_data:
            img = qr.make(input_data.read())
            img.save(self.path / f"{filename}.png")

    def write_conf_to_file(self, filename: str, conf: str) -> None:
        """write configuration to file"""
        with open(self.path / filename, "w") as f:
            f.write(conf.strip())


class ServerConf(WireGuardConfiguration):
    def __init__(
        self,
        private_key: str,
        ip_address: ipaddress.IPv4Interface,
        port: int,
        peers: str,
    ):

        super().__init__(private_key, ip_address)
        self.port = port
        self.peers = peers

    def make_conf(self) -> str:
        return (
            f"[Interface]\n"
            f"Address = {self.ip_address}\n"
            f"ListenPort = {self.port}\n"
            f"PrivateKey = {self.private_key}\n\n"
            f"{self.peers}"
        )


class ClientConf(WireGuardConfiguration):
    def __init__(
        self,
        private_key: str,
        ip_address: ipaddress.IPv4Interface,
        server_public_key: str,
        allowed_ips: ipaddress.IPv4Network,
        endpoint: str,
        port: int,
    ):

        super().__init__(private_key, ip_address)
        self.server_public_key = server_public_key
        self.allowed_ips = allowed_ips
        self.endpoint = endpoint
        self.port = port

    def make_conf(self) -> str:
        return (
            f"[Interface]\n"
            f"Address = {self.ip_address}\n"
            f"PrivateKey = {self.private_key}\n\n"
            f"[Peer]\n"
            f"PublicKey = {self.server_public_key}\n"
            f"AllowedIPs = {self.allowed_ips}\n"
            f"Endpoint = {self.endpoint}:{self.port}\n\n"
        )
