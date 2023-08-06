import abc
import functools
from typing import Dict, Optional

from classiq_interface.generator import function_param_list, function_params

from classiq import wire


class FunctionHandler(abc.ABC):
    @abc.abstractmethod
    def _function_call_handler(
        self,
        function: str,
        params: function_params.FunctionParams,
        in_wires: Optional[Dict[str, wire.Wire]] = None,
    ):
        pass

    def __getattribute__(self, item):
        is_item_function_name = any(
            item == func.__name__
            for func in function_param_list.get_function_param_list()
        )

        if is_item_function_name:
            return functools.partial(self._function_call_handler, function=item)

        return super().__getattribute__(item)

    def __dir__(self):
        return list(super().__dir__()) + [
            func.__name__ for func in function_param_list.get_function_param_list()
        ]
