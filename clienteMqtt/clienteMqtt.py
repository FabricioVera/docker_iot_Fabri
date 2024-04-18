import asyncio, ssl, certifi, logging, os, sys
import aiomqtt

logging.basicConfig(format='%(asctime)s - cliente mqtt - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

global cont
cont = 0

async def publicar_contador(client):
    global cont
    while True:
        await asyncio.sleep(5)
        await client.publish(os.environ['TOPICOCONTADOR'], payload=cont)

async def contador():
    global cont
    while True:
        await asyncio.sleep(3)
        cont=cont+1
        logging.info(cont)

async def leer_topicos(client):
    async for message in client.messages:
            if message.topic.matches(os.environ['TOPICOA']):
                logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))
            if message.topic.matches(os.environ['TOPICOB']):
                logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

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
        #await publicar_contador(client)
        async with asyncio.TaskGroup() as tg:
            tg.create_task(contador())
            tg.create_task(publicar_contador(client))
            tg.create_task(leer_topicos(client))
        
            

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Saliendo del docker...")
        sys.exit(0)