import cv2
from flask import Flask, Response, render_template
from robodog.Thread import GenericThread

class WebAppThread(GenericThread):
    app = Flask(__name__)
    app.run(host='0.0.0.0', port=8000, threaded=False, debug=False)

    def name(self) -> str:
        return "Web App Thread"

    def run(self):
        self.init()

    def generate_frames(self):
        while not self.stop_signal.is_set():
            if self.args[0] is not None:
                flag, encoded_image = cv2.imencode('.jpg', self.args[0])
                if flag:
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')


    @app.route('/video')
    def video(self):
        return Response(self.generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/')
    def index():
        return render_template('index.html')
