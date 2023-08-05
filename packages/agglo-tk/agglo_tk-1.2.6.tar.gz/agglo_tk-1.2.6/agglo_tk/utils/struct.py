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

from collections import OrderedDict, namedtuple
import ctypes


__all__ = ["AtkCtypesMixin", "AtkCtypesSingleFieldMixin", "AtkCtypesPropertiesGenerator"]

class AtkCtypesMixin:
    def __repr__(self):
        fields = ", ".join(f"{field_name}={value}" for field_name, value in self.fields._asdict().items())

        return f"{self.__class__.__name__}({fields})"


    def __iter__(self):
        return iter(self.fields._asdict().items())


    def __eq__(self, other):
        result = (type(self) == type(other))

        result = result and (len(self.fields) == len(other.fields))
        for field_name, value in self:
            try:
                result = result and (getattr(other, field_name) == value)
            # Case where current field is not present in other
            except AttributeError:
                result = False

            if not result:
                break

        return result


    @property
    def fields(self):
        fields = OrderedDict((field_name, getattr(self, field_name)) for field_name, *_ in self._fields_)

        return namedtuple(f"{self.__class__.__name__}_fields", fields.keys())(**fields) 


    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(cls)


    def to_bytes(self):
        return bytes(self)


    def from_bytes(self, bytes_):
        ctypes.memmove(ctypes.pointer(self), bytes_, self.sizeof())

        return self


class AtkCtypesSingleFieldMixin(AtkCtypesMixin):
    _pack_ = 1

    def __init__(self, converter):
        self._converter = converter


    @property
    def value(self):
        return self._converter(self.fields[0])
    

    def from_bytes(self, bytes_):
        super().from_bytes(bytes_)

        return self.value


class AtkCtypesPropertiesGenerator(type(ctypes.Structure)):
    def __new__(cls, name, bases, dct):
        properties = dct.pop("_PROPERTIES")

        # Add properties from _PROPERTIES in cls attributes
        dct.update(properties)

        return super().__new__(cls, name, bases, dct)


    @staticmethod
    def struct_property(field_name, convert_get=None, convert_set=None):
        fget = lambda self: convert_get(getattr(self, field_name)) if convert_get else None
        fset = lambda self, value: setattr(self, field_name, convert_set(value)) if convert_set else None

        return property(fget, fset)
