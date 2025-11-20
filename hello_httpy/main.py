import logging
from .model.HelloHttpy import HelloHttpy

logger = logging.getLogger("main-loop")
logging.basicConfig(level=logging.INFO)


def main():
    server = HelloHttpy()
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt On Server")
    finally:
        server.stop()


if __name__ == "__main__":
    main()