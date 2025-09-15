import time
from collections import defaultdict

class SignatureEngine:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.ssh_counter = defaultdict(list)  # src_ip -> [timestamps]

    def check_ssh_bruteforce(self, record):
        if not self.config.get('ssh_bruteforce', {}).get('enabled', False):
            return False
        src = record.get('src')
        dst_port = int(record.get('dport', 0) or 0)
        if dst_port == 22:
            now = time.time()
            window = 60  # second window
            self.ssh_counter[src].append(now)
            # remove old
            self.ssh_counter[src] = [t for t in self.ssh_counter[src] if now - t <= window]
            threshold = self.config['ssh_bruteforce'].get('threshold_per_minute', 10)
            if len(self.ssh_counter[src]) >= threshold:
                self.logger.warning(f"Signature: SSH brute-force suspected from {src} ({len(self.ssh_counter[src])} hits in last minute)")
                return True
        return False

    def check_suspicious_ports(self, record):
        ports = self.config.get('suspicious_ports', [])
        dport = int(record.get('dport', 0) or 0)
        if dport in ports:
            self.logger.warning(f"Signature: Connection to suspicious port {dport} from {record.get('src')}")
            return True
        return False

    def check_all(self, record):
        alerts = []
        if self.check_ssh_bruteforce(record):
            alerts.append('ssh_bruteforce')
        if self.check_suspicious_ports(record):
            alerts.append('suspicious_port')
        return alerts
