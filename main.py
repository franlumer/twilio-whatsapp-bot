from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import dolar_multi as dm

app = Flask(__name__)

@app.route("/whatsapp", methods = ["GET","POST"])

def whatsapp_reply():
    response = MessagingResponse()
    incoming_msg = dm.normalizar_texto(request.form.get('Body'))
    
    # si el msj entrante es ayuda o help
    if dm.normalizar_texto(incoming_msg) == "help" or dm.normalizar_texto(incoming_msg) == "ayuda":
        help= """Para solicitar los precios de una moneda escriba cual su nombre.

Monedas disponibles: 
- dólar blue
- dólar oficial 
- dólar mep/bolsa
- contado con liqui
- dólar cripto
- dólar tarjeta
"""
        response.message(help)
        return str(response) 
    # en caso de que el msj sea una moneda devuelve los precios
    elif dm.normalizar_texto(incoming_msg) == "1":
        response.message("seccion no disponible")
        return str(response)
    elif dm.normalizar_texto(incoming_msg) in dm.monedas:
        response.message(dm.busqueda(str(incoming_msg)))
        return str(response)
    elif dm.normalizar_texto(incoming_msg) == 'todo' or dm.normalizar_texto(incoming_msg) == 'dolar':
        response.message(dm.busqueda(str(incoming_msg)))
        return str(response)
if __name__ == "__main__":
    app.run(port=8080)