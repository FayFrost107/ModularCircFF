from ..Time import TimeClass
from ..StateVariable import StateVariable

class ComponentBase():
    def __init__(self,
                 name,
                 time_object:TimeClass,
                 v:float = None,
                 ) -> None:
        self._name     = name
        self._to      = time_object
        
        self._P_i = StateVariable(name=name+'_P_i', timeobj=time_object)
        self._Q_i = StateVariable(name=name+'_Q_i', timeobj=time_object)
        self._P_o = StateVariable(name=name+'_P_o', timeobj=time_object)
        self._Q_o = StateVariable(name=name+'_Q_o', timeobj=time_object)
        self._V   = StateVariable(name=name+'_V' , timeobj=time_object)
        
        if v is not None:
            self.V.loc[0] = v
        return
        
    def __repr__(self) -> str:
        var = (f" Component {self._name}" + '\n' +
               f" - P_i " + str(self._P_i) + '\n' +
               f" - Q_i " + str(self._Q_i) + '\n' +
               f" - P_o " + str(self._P_o) + '\n' +
               f" - Q_o " + str(self._Q_o) + '\n'
               )
        return var
                
    @property
    def P_i(self):
        return self._P_i._u
    
    @property
    def P_o(self):
        return self._P_o._u
    
    @property
    def Q_i(self):
        return self._Q_i._u
    
    @property
    def Q_o(self):
        return self._Q_o._u
    
    @property
    def V(self):
        return self._V._u
    
    @property
    def global_state_variable_names(self):
        return {
            'P_i' : self._P_i.name,
            'P_o' : self._P_o.name,
            'Q_i' : self._Q_i.name,
            'Q_o' : self._Q_o.name
            }
    
    def comp_dvdt(self, intq:int=None, q_i:float=None, q_o:float=None):
        if intq is not None:
            return self.Q_i[intq] - self.Q_o[intq]
        elif q_i is not None and q_o is not None:
            return q_i - q_o
        
    def make_unique_io_state_variable(self, q_flag:bool=False, p_flag:bool=True) -> None:
        if q_flag: 
            self._Q_o = self._Q_i
            self._Q_o.set_name(self._name + '_Q')
        if p_flag: 
            self._P_o = self._P_i
            self._P_o.set_name(self._name + '_P')
        return 
    
    def setup(self) -> None:
        raise Exception("This is a template class only.")
  