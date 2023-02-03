import adafruit_dht
import board
import ssl
import time
import paho.mqtt.client as mqtt


## Sélection du DHT sur le port GPIO
dht_device = adafruit_dht.DHT11(board.D9)


### CLIENT MQTT
topic = "/v1.6/devices/MACHINE" #Permet de donner le topic où la raspberry publie les donnés 
TLS_CERT_PATH="/Chemin/du/certificat/" #Donne le chemin du certificat TLS/SSL 



client = mqtt.Client 
client.username_pw_set("TOKEN","") #Token du compte ubidots qui permet de donner le compte auquel le raspberry se connecte
client.tls_set(ca_certs=TLS_CERT_PATH, certfile=None,keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

#ca_certs : chemin vers le certificat d'autorité de certification utilisé pour vérifier le certificat du serveur.
#certfile : chemin vers le certificat du client, qui peut être utilisé pour s'authentifier auprès du serveur ici défini sur None.
#keyfile : chemin vers la clé privée associée au certificat du client (ici il y en a pas car c'est égale à NONE).
#cert_reqs : niveau de vérification du certificat du serveur, défini ici sur ssl.CERT_REQUIRED pour indiquer que le certificat du serveur doit être valide.
#tls_version : version de la spécification TLS utilisée pour la connexion, défini ici sur ssl.PROTOCOL_TLSv1_2 pour indiquer la version TLS 1.2.
#ciphers : jeu de chiffrements supportés pour la connexion, défini ici sur "None" pour utiliser les chiffrements par défaut.


client.tls_insecure_set(False)
client.connect("industrial.api.ubidots.com", 8883) #Port ubidots ouvert pour la connexion


# ce while permet de récupérer et de publier les donnés du capteur sur le dashboard ubidots
while (1) :
    temp = dht_device.temperature
    humidity = dht_device.humidity
    msg = '{"temperature": %s, "humidity":%s}' % (temp, humidity)
    client.publish(topic,msg)
    time.sleep(30)
