# This file is part of SmplGen. Copyright (C) 2024 Christian Rauch.
# Distributed under terms of the GPL3 license.


from ast import Module
import math
from jinja2 import Environment, nodes, select_autoescape
import random
from functools import partial

import builtinfuncs as b


class Generator:

    def __init__(self, pattern, entries: int=1): 
        if entries != 1: pattern = \
            f'{{% for i in range({entries}) %}}{pattern}\n{{% endfor %}}'
        self.env = Environment(autoescape=select_autoescape())
        self.template = self._prepare(pattern)

    def _modules(self) -> list:
        return [
            b.Common, 
            b.Interval, 
            b.People, 
            b.TempInfRet, 
            random]

    def _prepare(self, pattern: str) -> nodes.Template:
        for m in self._modules(): 
            self._map_methods(self.env.globals, m)
        return self.env.from_string(pattern)

    def _map_methods(self, mappings: dict, module: Module) -> dict:
        methods = [m for m in dir(module) \
            if callable(getattr(module, m)) and not m.startswith('_')]
        for m in methods:
            mappings[m] = partial(self._invoke, None, module, m)
            mappings[f'i{m}'] = partial(self._invoke, int, module, m)
        return mappings
    
    def _invoke(self, cast, module, method, *args, **kwargs):
        method = getattr(module, method)
        value = method(*args, **kwargs)
        if cast != None: value = cast(value)
        return value
    
    def generate(self, kwargs: dict={}) -> str:
        return self.template.render(kwargs)
