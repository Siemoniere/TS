from scapy.all import *

def pokaz(pkt):
    print("Sniff: wykryto pakiet:")
    pkt.summary()
    pkt.show()

def sniff_icmp(timeout=10):
    print(f"Sniffuję ICMP przez {timeout} sekund...")
    pkts = sniff(filter="icmp", prn=pokaz, timeout=timeout)
    wrpcap("capture.pcap", pkts)  # Zapis do pliku
    for pkt in pkts:
        print("="*50)
        pkt.show()
        
if __name__ == "__main__":
    sniff_icmp(10)
