from .ComponentBase import ComponentBase
from ..Time import TimeClass
from ..HelperRoutines import non_ideal_diode_flow 

import pandas as pd

class Valve_non_ideal(ComponentBase):
    def __init__(self, 
                 name:str,
                 time_object: TimeClass,
                 r:float, 
                 max_func
                 ) -> None:
        super().__init__(name=name, time_object=time_object)
        # allow for pressure gradient but not for flow
        self.make_unique_io_state_variable(q_flag=True, p_flag=False) 
        # setting the resistance value
        self.R = r
        self.max_func = max_func
        
    def setup(self) -> None:
        self._Q_i.set_u_func(lambda t, p_in, p_out : non_ideal_diode_flow(p_in=p_in, p_out=p_out, r=self.R, max_func=self.max_func),
                             function_name='lambda non_ideal_diode_flow + max_func')
        self._Q_i.set_inputs(pd.Series({'p_in':self._P_i.name, 
                                        'p_out':self._P_o.name}))
        