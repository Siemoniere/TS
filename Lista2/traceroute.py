from scapy.all import *

def my_traceroute(dst, max_hops=30):
    print(f"Traceroute do {dst}")
    for ttl in range(1, max_hops + 1):
        pkt = IP(dst=dst, ttl=ttl) / ICMP()
        reply = sr1(pkt, timeout=2, verbose=0)
        if reply is None:
            print(f"{ttl}: brak odpowiedzi")
        elif reply.type == 11:  # Time Exceeded
            print(f"{ttl}: {reply.src}")
        elif reply.type == 0:  # Echo Reply
            print(f"{ttl}: {reply.src} (cel osiągnięty)")
            break
if __name__ == "__main__":
    my_traceroute("papertoilet.com")
