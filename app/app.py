from flask import Flask, render_template
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

# Lista de portais de notícias
PORTAIS = {
    "IGN": "https://br.ign.com/",
    "Gamespot": "https://www.gamespot.com/",
    "The Verge": "https://www.theverge.com/games/",
    "Eurogamer": "https://www.eurogamer.net/",
    "Polygon": "https://www.polygon.com/"
}

# Intervalo de atualização (em horas)
INTERVALO_ATUALIZACAO = 8

app = Flask(__name__)

# Dicionário para armazenar as notícias
noticias = {}

def buscar_noticias():
    global noticias
    noticias = {}
    for nome, url in PORTAIS.items():
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        noticias_portal = []
        for noticia in soup.find_all("article"):
            titulo = noticia.find("h2").text
            resumo = noticia.find("p").text
            link = noticia.find("a")["href"]
            noticias_portal.append({
                "titulo": titulo,
                "resumo": resumo,
                "link": link
            })
        noticias[nome] = noticias_portal

@app.route("/")
def index():
    global noticias
    ultima_atualizacao = datetime.now() - timedelta(hours=INTERVALO_ATUALIZACAO)
    if datetime.now() > ultima_atualizacao:
        buscar_noticias()
    return render_template("index.html", noticias=noticias)

if __name__ == "__main__":
    app.run(debug=True)
