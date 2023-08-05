import datetime
import logging
import os
import tempfile
import time
from typing import Optional

import pexpect
from pytest_embedded.log import DuplicateStdout, DuplicateStdoutPopen
from pytest_embedded.utils import to_str

from . import DEFAULT_IMAGE_FN


class Qemu(DuplicateStdoutPopen):
    """
    QEMU class
    """

    QEMU_PROG_PATH = 'qemu-system-xtensa'
    QEMU_DEFAULT_ARGS = '-nographic -no-reboot -machine esp32'

    QEMU_STRAP_MODE_FMT = '-global driver=esp32.gpio,property=strap_mode,value={}'
    QEMU_SERIAL_TCP_FMT = '-serial tcp::{},server,nowait'

    def __init__(
        self,
        qemu_image_path: Optional[str] = None,
        qemu_prog_path: Optional[str] = None,
        qemu_cli_args: Optional[str] = None,
        qemu_extra_args: Optional[str] = None,
        qemu_log_path: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            qemu_image_path: QEMU image path
            qemu_prog_path: QEMU program path
            qemu_cli_args: QEMU CLI arguments
            qemu_extra_args: QEMU CLI extra arguments, will append to `qemu_cli_args`
            qemu_log_path: QEMU log file path, would direct to `pexpect_proc` automatically
        """
        image_path = qemu_image_path or DEFAULT_IMAGE_FN
        if not os.path.exists(image_path):
            raise ValueError(f'QEMU image path not exists: {image_path}')

        qemu_prog_path = qemu_prog_path or self.QEMU_PROG_PATH
        qemu_cli_args = qemu_cli_args or self.QEMU_DEFAULT_ARGS

        qemu_extra_args = qemu_extra_args.replace('"', '') if qemu_extra_args else qemu_extra_args
        qemu_extra_args = [qemu_extra_args] if qemu_extra_args else []
        qemu_extra_args.append(f'-drive file={image_path},if=mtd,format=raw')

        # we use log file to record serial output
        self.log_file = qemu_log_path or os.path.join(
            tempfile.tempdir, datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S'), 'serial.log'
        )

        parent_dir = os.path.dirname(self.log_file)
        if parent_dir:  # in case value is a single file under the current dir
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        qemu_extra_args.append(f'-serial file:{self.log_file}')

        self.qemu_inst = None

        cmd = f'{qemu_prog_path} {qemu_cli_args} {" ".join(qemu_extra_args)}'
        logging.debug(cmd)

        super().__init__(cmd, **kwargs)

    def _forward_io(self, pexpect_proc: Optional[pexpect.spawn] = None, source: Optional[str] = None) -> None:
        time.sleep(1)  # ensure the log file is generated by qemu
        with DuplicateStdout(pexpect_proc, source):
            for line in open(self.log_file):
                print(to_str(line))
