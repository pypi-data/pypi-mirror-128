import os
import errno
import concurrent.futures

from typing import Text, Dict, Union, List, Callable
from threading import Thread, RLock
from concurrent.futures import ThreadPoolExecutor, Future

from appyratus.json import JsonEncoder
from appyratus.logging import ConsoleLoggerInterface as Console

from .channel import Channel    


class Hub:
    """
    A hub is collection of channels. A channel is an abstraction of a POSIX
    named pipe, created with mkfifo. Channels perform IO directly in memory;
    however, the fifo itself exists as a file in the filesystem. The location
    where these generated files reside is the "fifo_dir" directory specified in
    the constructor.

    Usage generally looks like this:

    ```python
    hub = Hub()
    channel = hub['example']   # or hub.channel('example')

    # send something...
    future = channel.send(list_or_dict)

    # block, until we receive something...
    list_or_dict = channel.receive()
    ```

    Implementing a version of pub/sub is also possible like this:

    ```python
    subscription = channel.subscribe(callback)
    subscription.cancel()
    ```

    You can publish something at a regular interval, like:

    ```python
    channel.publish(data_or_func, interval=timedelta(seconds=1))
    channel.publisher.stop()
    ```

    Finally, to close all subscription and publisher threads currently
    active, you can simply call hub.close() at the end of your program.
    """

    def __init__(
        self,
        fifo_dir: Text = '/tmp',
        max_workers: int = None,
        thread_name_prefix: Text = 'Channel',
        encoder=None,
        logger=None,
    ):
        """
        Args:
        - `fifo_dir`: location to store fifo files in the filesystem.
        - `max_workers`: size of send/receive background task thread pool.
        - `thread_name_prefix`: prefix for thread pool workers.
        - `encoder`: example JsonEncoder, with encode and decode methods.
        - `logger`: a Python logger object or a default will be used.
        """
        self.fifo_dir = fifo_dir
        self.channels = {}
        self.encoder = encoder or JsonEncoder()
        self.log = logger or Console('hub', level='DEBUG')
        self.max_workers = max_workers or max(1, os.cpu_count() // 2)
        self.is_active = True
        self.executor = ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix=thread_name_prefix,
        )

    def __repr__(self):
        return f'Hub(channels={list(self.channels)})'

    def __getitem__(self, name: Text):
        """
        Return a Channel object by name. This creates the object automatically
        if it doesn't already exist.
        """
        return self.channel(name)

    def __iter__(self):
        """
        Return an iterator over the names of the Channel objects managed by
        the Hub.
        """
        return self.channels.keys()

    def __len__(self):
        """
        Return the number of Channel objects managed by the Hub.
        """
        return len(self.channels)

    def keys(self):
        """
        dict.keys-like functionality, iterating over the names of existing
        Channel objects managed by the Hub.
        """
        return self.channels.keys()

    def values(self):
        """
        dict.values-like functionality, iterating over the Channel objects
        managed by the Hub.
        """
        return self.channels.values()

    def items(self):
        """
        dict.items-like functionality, iterating over pairs of the names and
        associated Channel objects managed by the Hub.
        """
        return self.channels.items()

    def channel(self, name: Text) -> 'Channel':
        """
        Get or create a Channel object, memoizing it in self.channels.
        """
        channel = self.channels.get(name)
        if channel is None:
            channel = Channel(self, name)
            self.channels[name] = channel
        return channel

    def close(self):
        """
        This should be called when you're finished with the Hub.
        """
        for channel in list(self.channels.values()):
            if channel.publisher is not None:
                channel.publisher.stop()
            if channel.subscription is not None:
                channel.subscription.cancel()

        self.executor.shutdown()
        self.is_active = False