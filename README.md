# twilio-whatsapp-bot

This bot is used for consulting dollar prices from a public web page.
It uses twilio whatsapp messages api for chating, python for the logical proces and ngrok for internet exposure.

Our main file is a Flask Python web app located on a local server in our PC. The web scrapping files are located on our PC's too.
As our python files runs in a local server we have to expose it to the internet for being able to access from there. For this we are using an ngrok webhook.

For accessing the chat-bot you have to send a message to this number (+1 (415) 523-8886) saying "join dance-stand". Type "ayuda" or "help" for a help message.

////////// package path //////////

(see package_path.png)

1. Messages come out of the client and travel to Twilio servers. There, through some configuration in "when a message comes in" we are redirecting this message to our ngrok server URL through an HTTP package through a preset port.
2. Ngrok is a "door" or "tunnel" to our internet-exposed local server so the package is received by our PC and processed by our python program.
3. Our python program decides what to do with the message. For example, he reads it and depending on its content do something or not.
4. Through python we sent back another message, it goes for the same path as when it comes in. It goes from our PC to ngrok, from ngrok to twilio and from twilio to our clients whatsapp and that's all.
