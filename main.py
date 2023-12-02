from email.message import EmailMessage
import uvicorn
from fastapi import FastAPI, HTTPException
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import mimetypes
from email.utils import make_msgid
import smtplib
import base64
import mimetypes
import imghdr

from schemas import SecretSanta
from config import settings
from Exceptions import ParsingErrorExceptions, ValidationErrorExceptions, SendMailException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthychecker")
def read_root():
    return {"STATUS": "Send mail server is running"}

@app.post("/sendMail")
def send_mail(payload: SecretSanta):
    response = dict()
    
    try:
        if not payload.secretSanta:
            raise ParsingErrorExceptions(
                error_code=400, 
                error_message="Parsing error: modify payload and retry"
                )
    
        if not isinstance(payload.secretSanta, list):
            raise ValidationErrorExceptions(
                error_code=403, 
                error_message="Validation error: modify payload and retry"
                )
        
        print(payload.secretSanta)

        # Define email and password of secret santa managment
        email = str(settings.EMAIL)
        password = str(settings.PASSWORD)

        for index in range(len(payload.secretSanta)):
            print("EMAIL: " + payload.secretSanta[index]["sender"]["email"])
            print("NOME: " + payload.secretSanta[index]["sender"]["name"])
            print("EMAIL DEL SENDER: " + str(settings.EMAIL))

            # mail subject
            subject = "SECRET SANTA"

            message = EmailMessage()

            message["From"] = email
            message["To"] = payload.secretSanta[index]["sender"]["email"]
            message["Subject"] = subject

            # now create a Content-ID for the image
            cid = make_msgid()[1:-1]

            # set an html body
            message.set_content("""\
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Document</title>
                </head>
                <body>
                    <div>
                    <p>Oh oh oh """ + payload.secretSanta[index]["sender"]["name"] + """,</p>
                    <p>Il Natale è alle porte e Babbo Natale ha bisogno di te!</p>
                    <p>Sarai il Secret Santa di:</p>
                    <div style="height: 20px"></div>
                    <p></p>
                    </div>
                    <figure>
                    <img src="cid:{image_cid}" alt="receiver-secret-santa" style="width: 100%" />
                    </figure>
                </body>
                </html>
            """.format(image_cid=cid), subtype="html")

            file_path = '/Users/pasqualepedoto/Downloads/images.jpeg'

            extends = imghdr.what(file_path)
            maintype = ""
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                maintype = "image"
            
            # Add image into the email
            with open(file_path, "rb") as img:
                message.add_related(
                    # Read image
                    img.read(), 
                    # Define file type
                    maintype=maintype, 
                    # Define file extends
                    subtype=extends, 
                    # Add content-id define precently
                    cid=f"<{cid}>")

            # Open connection with smtp.gmail.com server at port 587
            with smtplib.SMTP(str(settings.SERVER_NAME), int(settings.SERVER_PORT)) as server:
                server.starttls()
                server.login(email, password)
                result = server.send_message(message)

            response["status"] = 200
            response["message"] = "Email inviata con successo"
    
    except ParsingErrorExceptions as exc:
        response["error_code"] = exc.error_code
        response["error_message"] = exc.error_message

        raise HTTPException(status_code=exc.error_code, detail=response)
    
    except ValidationErrorExceptions as exc:
        response["error_code"] = exc.error_code
        response["error_message"] = exc.error_message

        raise HTTPException(status_code=exc.error_code, detail=response)

    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error")

    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
