import pandas as pd
from ..HelperRoutines import bold_text

class ParametersObject():
    def __init__(self, name='ParametersObject') -> None:
        self.components = {}
        self._name = name
        self._vessels = []
        self._valves  = []
        self._chambers= []
        self.timings = {}
        
        
    def __repr__(self) -> str:
        out = self._name + ' parameters set: \n'
        for comp in self.components: 
            out += f" * Component - {bold_text(str(comp))}" + '\n'
            for key, item in self.components[comp].items():
                if isinstance(item, float):
                    out += (f"  - {bold_text(str(key)):<20} : {item:.3e}") + '\n'
                else:
                    out += (f"  - {bold_text(str(key)):<20} : {item}") + '\n'
            out += '\n'
        return out
    
    def __getitem__(self, key):
        return self.components[key]
    
    def __setitem__(self, key, val):
        self.components[key] = val
        
    def _set_comp(self, key:str, set, **kwargs):
        if key not in set:
            raise Exception(f'Wrong key! {key} not in {set}.')
        for k, val in kwargs.items():
            if val is None: continue
            assert k in self[key].index.values, f" {key}: {k} not in {self[key].index.values}"
            self[key].loc[k] = val
            
    def set_timings(self, key:str, **kwargs):
        if key not in self._chambers:
            raise Exception(f'Wrong key! {key} not in {self._chambers}.')
        for k, val in kwargs.items():
            if val is None: continue
            assert k in self.timings[key].index.values, f" {key}: {k} not in {self[key].index.values}"
            self[key].loc[k] = val