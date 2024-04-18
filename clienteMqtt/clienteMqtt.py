import asyncio, ssl, certifi, logging, os
import aiomqtt

logging.basicConfig(format='%(asctime)s - cliente mqtt - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')


async def publicar_contador(client):
    while True:
        await asyncio.sleep(5)
        await client.publish(os.environ['TOPICOCONTADOR'], payload=0.38)



async def main():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    async with aiomqtt.Client(
        os.environ['SERVIDOR'],
        port=8883,
        tls_context=tls_context,
    ) as client:
        #SUBSCRIPCIONES A TOPICOS A y B:
        await client.subscribe(os.environ['TOPICOA'])
        await client.subscribe(os.environ['TOPICOB'])
        await publicar_contador(client)
        async for message in client.messages:
            if message.topic.matches(os.environ['TOPICOA']):
                logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))
            if message.topic.matches(os.environ['TOPICOB']):
                logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))
            

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Saliendo del docker...")