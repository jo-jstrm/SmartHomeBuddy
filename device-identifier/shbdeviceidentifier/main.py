import zerorpc
import logging

from rpc import DeviceIdentifierApi

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_port():
    return 4242


def main():
    logging.info('Started Python device-identifier.')
    addr = f'tcp://127.0.0.1:{parse_port()}'
    server = zerorpc.Server(DeviceIdentifierApi())
    server.bind(addr)
    logging.info(f'Started running on {addr}')
    server.run()


if __name__ == '__main__':
    main()