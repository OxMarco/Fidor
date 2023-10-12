import logging
import queue
from robodog.Thread import GenericThread
import serial
from pynmeagps.nmeareader import NMEAReader

class GPSThread(GenericThread):  
    def name(self) -> str:
        return "GPS Thread"

    def init(self):
        super().init()
        self.serial = serial.Serial(self.args[0], 9600, timeout=5.0)

    def main(self):
        with self.ser as serial_stream:
            nmeareader = NMEAReader(serial_stream)
            for (_, parsed_data) in nmeareader:
                if(parsed_data.identity == 'GNGGA'):
                    temp = {
                        "hdop": parsed_data.HDOP,
                        "satellites": parsed_data.numSV,
                        "timestamp": parsed_data.time,
                        "lat": parsed_data.lat,
                        "lon": parsed_data.lon, 
                        "alt": parsed_data.alt
                    }
                    try:
                        self.args[1].put(temp, timeout=2)
                    except queue.Full:
                        logging.error("Queue is full")
                        pass
