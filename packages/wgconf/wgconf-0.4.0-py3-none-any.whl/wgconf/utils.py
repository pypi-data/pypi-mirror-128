from ipaddress import IPv4Interface, IPv4Network
from subprocess import PIPE, run
from typing import List, Tuple, Dict
from pathlib import Path
import sys

from wgconf.WireGuardConfiguration import ServerConf, ClientConf


def is_valid_network(ip: str) -> bool:
    """check if network is in valid cidr notation"""
    try:
        IPv4Network(ip)
    except ValueError:
        return False
    return True


def has_enough_addresses(ip: str, num_clients: int) -> bool:
    """check if network has enough addreses for number of clients
    account for network + broadcast addresses + server address"""
    if num_clients > IPv4Network(ip).num_addresses - 3:
        return False
    return True


def exit_if_no_wg_tools() -> None:
    try:
        run(["wg"])
    except FileNotFoundError:
        sys.exit("You might not have wireguard-tools intalled. Exiting...")


def gen_key_pair() -> Dict[str, str]:
    """generate and return a wireguard key pair"""
    wg_genkey_output = run(["wg", "genkey"], stdout=PIPE)
    wg_pubkey_output = run(
        ["wg", "pubkey"], input=wg_genkey_output.stdout, capture_output=True
    )
    private_key = wg_genkey_output.stdout.decode().strip()
    public_key = wg_pubkey_output.stdout.decode().strip()
    return {"private_key": private_key, "public_key": public_key}


def gen_client_keys(num_clients: int) -> Dict[int, Dict[str, str]]:
    """generate client key pairs and stores them in a dictionary"""
    client_keys_dict = {i: gen_key_pair() for i in range(1, num_clients + 1)}
    return client_keys_dict


def create_confs(
    server_private_key: str,
    server_public_key: str,
    client_keys_dict: Dict[int, Dict[str, str]],
    network_address: IPv4Interface,
    endpoint: str,
    port: int,
    allowed_ips: str,
    path: Path,
) -> Tuple[ServerConf, List[ClientConf]]:
    """create server and client configs"""
    server_ip = network_address + 1
    # initialize client_ip
    client_ip = server_ip

    server_peers_list: List[str] = []
    client_confs: List[ClientConf] = []

    for k in client_keys_dict:
        client_ip += 1
        server_peers_list.append(
            f"[Peer]\n"
            f'PublicKey = {client_keys_dict[k]["public_key"]}\n'
            f"AllowedIPs = {client_ip}\n\n"
        )

        client_confs.append(
            ClientConf(
                client_keys_dict[k]["private_key"],
                client_ip,
                server_public_key,
                allowed_ips,
                endpoint,
                port,
                path,
            )
        )

    server_peers = "".join(server_peers_list)

    server_conf = ServerConf(server_private_key, server_ip, port, server_peers, path)

    return server_conf, client_confs
