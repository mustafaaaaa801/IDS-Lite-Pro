import csv
import os
from scapy.all import rdpcap

def read_pcap_to_dicts(pcap_path, limit=None):
    packets = rdpcap(pcap_path)
    out = []
    count = 0
    for p in packets:
        if limit and count >= limit:
            break
        record = {}
        try:
            record['size'] = len(p)
            if p.haslayer('IP'):
                ip = p['IP']
                record['src'] = ip.src
                record['dst'] = ip.dst
                record['proto'] = ip.proto
            else:
                record['src'] = ''
                record['dst'] = ''
                record['proto'] = 0
            if p.haslayer('TCP'):
                tcp = p['TCP']
                record['sport'] = tcp.sport
                record['dport'] = tcp.dport
            elif p.haslayer('UDP'):
                udp = p['UDP']
                record['sport'] = udp.sport
                record['dport'] = udp.dport
            else:
                record['sport'] = 0
                record['dport'] = 0
        except Exception:
            continue
        out.append(record)
        count += 1
    return out

def write_dicts_to_csv(dicts, csv_path, append=False):
    os.makedirs(os.path.dirname(csv_path) or '.', exist_ok=True)
    mode = 'a' if append else 'w'
    write_header = True
    if append and os.path.exists(csv_path):
        write_header = False
    with open(csv_path, mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['src','dst','size','proto','sport','dport'])
        if write_header:
            writer.writeheader()
        for d in dicts:
            # ensure all keys exist
            row = {k: d.get(k, '') for k in ['src','dst','size','proto','sport','dport']}
            writer.writerow(row)
