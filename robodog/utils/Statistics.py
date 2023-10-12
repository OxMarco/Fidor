import json
from datetime import datetime
import psutil

class Statistics():
    @staticmethod
    def hardware(show_temp=False, show_fans=False, show_battery=True):
        epoch = psutil.boot_time()
        dt_object = datetime.fromtimestamp(epoch)

        return {
            "cpu_count": psutil.cpu_count(),
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory(),
            "disk_usage": psutil.disk_usage('/'),
            "temp": psutil.sensors_temperatures() if show_temp else 0,
            "fans": psutil.sensors_fans() if show_fans else 0,
            "battery": psutil.sensors_battery() if show_battery else 0,
            "boot_date": dt_object.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def processes():
        process_list = []
        for proc in psutil.process_iter(['pid', 'name']):
            process_list.append(proc.info)
        
        process_list_json = json.dumps(process_list, indent=4)
        
        return process_list_json

    @staticmethod
    def video(frame):
        return {
            "frame_size": frame.shape,
        }
