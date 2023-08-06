from qrcode import Qrcode
from dados import Dados
from pdf import header


class Cracha:

    def __init__(self, usuario_github=None, url_facebook=None, url_instagram=None):
        self._github = usuario_github
        self._url_facebook = url_facebook
        self._url_instagram = url_instagram

    @property
    def url_facebook(self):
        return self._url_facebook

    @property
    def url_instagram(self):
        return self._url_instagram

    @property
    def github(self):
        return self._github

    # badge
    def cracha(self):
        if self.url_facebook != None:
            Qrcode(self.url_facebook).qrcode().png(
                "Facebook.png", scale=6, module_color=[228, 87, 118], background=[248, 197, 33])
        if self.url_instagram != None:
            Qrcode(self.url_instagram).qrcode().png("Instagram.png", scale=6,
                                                    module_color=[228, 87, 118], background=[248, 197, 33])
        if self.url_facebook == None and self.url_instagram == None:
            Qrcode('https://github.com/' +
                   self.github).qrcode().png("Github.png", scale=6, module_color=[228, 87, 118], background=[248, 197, 33])

        dados = Dados(self.github).github()
        if dados != 0:
            header(dados, self.url_facebook, self.url_instagram)
