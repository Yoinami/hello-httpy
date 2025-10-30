import logging
from .model.Server import Server

logger = logging.getLogger("main-loop")
logging.basicConfig(level=logging.INFO)



def main():
    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt On Server")
    finally:
        server.stop()