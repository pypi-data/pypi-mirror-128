import os
import errno

from typing import Text, Dict, Union, List, Callable
from threading import RLock, Timer
from datetime import timedelta
from concurrent.futures import Future

from .subscription import Subscription, Subscriber
from .publisher import Publisher


class Channel:
    """
    A Channel is an abstraction of a POSIX named pipe. It's a two-way channel.
    We don't read and write to it directly. Instead, channels are
    instantiated and managed through Hub objects. Whe you do
    hub.send("bob" data), for example, the hub gets or creates a
    Channel named "bob" and writes `data` to it.
    """

    def __init__(self, hub: 'Hub', name: Text):
        self.hub = hub
        self.log = hub.log
        self.encoder = hub.encoder
        self.name = name
        self.filepath = os.path.join(hub.fifo_dir, name)
        self.read_chunk_size = 2048  # in bytes
        self.read_lock = RLock()
        self.write_lock = RLock()
        self._subscription = None
        self._publisher = None

        self.mkfifo()

    def __repr__(self):
        return f'Channel(name={self.name})'

    @property
    def subscription(self) -> 'Subscription':
        return self._subscription

    @property
    def publisher(self):
        return self._publisher

    def publish(
        self,
        data: Union[Callable, Dict, List],
        interval: timedelta = None
    ):
        """
        Publish something once or at a regular interval.
        """
        if self._publisher is None:
            self._publisher = Publisher(self)
            self._publisher.start()

        if timedelta is None:
            self._publisher.publish(data)
        else:
            def repeat():
                if self._publisher.is_active:
                    self._publisher.publish(data)
                    next_timer = Timer(interval.total_seconds(), repeat)
                    next_timer.start()

            timer = Timer(interval.total_seconds(), repeat)
            timer.start()

    def subscribe(self, callback: Callable, history: int = 1) -> 'Subscription':
        """
        Subscribe the current thread to this channel, invoking the callback
        upon receipt of each data item received.
        """
        if self._subscription is not None:
            self.log.warning(f'canceling existing {self.name} subscription')
            self._subscription.cancel()

        # create subscription and start a background process that receives data
        # and executes the callback
        self._subscription = Subscription(self, callback, history=history)
        self._subscription.start()
        return self._subscription

    def send(self, data: Union[Dict, List], encode=True) -> Future:
        """
        Thread-safe write data to the channel. The input data is encoded using
        the encoder supplied to the calling Hub. For example, the base
        hub by default uses a JsonEncoder.
        """
        def task():
            if encode:
                try:
                    encoded_data = self.encoder.encode(data).encode('utf-8')
                except Exception:
                    self.log.exception(
                        message=f'error encoding fifo data',
                        data={'filepath': self.filepath}
                    )
                    return False
            else:
                encoded_data = data

            if not self.hub.is_active:
                return False

            try:
                fd = os.open(self.filepath, os.O_SYNC|os.O_CREAT|os.O_RDWR)
                with self.write_lock:
                    os.write(fd, encoded_data)
                return True
            except Exception:
                fd = None
                self.log.exception(
                    message=f'error writing fifo',
                    data={'filepath': self.filepath}
                )
                return False
            finally:
                if fd is not None:
                    os.close(fd)

        if not self.hub.is_active:
            return None

        # perform the write in a worker thread
        future = self.hub.executor.submit(task)

        # also send to any subscribers
        if self._publisher is not None:
            self.publish(data)

        return future

    def receive(self, wait=True, timeout=None) -> Union[Dict, List, Future]:
        """
        Read from the Channel, receiving a single dict or list of dicts. This
        operation is blocking.
        """
        def task():
            # read the file in chunks
            chunks = []
            done = False
            fd = None
            try:
                # open file, returning file descriptor int
                fd = os.open(self.filepath, os.O_RDONLY)
                if fd is None:
                    return None

                # keep reading until we reach a final null byte
                with self.read_lock:
                    while not done:
                        chunk = os.read(fd, self.read_chunk_size)
                        if chunk:
                            chunks.append(chunk.decode('utf-8'))
                        else:
                            done = True
            except Exception:
                self.log.exception(
                    message='error reading fifo',
                    data={'filepath': self.filepath}
                )
                return None
            finally:
                if fd is not None:
                    os.close(fd)

            received_text = ''.join(chunks)
            if not received_text or not self.hub.is_active:
                return None

            # decode received data string
            try:
                data = self.encoder.decode(received_text)
                return data
            except Exception:
                self.log.exception(
                    message='error decoding fifo data',
                    data={
                        'filepath': self.filepath,
                        'raw_data': received_text,
                    }
                )

        if not self.hub.is_active:
            return None

        # perform read in worker thread
        future = self.hub.executor.submit(task)

        # return future or wait and return the result
        if wait:
            return future.result(timeout=timeout)
        else:
            return future

    def mkfifo(self):
        """
        Create a new file in the filesystem using mkfifo.
        """
        has_error = False

        try:
            os.mkfifo(self.filepath)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                has_error = True
        except Exception:
            has_error = True

        if has_error:
            self.log.exception(
                f'mkfifo failed',
                data={'filepath': self.filepath}
            )

    def remove(self):
        """
        Try to delete the file created via self.mkfifo from the filesystem.
        """
        if os.path.exists(self.filepath):
            try:
                self.log.debug(f'deleting fifo {self.filepath}')
                os.remove(self.filepath)
            except Exception:
                self.log.exception(
                    message='could not delete fifo',
                    data={'filepath': self.filepath}
                )
