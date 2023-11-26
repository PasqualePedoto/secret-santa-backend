from fastapi import FastAPI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()


@app.get("/healthychecker")
def read_root():
    return {"Hello": "World"}

@app.get("/sendEmail")
def sendEmail():
    # Imposta le tue credenziali
    email_address = 'pasquale.pedoto123@gmail.com'
    password = 'hzldjaotjvutdrbi'

    # Crea il messaggio
    subject = 'Oggetto della mail'
    body = 'Corpo del messaggio'

    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = 'ivanop92@gmail.com'
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    # Connessione al server SMTP di Gmail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Avvia la connessione TLS
        server.login(email_address, password)
        server.send_message(message)

    return {
        "status": "Email inviata"
    }
