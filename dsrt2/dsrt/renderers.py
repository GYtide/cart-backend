from rest_framework.renderers import BaseRenderer

class BinaryRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data
