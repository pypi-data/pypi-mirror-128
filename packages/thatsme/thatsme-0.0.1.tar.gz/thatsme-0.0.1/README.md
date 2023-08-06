# thatsme

## Crachá personalizado com dados do github e/ou QRcodes dos perfis do Facebook e Instagram no formato PDF

<p> Usuário completo</p>

![Usuário + QRcode do Facebook + QRcod do Instagram](demo/UC.png)

<p> Usuário básico </p>

![Usuário + QRcode do Github](demo/UB.png)

O thatsme foi criado em python3.8. O sistema pode ser usado em Windows, Linux e Mac.

Colaboradores: <br />

1. [Wendel Nunes](https://github.com/WendelSantosNunes) <br />
2. [Eva Luana](https://github.com/evalasilva) <br />

### Descrição:

> O thatsme é um pacote criado durante a disciplina de Programação Orientada a Objetos 2 (POO2), ministrada no curso de Sistema de Informação na Universidade Federal do Piauí# thatsme
## Crachá personalizado com dados do github e/ou QRcodes dos perfis do Facebook e Instagram 

![Usuário + QRcode do Facebook + QRcod do Instagram](demo/UC.png)
<p> Usuário completo </p>

![Usuário + QRcode do Github](demo/UB.png)
<p> Usuário básico </p>

O thatsme foi criado em python3.8. O sistema pode ser usado em Windows, Linux e Mac.


Colaboradores: <br />

1. [Wendel Nunes](https://github.com/WendelSantosNunes) <br />
2. [Eva Luana](https://github.com/evalasilva) <br />

### Descrição:
> O thatsme é um pacote criado durante a disciplina de Programação Orientada a Objetos 2 (POO2), ministrada no curso de Sistema de Informação na Universidade Federal do Piauí-CSHNB.
> Não há intuito comercial, ou governamental. 
> O thatsme foi produzido para fins de aprendizado e experiência em desenvolvimento de pacotes, contudo pode ser utilizado por qualquer usuário do Github que tenha interesse. O projeto possui a Licença do MIT disponibilizada pelo próprio Github.
> O thatsme pode ser utilizado como cartão virtual, em formato PDF, para qualquer pessoa física/jurídica que queira compartilhar suas informações de contato de forma padronizada, elegante e eficiente.

## Requisitos:

1. [python3](https://www.python.org/downloads/)
2. [pip](https://pip.pypa.io/en/stable/installation/)



## Instalação:

### Python3 
1. Windows: [Download](https://www.python.org/downloads/)

2.Linux Debian e derivados.

	~~~ Bash
		$ sudo apt-get install python3
	~~~

### PIP
1. Instalação do PIP - LINUX
 
 	~~~ Debian
		$ sudo  apt-get install python-pip
	~~~
	~~~ Red Hat/ OpenSUSe
		$ sudo  yum install python-pip
	~~~

### thatsme
1. Instalação do thatsme
 
 	pip install thatsme



## Executar o programa:

1. Instale o pacote; 
2. Importe a classe Cracha:
    (from cracha import Cracha); 
3. Crie um objeto da classe:
    
    3.1. O objeto deve enviar como parâmetro("nome_usuario_github","url_perfil_facebook", "url_perfil_instagram");
        from cracha import Cracha

        usuario = Cracha('usuario_github', 'url_perfil_facebook', 'url_perfil_instagram')

        usuario.cracha()
    
    3.2. O parâmetro "nome_usuario_github" é obrigatório;
    3.3. Caso não hajam as URLs dos perfins do Facebook e/ou Instagram, deve ser inserido "None" no local devido;
        
        from cracha import Cracha

        usuario = Cracha('usuario_github', None, 'url_perfil_instagram')

        usuario.cracha()


    3.4. Para o caso de não haver URL do Facebook nem do Instagram será adicionado o QRcode do perfil do usuário no Github;
    3.5. Se o usuário do Github não for encontrado será apresentado o ERROR 404. 
    
O projeto possui a licensa do MIT disponibilizada pelo próprio Github.
> O thatsme pode ser utilizado como cartão virtual paraqualquer pessoa física/jurídica que queira compartilhar suas informações de contato de forma padronizada, elegante e eficiente.

## Requisitos:

1. [python3](https://www.python.org/downloads/)
2. [pip](https://pip.pypa.io/en/stable/installation/)

## Instalação:

### Python3

1. Windows: [Download](https://www.python.org/downloads/)

2. Linux Debian e derivados.

   ```Bash
   	$ sudo apt-get install python3
   ```

### PIP

1. Instalação do PIP - LINUX

   ```Debian
   	$ sudo  apt-get install python-pip
   ```

   ```Red Hat/ OpenSUSe
   	$ sudo  yum install python-pip
   ```

### thatsme

1. Instalação do thatsme

   pip install thatsme

## Executar o programa:

1.  Instale o pacote;

2.  Importe a classe Cracha:
    (from cracha import Cracha);

3.  Crie um objeto da classe:

    3.1. O objeto deve enviar como parâmetro("nome_usuario_github","url_perfil_facebook", "url_perfil_instagram");
    from cracha import Cracha

        usuario = Cracha('usuario_github', 'url_perfil_facebook', 'url_perfil_instagram')

        usuario.cracha()

    3.2. O parâmetro "nome_usuario_github" é obrigatório;

    3.3. Caso não hajam as URLs dos perfins do Facebook e/ou Instagram, deve ser inserido "None" no local devido;

        from cracha import Cracha

        usuario = Cracha('usuario_github', None, 'url_perfil_instagram')

        usuario.cracha()

    3.4. Para o caso de não haver URL do Facebook nem do Instagram será adicionado o QRcode do perfil do usuário no Github;

    3.5. Se o usuário do Github não for encontrado será apresentado o ERROR 404.
