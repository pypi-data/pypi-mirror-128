from fpdf import FPDF


def header(dados, url_facebook, url_instagram):
    fpdf = FPDF('L', 'mm', (100, 150))
    fpdf.add_page()

    fpdf.image('Rectangle 1.png', 0, 0, 180)
    fpdf.image('Desktop.png', -30, -10, 210)

    # fonte
    fpdf.set_font('helvetica', '', 10)
    fpdf.set_text_color(255, 255, 255)

    # qrcode
    if url_facebook != None and url_instagram != None:
        fpdf.image('Facebook.png', 95, 30, 25)
        fpdf.image('Instagram.png', 95, 60, 25)
    elif url_instagram != None:
        fpdf.image('Instagram.png', 95, 30, 25)
    elif url_facebook != None:
        fpdf.image('Facebook.png', 95, 30, 25)
    else:
        fpdf.image('Github.png', 95, 30, 25)

    # dados do github

    fpdf.image(dados['avatar_url'], 30, 30, 25)
    fpdf.ln(50)
    fpdf.text(30, 60, dados['login'])
    fpdf.ln(3)
    effective_page_width = (fpdf.w - 9*fpdf.l_margin) + 10
    if dados['bio']:
        fpdf.multi_cell(effective_page_width, 5,
                        dados['bio'], border=0, align='C')

    fpdf.output('Crachá.pdf')
