class ObjectDetector():
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def process(self, frame):
        raise NotImplementedError("Child classes should override this method")
