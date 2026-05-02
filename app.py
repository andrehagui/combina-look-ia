from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def analisar_look(caminho_imagem):
    imagem = Image.open(caminho_imagem).convert("RGB")

    largura, altura = imagem.size

    esquerda = largura * 0.2
    topo = altura * 0.15
    direita = largura * 0.8
    baixo = altura * 0.9

    imagem = imagem.crop((esquerda, topo, direita, baixo))
    imagem = imagem.resize((100, 100))

    pixels = list(imagem.getdata())

    media_r = sum(p[0] for p in pixels) / len(pixels)
    media_g = sum(p[1] for p in pixels) / len(pixels)
    media_b = sum(p[2] for p in pixels) / len(pixels)

    brilho = (media_r + media_g + media_b) / 3

    diferenca_cor = (
        abs(media_r - media_g)
        + abs(media_r - media_b)
        + abs(media_g - media_b)
    )

    # detectar paleta
    if abs(media_r - media_g) < 20 and abs(media_g - media_b) < 20:
        paleta = "Neutra elegante"
        neutro = True
    elif media_r > media_g and media_r > media_b:
        paleta = "Vermelhos / quentes"
        neutro = False
    elif media_g > media_r and media_g > media_b:
        paleta = "Verdes / naturais"
        neutro = False
    elif media_b > media_r and media_b > media_g:
        paleta = "Azuis / frios"
        neutro = False
    else:
        paleta = "Mista"
        neutro = False

    nota = 6.5

    if brilho > 90:
        nota += 0.8

    if brilho > 150:
        nota += 0.5

    if 20 < diferenca_cor < 80:
        nota += 1.2

    if neutro:
        nota += 1.0

    if diferenca_cor > 120:
        nota -= 0.8

    nota = max(5.0, min(round(nota, 1), 10))

    if nota >= 9:
        comentario = "Combinação refinada e muito harmoniosa."
        cores = f"{paleta}"
        estilo = "Elegante premium"
        ocasiao = "Evento / social"
        sugestao = "Look muito bem construído."

    elif nota >= 8:
        comentario = "Boa harmonia visual e ótimo equilíbrio."
        cores = f"{paleta}"
        estilo = "Casual elegante"
        ocasiao = "Uso versátil"
        sugestao = "Acessórios podem elevar ainda mais."

    elif nota >= 7:
        comentario = "Combinação boa, mas há espaço para melhorar."
        cores = f"{paleta}"
        estilo = "Casual"
        ocasiao = "Dia a dia"
        sugestao = "Uma peça neutra pode equilibrar melhor."

    else:
        comentario = "Combinação fraca ou visualmente carregada."
        cores = f"{paleta}"
        estilo = "Desalinhado"
        ocasiao = "Indefinida"
        sugestao = "Simplificar a paleta pode melhorar bastante."

    return nota, comentario, cores, estilo, ocasiao, sugestao


@app.route("/", methods=["GET", "POST"])
def home():
    imagem = None
    nota = None
    comentario = None
    cores = None
    estilo = None
    ocasiao = None
    sugestao = None

    if request.method == "POST":
        arquivo = request.files["foto"]

        if arquivo and arquivo.filename != "":
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
            arquivo.save(caminho)

            imagem = arquivo.filename

            nota, comentario, cores, estilo, ocasiao, sugestao = analisar_look(caminho)

    return render_template(
        "index.html",
        imagem=imagem,
        nota=nota,
        comentario=comentario,
        cores=cores,
        estilo=estilo,
        ocasiao=ocasiao,
        sugestao=sugestao
    )


if __name__ == "__main__":
    app.run(debug=True)