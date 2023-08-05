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

from subprocess import CalledProcessError
from paramiko import SSHClient, RSAKey, AutoAddPolicy
from paramiko.ssh_exception import BadAuthenticationType
from .command_runner import AtkCommandRunner, PRINT_OUTPUT
from .trace import trace


__all__ = ["AtkSSHRunner"]

class AtkSSHRunner(AtkCommandRunner):
    def __init__(self, address, login, pwd=None, ssh_key=None, working_dir=None):
        super().__init__(None)
        self.working_dir = working_dir

        self.address = address
        self.login = login
        self.pwd = pwd
        self.ssh_key = ssh_key
        self._ssh_client = None


    def __del__(self):
            self._close()

    
    def _open(self):
        trace(trace_class="ATK", info=f"SSHRunner::open SSH connection to {self.address}")

        # Connect to ssh
        self._ssh_client = SSHClient()
        self._ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        # Different use case: ssh_key or password
        if self.ssh_key:
            self._ssh_client.connect(self.address, username=self.login, pkey=(RSAKey.from_private_key_file(self.ssh_key)))
        elif self.pwd:
            self._ssh_client.connect(self.address, username=self.login, password=self.pwd)
        else:
            raise BadAuthenticationType("No password neither ssh_key provided")
    

    def _close(self):
        try:
            # Disconnect from ssh
            self._ssh_client.close()
            self._ssh_client = None
        # Case where ssh connection was not opened
        except AttributeError:
            pass


    def _execute(self, command, working_dir, output):
        result = None
        command_result = 0

        # Ensure that we're connected to ssh
        if not self._ssh_client:
            self._open()

        # If working dir is set
        if self.working_dir:
            # cd to working dir
            self.__execute_ssh("cd " + str(self.working_dir))

        # Execute ssh command
        trace(trace_class="ATK", info=f"SSHRunner::execute command {command}")
        result = self.__execute_ssh(command)
    
        if (output == PRINT_OUTPUT):
            print(result)

        return result


    def __execute_ssh(self, command):
        result = None

        # Execute ssh command
        _, stdout, stderr = self._ssh_client.exec_command(command)
        command_result = stderr.channel.recv_exit_status()

        # If an error occured
        if command_result != 0:
            # Raise exception
            stderr = stderr.read().decode("utf-8")
            raise CalledProcessError(command_result, command, stderr)
        else:
            # Retrieve command output
            stdout = stdout.read().decode("utf-8")
            result = stdout

        return result


    def _get_command_log(self, command):
        return self.login + "@" + self.address + ":'" + command + "'"