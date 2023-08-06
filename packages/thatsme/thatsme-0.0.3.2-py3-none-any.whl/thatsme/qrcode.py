import pyqrcode
import png


class Qrcode:

    def __init__(self, url_social):
        self._url_social = url_social

    @property
    def url_social(self):
        return self._url_social

    def qrcode(self):
        qr = pyqrcode.create(self.url_social)
        return qr
