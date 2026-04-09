import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

# CONFIGURAÇÃO
URL = "https://www.decolar.com/passagens-aereas/"  # página de ofertas
PRECO_ALVO = 800  # por exemplo: R$ 800
EMAIL_ORIGEM = "faustosasdelli@gmail.com"
SENHA_APP = "sidcr ioun sabb fbdd"
EMAIL_DESTINO = "faustosasdelli@gmail.com"

def enviar_email(assunto, corpo):
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = EMAIL_ORIGEM
    msg["To"] = EMAIL_DESTINO
    msg.set_content(corpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ORIGEM, SENHA_APP)
        smtp.send_message(msg)

    print("E-mail enviado!")

def buscar_precos():
    resposta = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    })
    if resposta.status_code != 200:
        print("Erro ao acessar a página:", resposta.status_code)
        return []

    soup = BeautifulSoup(resposta.text, "html.parser")

    precos = []
    # Aqui é a parte crítica: você deve inspecionar o HTML real
    # para identificar qual seletor CSS ou tag usa para os preços.
    # Abaixo é só exemplo genérico:
    for tag in soup.select(".price"):  # isso depende totalmente do site real
        texto = tag.get_text().strip()
        # Exemplo de texto: "R$ 699"
        texto = texto.replace("R$", "").replace(".", "").replace(",", ".")
        try:
            valor = float(texto)
            precos.append(valor)
        except:
            continue

    return precos

def main():
    precos = buscar_precos()
    if not precos:
        print("Nenhum preço encontrado.")
        return

    menor_preco = min(precos)
    print("Menor preço encontrado:", menor_preco)

    if menor_preco <= PRECO_ALVO:
        corpo = f"Preço baixo encontrado: R$ {menor_preco}\nVeja: {URL}"
        enviar_email("Alerta de passagem barata Decolar", corpo)
    else:
        print("Ainda não atingiu o valor desejado.")

if __name__ == "__main__":
    main()
