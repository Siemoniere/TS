from scapy.all import *
from package import send_ping
from sniffer import sniff_icmp
import threading
import time

# Sniffer w osobnym wątku
def sniff_async():
    sniff_icmp(timeout=5)

if __name__ == "__main__":
    t = threading.Thread(target=sniff_async)
    t.start()

    time.sleep(1)  # chwila na start sniffowania
    send_ping("papertoilet.com")

    t.join()
