from dataclasses import dataclass, field
from datetime import date

@dataclass
class SerieDiariaIntegridadInfo:
    cod_symbol: str = field(default="")
    flg_split: bool = field(default=False)
    flg_split_correcto: bool = field(default=None)
    flg_num_dias_sep_correcto: bool = field(default=None)
    flg_correcto: bool = field(default=False)    
    
    def __post_init__(self):
        evals = []
        if self.flg_split:
            evals.append(self.split_correcto)            
        
        # evals.append(self.num_dias_separacion_correcto)

        self.flg_correcto = all(evals)
        
    

@dataclass
class SerieSemanalIntegridadInfo:
    min_cod_semana_correcto: bool = None
    max_cod_semana_correcto: bool = None
    cantidad_correcto: bool = None
    correcto: bool = field(default=False, init=False)
    reprocesar: bool = field(default=False, init=False)       
    reprocesar_todo: bool = field(default=False, init=False)

    def __post_init__(self):        
        self.correcto = (False in [self.max_cod_semana_correcto, self.min_cod_semana_correcto, self.cantidad_correcto])
        if not self.correcto:
            self.reprocesar = True
            self.reprocesar_todo = True

@dataclass
class VariacionSemanalIntegridadInfo:
    min_cod_semana_correcto: bool = None
    max_cod_semana_correcto: bool = None
    cantidad_correcto: bool = None
    correcto: bool = field(default=False, init=False)
    reprocesar: bool = field(default=False, init=False)
    reprocesar_todo: bool = field(default=False, init=False)

    def __post_init__(self):
        self.correcto = (False in [self.max_cod_semana_correcto, self.min_cod_semana_correcto, self.cantidad_correcto])
        if not self.correcto:
            self.reprocesar = True
            self.reprocesar_todo = True