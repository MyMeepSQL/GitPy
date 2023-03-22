import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import datetime

# Paramètres pour l'API OpenMeteo et les informations d'authentification pour votre compte e-mail
LATITUDE = '33.9842'
LONGITUDE = '-6.8675'
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = '587'
EMAIL_LOGIN = 'aovpns@outlook.com'
EMAIL_PASSWORD = r'YE@3E5fVQr*tZ&aUgsPWpT*R9bh89V@Qt@2s%bzUn&ezPQYr36JSXiDN$$*TDq35pv*3mp39hXK#653$$ccw^%8KLNuZ74&o286#ry^PJ7p6@Kv&4SFHy3&7'
DESTINATION_EMAIL = 'thspam35@gmail.com'

# Récupérer les prévisions météo pour aujourd'hui
url = f'https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=weatherdescription,precipitationprobability,temperature,winddirection,windspeed,pressure,humidity&timezone=Europe/Paris&limit=1'
response = requests.get(url).json()
forecast = response['forecast'][0]

# Récupérer les informations météorologiques pour aujourd'hui
weather_description = forecast['weather_description']
precipitation_probability = forecast['precipitation_probability']
temperature = forecast['temperature']
wind_direction = forecast['winddirection']
wind_speed = forecast['windspeed']
pressure = forecast['pressure']
humidity = forecast['humidity']

# Générer le rapport météo pour aujourd'hui
report = f"Rapport météo pour aujourd'hui ({datetime.date.today().strftime('%d/%m/%Y')}) :\n\n"
report += f"Description du temps : {weather_description}\n"
report += f"Probabilité de précipitations : {precipitation_probability}%\n"
report += f"Température : {temperature}°C\n"
report += f"Direction du vent : {wind_direction}°\n"
report += f"Vitesse du vent : {wind_speed} km/h\n"
report += f"Pression atmosphérique : {pressure} hPa\n"
report += f"Humidité : {humidity}%\n"

# Créer un fichier texte pour le rapport
filename = 'rapport_meteo.txt'
with open(filename, 'w') as f:
    f.write(report)

# Configurer le serveur SMTP pour votre compte e-mail
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(EMAIL_LOGIN, EMAIL_PASSWORD)

# Créer un message e-mail avec le fichier texte en pièce jointe
msg = MIMEMultipart()
msg['Subject'] = 'Rapport Météo'
msg['From'] = EMAIL_LOGIN
msg['To'] = DESTINATION_EMAIL
with open(filename, 'rb') as f:
    part = MIMEApplication(f.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    msg.attach(part)

# Envoyer l'e-mail avec le rapport météo en pièce jointe
server.sendmail(EMAIL_LOGIN, DESTINATION_EMAIL, msg.as_string())
server.quit()