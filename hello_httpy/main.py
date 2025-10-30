import logging
from .model.Server import Server

logger = logging.getLogger("main-loop")
logging.basicConfig(level=logging.INFO)



def main():
    server = Server()
    server.listen(5)
    
    server.run()