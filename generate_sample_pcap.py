from scapy.all import IP, TCP, UDP, ICMP, wrpcap
pkts = []
pkts.append(IP(src="192.168.1.10", dst="93.184.216.34")/TCP(sport=52344,dport=80)/("GET / HTTP/1.1"))
pkts.append(IP(src="192.168.1.11", dst="93.184.216.34")/TCP(sport=52345,dport=80)/("GET /favicon.ico"))
pkts.append(IP(src="10.0.0.5", dst="192.168.1.1")/TCP(sport=44444,dport=22)/("SSH-2.0-OpenSSH"))
pkts.append(IP(src="172.16.0.2", dst="8.8.8.8")/UDP(sport=54321,dport=53)/b"\x00\x01")
pkts.append(IP(src="192.168.1.12", dst="203.0.113.5")/TCP(sport=52346,dport=80)/("GET /index"))
pkts.append(IP(src="192.168.1.15", dst="198.51.100.8")/TCP(sport=60000,dport=4444)/("X"*2000))
pkts.append(IP(src="192.168.1.16", dst="93.184.216.34")/TCP(sport=52348,dport=80)/("Hello"))
pkts.append(IP(src="192.168.1.17", dst="203.0.113.6")/UDP(sport=55555,dport=12345)/("Data"))
pkts.append(IP(src="203.0.113.9", dst="192.168.1.10")/TCP(sport=80,dport=52344)/("HTTP/1.1 200 OK"))
pkts.append(IP(src="10.0.0.6", dst="192.168.1.1")/TCP(sport=34567,dport=22)/("SSH-2.0-Exploit"))
wrpcap("data/samples.pcap", pkts)
print("Wrote data/samples.pcap with", len(pkts), "packets")