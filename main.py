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
from config import Settings
from Exceptions import ParsingErrorExceptions, ValidationErrorExceptions, SendMailException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8010",
]

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
        if not payload.secretList:
            raise ParsingErrorExceptions(
                error_code=400, 
                error_message="Parsing error: modify payload and retry"
                )
    
        if not isinstance(payload.secretList, list):
            raise ValidationErrorExceptions(
                error_code=403, 
                error_message="Validation error: modify payload and retry"
                )

        email = Settings.EMAIL
        password = Settings.PASSWORD

        subject = "SECRET SANTA"

        message = EmailMessage()

        message["From"] = email
        message["To"] = "pasquale.pedoto123@gmail.com"
        message["Subject"] = subject

        # now create a Content-ID for the image
        cid = make_msgid()[1:-1]
        # if `domain` argument isn't provided, it will 
        # use your computer's name

        # set an alternative html body
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
                <p>Oh oh oh 'tizio',</p>
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
        
        with open(file_path, "rb") as img:
            message.add_related(
                img.read(), 
                maintype=maintype, 
                subtype=extends, 
                cid=f"<{cid}>")

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email, password)
            server.send_message(message)

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
