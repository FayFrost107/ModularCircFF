from .OdeModel import OdeModel
from .MixedHeartMaynard4eWindkessel_parameters import MixedHeartMaynard4eWindkessel_parameters as MHM4W_parobj
from .ParametersObject import ParametersObject as po
from ..Components import Rlc_component, Valve_maynard,  \
    HC_mixed_elastance, R_component, Valve_non_ideal, \
        HC_constant_elastance, Valve_simple_bernoulli

FULL_NAMES =[
    'LeftA',
    'MiValve',
    'LeftV',
    'AoV',
    'SysArtImp',
    'SysArt',
    'SysCap',
    'SysVen',
    'RightA',
    'TriValve',
    'RightV',
    'PulV',
    'PulArtImp',
    'PulArt',
    'PulCap',
    'PulVen',
]

class MixedHeartMaynard4eWindkessel(OdeModel):
    def __init__(self, time_setup_dict, parobj:po=MHM4W_parobj) -> None:
        super().__init__(time_setup_dict)
        self.name = 'MixedHeartMaynard4eWindkessel'
        
        print(parobj)
        
        # The components...
        for key, name in zip(parobj.components.keys(), FULL_NAMES):
            if key in parobj._vessels: 
                class_ = Rlc_component
            elif key in parobj._imp or key in parobj._cap:
                class_ =  R_component
            elif key in parobj._valves:
                class_ = Valve_simple_bernoulli # Valve_non_ideal # Valve_maynard # Valve_simple_bernoulli
            elif key in parobj._chambers:
                class_ = HC_constant_elastance # HC_mixed_elastance HC_constant_elastance
            else:
                raise Exception(f'Component name {key} not in the model list.')
            self.commponents[key] = class_(name=name,
                                    time_object=self.time_object, 
                                    **parobj[key].to_dict())
            
            if key not in parobj._valves + parobj._cap + parobj._imp: 
                self.set_v_sv(key)
            # else:
            #     self.set_phi_sv(key)
            self.commponents[key].setup()
            
        self.connect_modules(self.commponents['lv'],
                            self.commponents['ao'],
                            plabel='p_lv',
                            qlabel='q_ao',
                            )
        self.connect_modules(self.commponents['ao'],
                            self.commponents['sai'],
                            plabel='p_sa',
                            qlabel='q_ao')
        self.connect_modules(self.commponents['sai'],
                            self.commponents['sa'],
                            plabel='pi_sa',
                            qlabel='q_ao',
                            qvariable=self.commponents['ao']._Q_o)
        self.connect_modules(self.commponents['sa'],
                            self.commponents['sc'],
                            plabel='p_sc',
                            qlabel='q_sa')
        self.connect_modules(self.commponents['sc'],
                            self.commponents['sv'],
                            plabel='p_sv',
                            qlabel='q_sa',
                            qvariable=self.commponents['sa']._Q_o)
        self.connect_modules(self.commponents['sv'],
                            self.commponents['ra'],
                            plabel='p_ra',
                            qlabel='q_sv')
        self.connect_modules(self.commponents['ra'],
                            self.commponents['ti'],
                            plabel='p_ra',
                            qlabel='q_ti')
        self.connect_modules(self.commponents['ti'],
                            self.commponents['rv'],
                            plabel='p_rv',
                            qlabel='q_ti')
        self.connect_modules(self.commponents['rv'],
                            self.commponents['po'],
                            plabel='p_rv',
                            qlabel='q_po')
        self.connect_modules(self.commponents['po'],
                            self.commponents['pai'],
                            plabel='p_pa',
                            qlabel='q_po')
        self.connect_modules(self.commponents['pai'],
                            self.commponents['pa'],
                            plabel='pi_pa',
                            qlabel='q_po',
                            qvariable=self.commponents['po']._Q_o)
        self.connect_modules(self.commponents['pa'],
                            self.commponents['pc'],
                            plabel='p_pc',
                            qlabel='q_pa')
        self.connect_modules(self.commponents['pc'],
                            self.commponents['pv'],
                            plabel='p_pv',
                            qlabel='q_pa',
                            qvariable=self.commponents['pa']._Q_o)
        self.connect_modules(self.commponents['pv'],
                            self.commponents['la'],
                            plabel='p_la',
                            qlabel='q_pv')
        self.connect_modules(self.commponents['la'],
                            self.commponents['mi'],
                            plabel='p_la',
                            qlabel='q_mi')
        self.connect_modules(self.commponents['mi'],
                            self.commponents['lv'],
                            plabel='p_lv',
                            qlabel='q_mi')
        for component in self.commponents.values():
            component.setup()
            
    def set_phi_sv(self, comp_key:str) -> None:
        phi_key = 'phi_' + comp_key
        self._state_variable_dict[phi_key] = self.commponents[comp_key]._PHI
        self._state_variable_dict[phi_key].set_name(phi_key)
        self.all_sv_data[phi_key] = self.commponents[comp_key].PHI