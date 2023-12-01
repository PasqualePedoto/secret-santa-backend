from email.message import EmailMessage
import uvicorn
from fastapi import FastAPI
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


app = FastAPI()


@app.get("/healthychecker")
def read_root():
    return {"STATUS": "Send mail server is running"}

@app.post("/sendMail")
def send_mail(payload: SecretSanta):

    if not payload.secretList:
        raise Exception

    # from email.mime.multipart import MIMEMultipart
    # from email.mime.base import MIMEBase
    # import smtplib
    # import base64
    # from email import encoders
    # from email.header import Header
    #
    # sender_email = "pasquale.pedoto123@gmail.com"
    # receiver_email = "pasquale.pedoto123@gmail.com"
    # password = "hzldjaotjvutdrbi"
    #
    # message = MIMEMultipart()
    # message["From"] = str(Header('HD+ monitoring <%s>' % sender_email))
    # message["To"] = receiver_email
    # message["Subject"] = "'HD+ monitoring - Check video"
    #
    # message.attach(MIMEText("""
    #     <html>
    #     <body>
    #     Hi,
    #     <br>>
    #     Do not respond to this email as it is dynamically generated.
    #     <br>
    #     Running the test on streaming control detected presence of DRM,
    #     so we find it impossible to check for the presence of black-screen,
    #     freeze etc using our machine learning services.
    #     <div style="height=10px"></div>
    #     <div style="height=10px"></div>
    #     <p>Attached is a recording of the streaming.</p>
    #     <b> IT Automation TEAM </b><br>
    #     </html>
    #     </body>"""
    #                         , "html"))
    #
    # video_allegato = MIMEBase("application", "octet-stream")
    # video_allegato.set_payload(open(file_url_uploaded, "rb").read())
    # encoders.encode_base64(video_allegato)
    # video_allegato.add_header(
    #     "Content-Disposition", f"attachment; filename={os.path.basename(file_url_uploaded)}"
    # )
    # message.attach(video_allegato)
    #
    # with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #     server.starttls()
    #     server.login(sender_email, password)
    #     server.send_message(message)
    #
    # return {
    #     "status": "email inviata"
    # }



    email = "pasquale.pedoto123@gmail.com"
    password = "hzldjaotjvutdrbi"

    subject = "SECRET SANTA"
    body = "Pippo"

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
    
    return {
        "status": "email inviata"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
