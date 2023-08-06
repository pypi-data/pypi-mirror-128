

class ObjectDetector(object):

    def predict(self, *args, **kwargs):
        raise NotImplementedError

    def destroy_model(self, *args, **kwargs):
        pass