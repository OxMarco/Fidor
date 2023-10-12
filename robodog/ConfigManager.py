import os

class ConfigManager:    
    @staticmethod
    def get_configs():
        return {
            "url": os.environ.get('URL', 'http://127.0.0.1:8000'),
            "serial_port": os.environ.get('SERIAL_PORT', '/dev/serial0'),
        }
