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

from subprocess import Popen, check_output, STDOUT, CalledProcessError
from threading import Thread
from pathlib import Path
from .trace import trace


__all__ = ["AtkCommandRunner", "SILENT", "PRINT_CMD", "PRINT_OUTPUT"]

SILENT = 0
PRINT_CMD = 1
PRINT_OUTPUT = 2

class AtkCommandRunner:
    def __init__(self, working_dir=None, cygwin=False):
        self.working_dir = working_dir or "."
        self.print_wd = False
        self.__use_shell = False
        self.__cygwin = cygwin
        try:
            self.working_dir = Path(working_dir).resolve().as_posix()
        except:
            pass


    def execute(self, command, output=PRINT_CMD, relative_wd="", strict=True, use_shell=False):
        result = ""
        execution = ""
        working_dir = self.working_dir
        self.__use_shell = use_shell

        # Append relative path
        if (relative_wd != ""):
            working_dir += "/" + relative_wd

        try:
            if (output >= PRINT_CMD):
                if self.print_wd:
                    execution = "from " + working_dir + ", "
                execution += "execute " + self._get_command_log(command) + "..."
                print(execution, end="")
            
            result = self._execute(command, working_dir, output)
            if (output >= PRINT_CMD):
                if (result != "") and ((output == PRINT_OUTPUT)):
                    print(execution, end="")
                print(" DONE")

        except Exception as exception:
            if isinstance(exception, CalledProcessError):
                result = exception.output
                if (output >= PRINT_CMD):
                    print(result)
            if (output >= PRINT_CMD):
                if (result != "") and ((output == PRINT_OUTPUT)):
                    print(execution, end="")
                print(" FAILED")
            if strict:
                raise
        finally:
            self.__use_shell = False

        return result


    def _execute(self, command, working_dir, output):
        result = ""
        has_wildcard = "*" in command
        use_shell = has_wildcard or self.__use_shell
        args = command if use_shell else command.split()

        trace(trace_class="ATK", info=f"CommandRunner::execute command {command}")

        if (output == PRINT_OUTPUT):                
            # Create temp file for stdout
            runner_log_thread = _RunnerLogThread()
            stdout_file_path = "runner_{id}.log".format(id=id(runner_log_thread))
            Path(stdout_file_path).touch()

            # Open log file with read/write access
            try:
                with open(stdout_file_path, "r+") as stdout_file:
                    try:
                        # Start a thread which will print command output
                        runner_log_thread.start()

                        # Run command in process, with output in a temp stdout file
                        kwargs = {"args":args, "cwd":working_dir, "universal_newlines":True, "stderr":STDOUT, "shell":use_shell, "stdout":stdout_file}
                        if self.__cygwin and use_shell:
                            # Add cugwin bash.exe executable to argument list
                            kwargs["args"] = "c:/cygwin64/bin/bash.exe -c '" + kwargs["args"] + "'"
                        process = Popen(**kwargs)

                        # Block until command is done
                        process.wait()
                    finally:
                        # Stop print stdout thread
                        runner_log_thread.continue_run = False
                        runner_log_thread.join(timeout=5)
            finally:
                # We need to reopen stdout file to read result
                with open(stdout_file_path, "r") as stdout_file:
                    result = stdout_file.read()
                
                # Remove log file
                Path(stdout_file_path).unlink()

            # If process has failed
            if process.returncode != 0:
                # Raise an error
                _, stderr = process.communicate()
                if stderr is None:
                    stderr = ""
                raise CalledProcessError(process.returncode, command, stderr)

        else:
            result = check_output(args=args, cwd=working_dir, universal_newlines=True, stderr=STDOUT, shell=use_shell)

        return result


    def _get_command_log(self, command):
        return "'" + command + "'"


class _RunnerLogThread(Thread):
    def __init__(self):
        super().__init__()
        self.continue_run = True


    def run(self):
        stdout_file_path = "runner_{id}.log".format(id=id(self))

        # Open temp stdout file with read access
        with open(stdout_file_path, "r") as stdout_file:
            # Print stdout file
            first_line = True
            while self.continue_run:
                for line in stdout_file.readlines():
                    if first_line:
                        print()
                        first_line = False
                    print(line, end="", flush=True)
