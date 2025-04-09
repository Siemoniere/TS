from scapy.all import *

def send_ping(dst="gov.za"):
    pkt = IP(dst=dst)/ICMP()
    print(f"Wysyłam ping do {dst}")
    response = sr1(pkt, timeout=2, verbose=0)
    if response:
        print("Odpowiedź:")
        response.show()
    else:
        print("Brak odpowiedzi")

if __name__ == "__main__":
    send_ping("papertoilet.com")
