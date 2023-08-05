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

from .base_types import setter_property


__all__ = ["AtkFrameBuffer"]

class AtkFrameBuffer:
    def __init__(self, bytes_, start=0, first_field_size=1, first_field_type=None, stop=None):
        self.__bytes = bytes_


        self.__sizeof_first_field = first_field_type or first_field_size
        self.__sizeof_next_field = self.__sizeof_first_field

        self.__start = start
        self.__stop = stop or len(self.__bytes)
        self.current = self.__stop


    def __iter__(self):
        self.current = self.__start
        self.__sizeof_next_field = self.__sizeof_first_field

        return self


    def __next__(self):
        result = bytes()
        
        try:
            offset = self.__sizeof_next_field.sizeof()
        # Case where __sizeof_next_field is not a struct type
        except AttributeError:
            offset = self.__sizeof_next_field

        if offset:
            if (self.__stop is not None) and (self.current >= self.__stop):
                raise StopIteration

            result = self.__bytes[self.current:self.current + offset]
            self.current += offset

            try:
                result = self.__sizeof_next_field().from_bytes(result)
            # Case where __sizeof_next_field is not a struct type
            except TypeError:
                pass

        return result


    @setter_property
    def next_field_size(self, value):
        self.__sizeof_next_field = value


    @setter_property
    def next_field_type(self, value):
        self.__sizeof_next_field = value
