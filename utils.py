
import smtplib
import os

PASSWORD = os.environ.get('MAIL_PASSWORD')


def enviar_email(nombre, apellido, correo, dia, mes, hora):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('nrbarbershop.valdivia@gmail.com', PASSWORD)

    email_string = f'''Subject: Confirmacion Hora NR Baber SHOP
    To: {','.join([correo])}
    Estimad@ {nombre} {apellido} su hora para el dia {dia} / {mes} a las {hora}:00 Ha sido agendada con exito.'''

    server.sendmail('nrbarbershop.valdivia@gmail.com', correo,
                    email_string)
