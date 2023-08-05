# @file 
# @brief 
# @copyright Copyright PA.COTTE 2016

from .module_loader import AtkModuleLoader


__all__ = ["AtkConfig", "AtkConfigModule"]

class AtkConfig:
    def __init__(self, path=None, **kwargs):
        self.config_file = AtkConfigModule(path) if path else None
        self._default_values = kwargs


    def __getattr__(self, attr_name):
        result = None

        if self.config_file and (attr_name in self.config_file):
            result = self.config_file.params[attr_name]
        elif attr_name in self._default_values:
            result = self._default_values[attr_name]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object '{attr_name}' attribute is not set")

        return result


    def __str__(self):
        params = "\n". join(f"  {name}: {getattr(self, name)}" for name in self._default_values)

        return f"{self.__class__.__name__}:\n{params}"


class AtkConfigModule:
    def __init__(self, path):
        self.path = path
        self._module = None
        self.load()


    def __contains__(self, item):
        return item in self.params
        

    def __getattr__(self, attr_name):
        result = None

        try:
            if attr_name == "params":
                module = object.__getattribute__(self, "_module")
                params_names = dir(module)
                params = vars(module)

                # Remove builtins from module variables
                params_names = [param_name for param_name in params_names 
                                        if not (param_name.startswith("__") and param_name.endswith("__"))]
                result = {param_name:params[param_name] for param_name in params_names}
            else:
              result = self.params[attr_name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object '{attr_name}' attribute is not set")

        return result


    def __str__(self):
        params = "\n". join(f"  {name}: {value}" for name, value in self.params.items())

        return f"{self.__class__.__name__}:\n{params}"


    def load(self):
        self._module = AtkModuleLoader(self.path).load()

        return self.params
