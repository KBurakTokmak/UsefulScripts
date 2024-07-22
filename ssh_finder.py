import nmap
import paramiko
import argparse
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scan_network(network):
    logger.info(f"Starting fast network scan for {network}")
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=network, arguments='-sn')
    except Exception as e:
        logger.error(f"Network scan failed: {e}")
        return []
    
    hosts = nm.all_hosts()
    logger.info(f"Found {len(hosts)} active devices on the network")
    return hosts

def ssh_connect(ip, username, password):
    logger.debug(f"Attempting to SSH into {ip} with username '{username}'")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=5)
        logger.info(f"Successfully connected to {ip}")
        return True
    except paramiko.AuthenticationException:
        logger.warning(f"Authentication failed for {ip}")
        return False
    except paramiko.SSHException as e:
        logger.error(f"SSHException for {ip}: {e}")
        return False
    except paramiko.ssh_exception.NoValidConnectionsError:
        logger.error(f"No valid connections for {ip}")
        return False
    except socket.error as e:
        logger.error(f"Socket error for {ip}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error for {ip}: {e}")
        return False
    finally:
        client.close()

def main(network, username, password):
    logger.info(f"Starting the script with network: {network}, username: {username}")
    hosts = scan_network(network)
    if not hosts:
        logger.error("No hosts found on the network.")
        return

    successful_ips = []

    for host in hosts:
        if ssh_connect(host, username, password):
            successful_ips.append(host)

    if successful_ips:
        logger.info("Successfully connected to the following IPs:")
        for ip in successful_ips:
            logger.info(ip)
    else:
        logger.warning("No successful connections were made.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan a local network and SSH into devices.')
    parser.add_argument('network', type=str, help='The network to scan (e.g., 192.168.1.0/24)')
    parser.add_argument('username', type=str, help='The SSH username')
    parser.add_argument('password', type=str, help='The SSH password')
    args = parser.parse_args()

    main(args.network, args.username, args.password)
