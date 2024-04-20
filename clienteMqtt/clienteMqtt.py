import asyncio, ssl, certifi, logging, os, sys
import aiomqtt

logging.basicConfig(format='%(funcName)s - %(asctime)s - cliente mqtt - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

class CONTADOR:
    def __init__(self):
        self.__contador = 0
    def incrementar(self):
        self.__contador += 1
    def valor(self):
        return self.__contador

async def contar():
    while True:
        await asyncio.sleep(3)
        contador.incrementar()
        logging.info("Incremento de contador a: "+ str(contador.valor()))


async def publicar_contador(client):
    while True:
        await asyncio.sleep(5)
        await client.publish(os.environ['TOPICOCONTADOR'], payload=contador.valor())
        logging.info("Publicando valor de contador.")

async def lectura_topicoa():
    while True:
        message = await topicoa_queue.get()
        logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))


async def lectura_topicob():
    while True:
        message = await topicob_queue.get()
        logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

#crear las colas para los mensajes
topicoa_queue = asyncio.Queue()
topicob_queue = asyncio.Queue()

async def distributor(client):
    # Ordenar los mensajes recibidos en sus respectivas colas
    async for message in client.messages:
        if message.topic.matches(os.environ['TOPICOA']):
            topicoa_queue.put_nowait(message)
        elif message.topic.matches(os.environ['TOPICOB']):
            topicob_queue.put_nowait(message)


"""async def leer_topicos(client):
    async for message in client.messages:
            if message.topic.matches(os.environ['TOPICOA']):
                logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))
            if message.topic.matches(os.environ['TOPICOB']):
                logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))"""

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
            tg.create_task(publicar_contador(client))
            tg.create_task(distributor(client))
            tg.create_task(lectura_topicoa())
            tg.create_task(lectura_topicob())
            tg.create_task(contar())
        
            

if __name__ == "__main__":
    try:
        contador = CONTADOR()
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Saliendo del docker...")
        sys.exit(0)