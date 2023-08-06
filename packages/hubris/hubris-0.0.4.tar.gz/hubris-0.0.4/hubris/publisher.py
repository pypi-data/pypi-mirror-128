from typing import Dict, Union, List, Callable
from threading import Thread
from collections import deque

from .subscriber import Subscriber


class Publisher:
    """
    Publishers come into being when the publish method is invoked on a
    channel. They manage a background thread which listens on a "subsribe"
    channel for incoming subscribers.

    A new channel is created for each distinct subscriber (one per remote
    thread). When a message is sent over the subscribed-to channel, all
    subscribers are sent a copy over their own distinct channels.
    """

    def __init__(self, channel: 'Channel'):
        self.channel = channel
        self.hub = channel.hub
        self.log = channel.hub.log
        self._subscribe_channel = self.hub[f'{self.channel.name}:subscribe']
        self._thread = None
        self._is_active = False
        self._subscribers = deque()

    @property
    def is_active(self) -> bool:
        """
        Is the "subscribe" channel still open and receiving new
        subscriptions?
        """
        return self._is_active

    def start(self):
        """
        Start the "subscribe" thread, which listesn on a channel for new
        subscribers, adding them to self._subscribers.
        """
        def run():
            self._is_active = True

            while self._is_active:
                data = self._subscribe_channel.receive()
                if data is None:
                    self._is_active = False
                else: 
                    subscriber = Subscriber.from_dict(self.hub, data)
                    self.log.info(
                        f'{subscriber.b36_thread_id} subscribed '
                        f'to {self.channel.name}'
                    )
                    self._subscribers.append(subscriber)

            self.log.info(
                f'{self.channel.name} publisher stopped'
            )

        # already active?
        if self._thread is not None:
            self.log.warning(
                f'{self.channel.name} publisher already active'
            )
            return

        # start the background thread
        self._thread = Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self, timeout=None):
        """
        Stop the "subscribe" thread and notify all subscriber processes that
        their subscriptions have ended (by sending None).
        """
        self._is_active = False

        # send stop signal to the "subscribe" thread
        self._subscribe_channel.send(None)

        # sever all outstanding subscriptions
        for subscriber in self._subscribers:
            if subscriber.channel.is_active:
                subscriber.channel.send(None)

        # join the thread
        if timeout and self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)

    def publish(self, data: Union[Dict, List, Callable]):
        """
        Publish data to all subscribers over their respective channels.
        """

        # if data is callable, it means that we expect it to return the actual
        # payload when called, so we call it here.
        if callable(data):
            data = data()

        # encode the data to send just once rather than in each separate
        # send call below....
        encoded_data = self.hub.encoder.encode(data).encode('utf-8')

        for i in range(len(self._subscribers)):
            subscriber = self._subscribers.popleft()

            # if the subscriber process is still alive, send the data
            if subscriber.is_host_process_active:
                subscriber.channel.send(encoded_data, encode=False)
                self._subscribers.append(subscriber)
            else:
                # the subscription has ended on the subscriber side
                # so remove the fifo file from the filesystem if exists
                subscriber.channel.remove()
                self.log.info(
                    f'{subscriber.b36_thread_id} unsubscribed '
                    f'from {self.channel.name}'
                )