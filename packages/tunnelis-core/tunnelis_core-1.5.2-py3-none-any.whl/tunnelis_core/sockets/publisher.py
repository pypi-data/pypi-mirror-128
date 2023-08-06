from typing import Tuple
from zmq import PUB as ZMQ_PUB
from zmq.sugar.context import Context


class Publisher:
    """
    A generic message publisher.

    """

    def __init__(self, broker: Tuple[str, int]):
        """
        Initialize a message publisher.

        Parameters
        ----------
        broker : Tuple(str, int)
            The TCP network address (host, port) of the message broker.

        """

        broker_host, broker_port = broker

        self.__zmq_context = Context()

        # Connect publisher to message broker
        self.__socket = self.__zmq_context.socket(ZMQ_PUB)
        self.__socket.connect(f'tcp://{broker_host}:{broker_port}')

    def publish(self, topic: bytes, message: bytes) -> None:
        """
        Publish a message.

        Parameters
        ----------
        topic : bytes
            The topic on which to publish the message.

        payload : bytes
            The message to be published.

        """
        self.__socket.send(topic + b' ' + message)

    def close(self) -> None:
        """
        Stops publisher.

        """
        self.__socket.close()
        self.__zmq_context.term()
