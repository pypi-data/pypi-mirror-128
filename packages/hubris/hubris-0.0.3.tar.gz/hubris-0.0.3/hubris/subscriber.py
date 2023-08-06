import os
import base36

from threading import get_ident
from typing import Dict, Text

from .util import exists_process


class Subscriber:
    """
    Subscribers are shared between publishers and client-side subscriptions.
    They are used to manage the lifetime of the associated fifo as well as
    for sending data to and from the publishing and subscribed processes.
    """

    def __init__(self, hub, name, thread_id=None, pid=None):
        self.hub = hub
        self.name = name
        self.thread_id = thread_id or get_ident()
        self.pid = pid or os.getpid()

    def to_dict(self):
        """
        Return a dict version of the subscriber, which is used when sending
        through a channel.
        """
        return {
            'name': self.name,
            'thread_id': self.thread_id,
            'pid': self.pid
        }

    @classmethod
    def from_dict(cls, hub: 'Hub', data: Dict) -> 'Subscriber':
        """
        Create and return a Subsciber from a dict, which is used when
        instantiating a subscriber after receiving as dict through a channel.
        """
        return cls(hub, **data)

    @property
    def channel(self) -> 'Channel':
        """
        Get the channel created for this subsciber.
        """
        return self.hub[self.name]

    @property
    def is_host_process_active(self) -> bool:
        """
        Does the Python process which generated this subscriber still exist
        as well as the fifo file?
        """
        return (
            exists_process(self.pid)
            and os.path.exists(self.channel.filepath)
        )

    @property
    def b36_thread_id(self) -> Text:
        """
        Base36-encoded string version of the thread id
        """
        return base36.dumps(self.thread_id)