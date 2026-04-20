import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ======================================================
# CONFIGURAÇÕES
# ======================================================
URL = "https://sitepd.org.br/"  # coloque o site real aqui
PALAVRAS_CHAVE = [
    "contribuição",
    "isenção",
    "carta",
    "não pagar",
    "prazo",
    "sindicato",
    "oposição",
    "presenncial"
]

# Envio de e-mail
EMAIL_ORIGEM = "faustosasdelli@gmail.com"
SENHA_APP = "idcr ioun sabb fbdd"             #aqui é a senha gerada pelo app do google
EMAIL_DESTINO = "faustosasdelli@gmail.com"

# Arquivo usado para evitar alertas repetidos
HISTORICO_FILE = "ultimo_resultado.txt"


# ======================================================
# FUNÇÃO PARA ENVIAR EMAIL
# ======================================================
def enviar_email(assunto, mensagem):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = EMAIL_DESTINO
        msg["Subject"] = assunto

        msg.attach(MIMEText(mensagem, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ORIGEM, SENHA_APP)
        server.send_message(msg)
        server.quit()

        print("Email enviado com sucesso!")

    except Exception as e:
        print("Erro ao enviar email:", e)


# ======================================================
# LÊ O ÚLTIMO RESULTADO SALVO (SE EXISTIR)
# ======================================================
def ler_ultimo_resultado():
    if not os.path.exists(HISTORICO_FILE):
        return ""
    with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


# ======================================================
# SALVA RESULTADO ATUAL PARA NÃO ALERTAR DE NOVO
# ======================================================
def salvar_resultado(texto):
    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        f.write(texto)


# ======================================================
# VERIFICA O SITE
# ======================================================
def verificar_site():
    try:
        resposta = requests.get(URL, timeout=20)
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")
        conteudo = soup.get_text().lower()

        encontrados = []
        for palavra in PALAVRAS_CHAVE:
            if palavra.lower() in conteudo:
                encontrados.append(palavra)

        from datetime import datetime
        print("Rodou em:", datetime.now())

        # Se nada for encontrado, não faz nada
        if not encontrados:
            print("Nenhuma palavra relevante encontrada.")
            return

        # Junta as palavras encontradas
        resultado_atual = ", ".join(encontrados)

        # Compara com o último resultado salvo para evitar alertas repetidos
        ultimo = ler_ultimo_resultado()

        if resultado_atual == ultimo:
            print("Novidades já notificadas anteriormente. Sem envio...")
            return

        # Enviar alerta
        mensagem = (
            f"As seguintes palavras foram encontradas no site:\n\n"
            f"{resultado_atual}\n\n"
            f"URL: {URL}"
        )

        enviar_email(
            "Nova atualização no site do sindicato",
            mensagem
        )

        # Salva o novo resultado
        salvar_resultado(resultado_atual)

    except Exception as e:
        print("Erro ao acessar o site:", e)


# ======================================================
# PONTO DE ENTRADA
# ======================================================
if __name__ == "__main__":
    verificar_site()