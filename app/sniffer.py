import os, sys, argparse
from scapy.all import sniff, IP, TCP, UDP, ICMP
from app.utils import write_dicts_to_csv
from app.logger import setup_logger
from app.signatures import SignatureEngine
from app.alerts import AlertManager
from app import socketio

logger = setup_logger({'logfile':'logs/ids_lite.log'})
sig_engine = SignatureEngine({}, logger)
alerter = AlertManager({}, logger)

def packet_handler_live(packet, out_csv):
    record = {}
    try:
        record['size'] = len(packet)

        # IP layer
        if packet.haslayer(IP):
            ip = packet[IP]
            record['src'], record['dst'] = ip.src, ip.dst
        else:
            record['src'] = record['dst'] = ''

        # Protocol
        if packet.haslayer(TCP):
            record['proto'] = 'TCP'
            tcp = packet[TCP]
            record['sport'], record['dport'] = tcp.sport, tcp.dport
        elif packet.haslayer(UDP):
            record['proto'] = 'UDP'
            udp = packet[UDP]
            record['sport'], record['dport'] = udp.sport, udp.dport
        elif packet.haslayer(ICMP):
            record['proto'] = 'ICMP'
            record['sport'] = record['dport'] = 0
        else:
            record['proto'] = 'OTHER'
            record['sport'] = record['dport'] = 0

        # Console logging
        logger.info(f"pkt src={record['src']} dst={record['dst']} proto={record['proto']} dport={record['dport']} size={record['size']}")

        # Signatures
        alerts = sig_engine.check_all(record)
        if alerts:
            alerter.send(f"Signatures triggered: {alerts} for {record}")

        # CSV
        write_dicts_to_csv([record], out_csv, append=True)

        # Live Dashboard via SocketIO
        socketio.emit('new_packet', record)

    except Exception as e:
        logger.exception(f"Error processing packet: {e}")

def live_sniff(out_csv, iface=None, count=0):
    # CSV header
    write_dicts_to_csv([], out_csv, append=False)
    logger.info(f"Starting live sniff on iface={iface or 'default'}, count={count or 'infinite'}")
    sniff(prn=lambda p: packet_handler_live(p, out_csv),
          iface=iface, store=0, count=count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--iface', default=None)
    parser.add_argument('--count', type=int, default=0)
    parser.add_argument('--out-csv', default='data/packets.csv')
    args = parser.parse_args()

    if args.live:
        live_sniff(args.out_csv, iface=args.iface, count=args.count)
