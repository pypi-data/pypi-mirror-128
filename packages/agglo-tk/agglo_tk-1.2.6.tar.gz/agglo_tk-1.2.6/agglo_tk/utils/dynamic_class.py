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

from importlib import import_module
from ..exceptions import AtkDynamicClassError


__all__ = ["AtkDynamicClass"]

class AtkDynamicClass:
    def __new__(cls_to_instantiate, *args, **kwargs):
        """
            Instantiates a class selected by _select_class method
        """
        result = None

        # Retrieve actual class
        selected_class = cls_to_instantiate.__retrieve_class(*args, **kwargs)

        # We cannot handle another override of __new__
        if selected_class.__new__ is not object.__new__:
            raise AtkDynamicClassError(AtkDynamicClassError.NEW_OVERRIDEN)

        # Override heritage
        factory_grandson = AtkDynamicClass.__update_heritage(cls_to_instantiate, selected_class)

        if not factory_grandson:
            # No need to override heritage
            cls_to_instantiate = selected_class

        # Instantiate selected class
        result = cls_to_instantiate(*args, **kwargs)

        return result


    @classmethod
    def __retrieve_class(cls_to_instantiate, *args, **kwargs):
        # Retrieve actual module and class
        module_name, class_name = cls_to_instantiate._select_class(*args, **kwargs)

        # Import module on class
        try:
            module = import_module(module_name)
            selected_class = getattr(module, class_name)
        except Exception as exception:
            raise ImportError(f"Cannot import class {class_name} from module {module_name}: {exception}")

        return selected_class


    @staticmethod
    def __update_heritage(cls, new_parent):
        factory_idx = -1
        nb_factory_grandson = 0
        direct_heir = 0

        # Look for AtkDynamicClass heir
        for i, parent in enumerate(cls.__bases__):
            # if cls is direct heir of AtkDynamicClass
            if parent is AtkDynamicClass:
                direct_heir = 1

            # if current parent is son of AtkDynamicClass
            elif AtkDynamicClass in parent.__bases__:
                factory_idx = i
                nb_factory_grandson += 1

            else:
                nb_factory_grandson += AtkDynamicClass.__update_heritage(parent, new_parent)

        if (direct_heir + nb_factory_grandson) > 1:
            raise AtkDynamicClassError(AtkDynamicClassError.MULTI_PARENT)
        
        if factory_idx >= 0:
            # AtkDynamicClass's grandson class parent is changed to new_parent, once and 
            # forever (further instantiation won't trigger AtkDynamicClass.__new__ anymore)
            bases = list(cls.__bases__)
            bases[factory_idx] = new_parent
            cls.__bases__ = tuple(bases)

            # Since heritage has change, factory_grandson __new__ method is not AtkDynamicClass.__new__ anymore, but 
            # selected_class.__new__. We must override __new__ to resolve conflicts between __new__ and __init__
            cls.__new__ = lambda cls, *args, **kwargs: object.__new__(cls)

        return nb_factory_grandson


    # TODO in a metaclass
    # def __instancecheck__():
    #     pass
