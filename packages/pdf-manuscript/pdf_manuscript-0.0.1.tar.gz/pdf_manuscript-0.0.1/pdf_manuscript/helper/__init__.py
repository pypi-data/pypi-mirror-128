import logging
import subprocess

from typing import List

log = logging.getLogger(__name__)


def syscall(
        args: List[str],
        stdout_handler: int = subprocess.PIPE,
        stderr_handler: int = subprocess.PIPE,
        text: bool = True,
        ignore_stderr: bool = False) -> str:
    log.info(f"syscall {' '.join(args)}")
    proc = subprocess.Popen(
        args,
        stdout=stdout_handler,
        stderr=stderr_handler,
        text=text
    )
    stdout, stderr = proc.communicate()
    log.info(f"syscall output {stdout}")
    log.info(f"syscall stderr {stderr}")
    # TODO - ignoring for the moment (empty sterr that is raising exception)
    # if stderr and not ignore_stderr:
    #    print(stderr)
    #    raise Exception(stderr)
    if proc.returncode:
        raise Exception("Invalid return code")
    return stdout
