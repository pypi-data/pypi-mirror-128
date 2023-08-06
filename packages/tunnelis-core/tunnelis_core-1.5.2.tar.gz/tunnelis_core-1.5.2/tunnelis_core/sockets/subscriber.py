from typing import Callable, Dict, Tuple
from zmq import SUB as ZMQ_SUB, SUBSCRIBE as ZMQ_SUBSCRIBE
from zmq.eventloop import zmqstream
from zmq.sugar.context import Context

SubscriberCallback = Callable[[bytes], None]


class Subscriber:
    """
    A generic message subscriber.

    """

    __subscriptions: Dict[bytes, SubscriberCallback] = {}

    def __init__(self, broker: Tuple[str, int]):
        """
        Initialize a message subscriber.

        Parameters
        ----------
        broker : Tuple(str, int)
            The TCP network address (host, port) of the message broker.

        """

        broker_host, broker_port = broker

        self.__zmq_context = Context()

        # Connect subscriber to message broker
        self.__socket = self.__zmq_context.socket(ZMQ_SUB)
        self.__socket.connect(f'tcp://{broker_host}:{broker_port}')

        # Create stream to handle received messages asynchronously
        self.__stream = zmqstream.ZMQStream(self.__socket)
        self.__stream.on_recv(self.__message_handler)

    def subscribe(self, topic: bytes, handler: SubscriberCallback) -> None:
        """
        Registers a callback function and starts listening for messages published on a given topic.
        Only one handler function is allowed per topic.

        Parameters
        ----------
        topic : bytes
            The message topic.

        handler : Callable(bytes) -> None
            The callback function to call.

        """
        if topic not in self.__subscriptions:
            self.__socket.setsockopt(ZMQ_SUBSCRIBE, topic)
        self.__subscriptions[topic] = handler

    def unsubscribe(self, topic: bytes) -> None:
        """
        Stops listening for messages published on a given topic and removes registered callback function.

        Parameters
        ----------
        topic : bytes

        """
        if topic in self.__subscriptions:
            del self.__subscriptions[topic]

    def close(self) -> None:
        """
        Stops subscriber.

        """
        self.__stream.close()
        self.__zmq_context.term()

    def __message_handler(self, message: Tuple[bytes, bytes]) -> None:
        """
        A generic message handler.
        Forwards received messages to their proper message handlers.

        Parameters
        ----------
        message : Tuple(bytes, bytes)
            The received message.

        """

        topic, payload = message.split()

        if topic in self.__subscriptions:
            handler = self.__subscriptions[topic]
            handler(payload)
