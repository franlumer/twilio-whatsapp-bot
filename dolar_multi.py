# scraper
import requests
from bs4 import BeautifulSoup
import unicodedata
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# --------------------

# busqueda('dolar blue')
# busqueda('won') // no disponible en la web
# busqueda('dolar oficial')
# busqueda('dolar mep/bolsa')
# busqueda('contado con liqui')
# busqueda('dolar cripto')
# busqueda('dolar tarjeta')

# funciones de busqueda (won no esta disponible actualmente)

# --------------------

monedas = ['dolar blue','dolar oficial','dolar mep/bolsa','contado con liqui','dolar cripto','dolar tarjeta']

def normalizar_texto(texto): # cubre las posibles entradas que pueda tener el usuario
    # convierte la entrada del usuario a minusculas sin acentos 
    texto = texto.lower()
    # Eliminar acentos
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def conexion(): # realiza la conexion para poder scrapear la web
    
    base_url = 'https://dolarhoy.com/' # link - No tocar!!
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'} # heades predeterminados para evitar errores
    page = requests.get(base_url, headers=headers) # establece los headers
    soup = BeautifulSoup(page.text, 'html.parser') # convierte el codigo HTML a un objeto de bs4
    return soup 

def busqueda(obj): # extrae el objeto segun lo que se necesite

    if normalizar_texto(obj) == "dolar blue":              # dolar blue tiene una estructura diferente asi que lo tratamos por aparte
        return extraccion_blue()
    
    elif normalizar_texto(obj) == "todo":
        mensaje = ''
        soup = conexion()
        div = soup.find_all('div', class_='tile is-child') 
        for a in monedas:
            if a == 'dolar blue': mensaje = mensaje + extraccion_blue() + '\n\n'
            else:
                for i in div:                                     
                    titulo = i.find('a', class_='title')
                    if titulo != None and normalizar_texto(titulo.text) == a: 
                        raw = i                                                                 
                        mensaje = mensaje + extraccion(raw, titulo) + '\n\n' 
        return str(mensaje.strip())

    else:
        soup = conexion()
        div = soup.find_all('div', class_='tile is-child') # extrae todos los marcos
        for i in div:                                      # por cada marco extrae el titulo y lo compara
            titulo = i.find('a', class_='title')
            if titulo != None and normalizar_texto(titulo.text) == normalizar_texto(obj): # si el titulo coincide con el requerido: 
                raw = i                                                                   # define raw y llama a extraccion()
                return extraccion(raw, titulo)

def extraccion_blue():
    soup = conexion()
    raw = soup.find('div', class_='tile is-child only-mobile')
    titulo = raw.find('a', class_='title')
    resultado = extraccion(raw, titulo)
    return resultado

def extraccion(raw, titulo): # trabaja el texto crudo (raw) para extraer los precios

    compra = raw.find('div',class_='compra')                            # extrae el div 'compra' 
    if compra.find('div', class_='val') == None: precio_compra = '-'    # en caso de que el valor este vacio lo reemplaza por '-'
    else: precio_compra = compra.find('div', class_='val').text         # en caso de que tenga un valor, toma ese mismo

    venta = raw.find('div',class_='venta')                
    wrapper = venta.find('div',class_='venta-wrapper')    
    if wrapper.find('div', class_='val') == None: precio_venta = '-'
    else: precio_venta = wrapper.find('div', class_='val').text

    #print(f'{titulo.text}\ncompra: {precio_compra}\nventa: {precio_venta}\n')
    resultado = f'*{titulo.text}*\nCompra: {precio_compra}\nVenta: {precio_venta}'
    return resultado

print(busqueda('todo'))