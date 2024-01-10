from scapy.all import Ether, IP, ICMP, sendp, send

eth = Ether(src="00:11:22:33:44:55")

ip = IP(src="192.168.1.100", dst="10.67.19.193")

icmp = ICMP()

packet = eth / ip / icmp

sendp(packet)

packet = ip / icmp
send(packet)
