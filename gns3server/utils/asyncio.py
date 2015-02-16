# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import asyncio
import shutil


@asyncio.coroutine
def wait_run_in_executor(func, *args):
    """
    Run blocking code in a different thread and wait
    for the result.

    :param func: Run this function in a different thread
    :param args: Parameters of the function
    :returns: Return the result of the function
    """

    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, func, *args)
    yield from asyncio.wait([future])
    return future.result()


@asyncio.coroutine
def subprocess_check_output(*args, working_dir=None, env=None):
    """
    Run a command and capture output

    :param *args: List of command arguments
    :param working_dir: Working directory
    :param env: Command environment
    :returns: Command output
    """

    proc = yield from asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, cwd=working_dir, env=env)
    output = yield from proc.stdout.read()
    if output is None:
        return ""
    return output.decode("utf-8")
