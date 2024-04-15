This program allows a few packets to be sent to an IP address and a series of ports.

This program uses the library scapy in order to function. If you have yet to install scapy on your machine,
please run "pip3 install scapy" or "sudo apt-get install scapy"

To run this program, call it with "python3 flood.py -i 192.168.0.1 -p 80 443 -s 8 -m 3"

    -i command: Specifies the target IP address.
    -p command: Specifies the target ports. This can be a single port or a series of ports.
    -s command: Determines the size of the packets to be sent. Typically, smaller packets have a more powerful effect.
    -m command: Selects the attack mode:
        -m 1 is for UDP flood
        -m 2 is for SYN flood
        -m 3 runs both SYN and UDP floods

Disclaimer: This is a simple project for demonstration purposes. I do not advocate for any malicious use of this Python script.
