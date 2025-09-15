import requests
import logging

class AlertManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def alert_console(self, msg):
        if self.config.get('enable_console', True):
            self.logger.warning(f"ALERT: {msg}")

    def alert_file(self, msg):
        # already logged, but duplicate if desired
        if self.config.get('enable_file', True):
            self.logger.error(f"ALERT_FILE: {msg}")

    def alert_webhook(self, msg):
        url = self.config.get('webhook_url')
        if url:
            try:
                requests.post(url, json={'text': msg}, timeout=5)
            except Exception as e:
                self.logger.error(f"Failed to send webhook alert: {e}")

    def send(self, msg):
        self.alert_console(msg)
        self.alert_file(msg)
        self.alert_webhook(msg)
