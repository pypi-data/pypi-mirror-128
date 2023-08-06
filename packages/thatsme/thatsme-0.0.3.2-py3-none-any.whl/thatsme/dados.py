import urllib.request
import json


class Dados():

    __slots__ = ['_nome']

    def __init__(self, nome):
        self._nome = nome

    @property
    def nome(self):
        return self._nome

    def github(self):
        with urllib.request.urlopen("https://api.github.com/users/{}".format(self.nome)) as url:
            dados = json.loads(url.read().decode())
        dados = 0

        return dados
