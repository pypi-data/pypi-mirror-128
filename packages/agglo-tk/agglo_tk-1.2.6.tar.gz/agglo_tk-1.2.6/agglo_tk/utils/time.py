############################################################################
##
## Copyright (C) 2025 Plaisic and/or its subsidiary(-ies).
## Contact: eti.laurent@gmail.com
##
## This file is part of the Agglo project.
##
## AGGLO_BEGIN_LICENSE
## Commercial License Usage
## Licensees holding valid commercial Agglo licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Plaisic.  For licensing terms and
## conditions contact eti.laurent@gmail.com.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## In addition, the following conditions apply:
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in
##       the documentation and/or other materials provided with the
##       distribution.
##     * Neither the name of the Agglo project nor the names of its
##       contributors may be used to endorse or promote products derived
##       from this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
## AGGLO_END_LICENSE
##
############################################################################

from time import time
from threading import Thread
from ..exceptions import AtkTimeoutError
from .event import AtkEvent


__all__ = ["AtkTimeoutChecker", "timeout", "call_with_timeout", "AtkTimeIt"]

class AtkTimeoutChecker:
    def __init__(self, timeout_sec, error_to_raise=None, op="action", start=True):
        self.timeout_sec = timeout_sec
        self.__error = error_to_raise or AtkTimeoutError(op=op, timeout_sec=timeout_sec)
        self.reset()
        if start:
            self.__start = time()


    def __enter__(self):
        self.check()

        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.check()


    @property
    def remaining_sec(self):
        result = 0

        if not self.__start:
            self.__start = time()
            result = self.timeout_sec
        else:
            result =  self.timeout_sec - (time() - self.__start)

        if result <= 0:
            raise self.__error

        return result


    def reset(self):
        self.__start = None


    def check(self):
        self.remaining_sec


def timeout(timeout_sec):
    def decorator(func):
        def decorated(*args, **kwargs):
            return call_with_timeout(func, timeout_sec, *args, **kwargs)

        return decorated

    return decorator


def call_with_timeout(method, timeout_sec, *args, **kwargs):
    method_done_event = AtkEvent()
    def run_method_async(method, method_done_event, *args, **kwargs):
        try:
            result = method(*args, **kwargs)
            method_done_event.set(result)

        except Exception as error:
            method_done_event.fail(error)
    method_thread = Thread(target=run_method_async, args=(method, method_done_event, *args), kwargs=kwargs)

    # Run method asynchronously and wait for completion
    method_thread.start()
    method_done_event.wait(timeout_sec)

    if method_done_event.timedout:
        raise AtkTimeoutError(op=method.__name__, timeout_sec=timeout_sec)

    elif method_done_event.failed:
        raise method_done_event.error

    return method_done_event.result



class AtkTimeIt:
    def __init__(self, name=None):
        self.call_count = 0
        self.call_average = 0
        self.elapsed_sec = 0
        self.__name = name
        self.__func = None
        self.__start = None


    @property
    def name(self):
        result = self.__name

        if not result and self.__func:
            result = self.__func.__name__

        return result
    

    def __call__(self, func):
        self.__func = func

        def decorated(*args, **kwds):
            with self:
                return func(*args, **kwds)

        return decorated


    def __enter__(self):
        self.call_count += 1
        self.__start = time()

        return self


    def __exit__(self, exc_type, exc_value, traceback):
        call_result = " failed" if exc_value else ""
        call_delay = time() - self.__start
        elapsed = f"time elapsed {round(call_delay, 6)} sec"

        if self.__func:
            count = f" {self.call_count}" if self.call_count else ""
            self.call_average = (((self.call_average) * (self.call_count - 1)) + call_delay) / self.call_count
            print(f"{self.name} call{count}{call_result} : {elapsed}, average {round(self.call_average, 6)} sec", flush=True)
        else:
            name = self.name or "TimeIt"
            print(f"{name}{call_result} : {elapsed}", flush=True)
        
        self.elapsed_sec = call_delay
