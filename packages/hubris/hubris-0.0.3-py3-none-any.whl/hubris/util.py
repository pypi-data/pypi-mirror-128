import os

from typing import Text


def exists_process(pid) -> bool:
    """
    Check For the existence of a unix pid.
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True