from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator
from ipaddress import IPv4Interface
from .utils import (
    exit_if_no_wg_tools,
    gen_key_pair,
    gen_client_keys,
    create_confs,
    is_valid_network,
    has_enough_addresses,
)


def main():
    exit_if_no_wg_tools()

    num_clients = inquirer.text(
        message="Enter number of devices:",
        validate=NumberValidator(),
        filter=lambda result: int(result),
    ).execute()

    def network_validator(result) -> bool:
        """Ensure the input is not empty."""
        return is_valid_network(result) and has_enough_addresses(result, num_clients)

    network = inquirer.text(
        message="Enter a network in CIDR Notation",
        validate=network_validator,
        filter=lambda result: IPv4Interface(result),
        invalid_message="Either invalid CIDR or not enough address space. The default of 10.0.0.0/24 should work for most configurations.",
        default="10.0.0.0/24",
    ).execute()

    endpoint = inquirer.text(
        message="Enter an endpoint for your Wireguard server (e.g. an IP address or hostname):",
    ).execute()

    port = inquirer.text(
        message="Enter a port for your endpoint. Press Enter for default:",
        validate=NumberValidator(),
        filter=lambda result: int(result),
        default="51820",
    ).execute()

    allowed_ips = inquirer.text(
        message="Which IP addresses are allowed to communicate with your client?",
        default=str(network),
    ).execute()

    server_key_pair = gen_key_pair()
    client_keys_dict = gen_client_keys(num_clients)

    server_conf, client_confs = create_confs(
        server_key_pair["private_key"],
        server_key_pair["public_key"],
        client_keys_dict,
        network,
        endpoint,
        port,
        allowed_ips,
    )

    server_conf.write_conf_to_file("01_server.conf", server_conf.make_conf())
    if num_clients <= 20:
        server_conf.generate_qr_code("01_server")

    for i, conf in enumerate(client_confs, start=1):
        conf.write_conf_to_file(f"{i + 1:02d}_client_{i}.conf", conf.make_conf())
        conf.generate_qr_code(f"{i+1:02d}_client_{i}")

    print(
        f"\nWireguard Server: {conf.endpoint}:{server_conf.port}\n"
        f"{i} clients\n"
        "Configuration files and QR codes stored in ./configs"
    )


if __name__ == "__main__":
    main()
