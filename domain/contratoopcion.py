from common.AppException import AppException
from datetime import date, datetime

class ContratoOpcionHumanReadable:
    """
    Parsea el formato human-readable de IBKR para contratos de opción.
    Ejemplo: "SMCI 07FEB25 38 C"
              <symbol> <ddMMMYY> <strike> <tipo>
    """

    _MESES = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,  'MAY': 5,  'JUN': 6,
        'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }

    def __init__(self, value: str):
        self.__raw = value
        self.__cod_symbol = None
        self.__fch_expiracion = None
        self.__imp_ejercicio = None
        self.__cod_tipo_opcion = None
        self._parse(value)

    # ------------------------------------------------------------------ #
    # Parsing                                                              #
    # ------------------------------------------------------------------ #

    def _parse(self, value: str):
        if not value or not value.strip():
            raise AppException(msg="El símbolo del contrato de opción no puede estar vacío")

        partes = value.strip().split()
        if len(partes) != 4:
            raise AppException(
                msg=f"Formato inválido: '{value}'. Se esperaba: 'SMCI 07FEB25 38 C'"
            )

        self.__cod_symbol      = self._extraer_symbol(partes[0])
        self.__fch_expiracion  = self._extraer_fecha(partes[1])
        self.__imp_ejercicio   = self._extraer_strike(partes[2])
        self.__cod_tipo_opcion = self._extraer_tipo(partes[3])

    def _extraer_symbol(self, parte: str) -> str:
        return parte.strip().upper()

    def _extraer_fecha(self, parte: str) -> date:
        """Parsea ddMMMYY, ej: '07FEB25' -> date(2025, 2, 7)"""
        parte = parte.strip().upper()
        if len(parte) != 7:
            raise AppException(msg=f"Formato de fecha inválido: '{parte}'. Se esperaba ddMMMYY")
        dia     = int(parte[:2])
        mes_str = parte[2:5]
        anyo    = 2000 + int(parte[5:])
        mes     = self._MESES.get(mes_str)
        if mes is None:
            raise AppException(msg=f"Mes desconocido: '{mes_str}'")
        return date(anyo, mes, dia)

    def _extraer_strike(self, parte: str) -> float:
        try:
            return float(parte.strip())
        except ValueError:
            raise AppException(msg=f"Strike inválido: '{parte}'")

    def _extraer_tipo(self, parte: str) -> str:
        tipo = parte.strip().upper()
        if tipo not in ('C', 'P'):
            raise AppException(msg=f"Tipo de opción inválido: '{parte}'. Se esperaba 'C' o 'P'")
        return tipo

    # ------------------------------------------------------------------ #
    # Propiedades                                                          #
    # ------------------------------------------------------------------ #

    @property
    def cod_symbol(self) -> str:
        """Símbolo del subyacente, ej: 'SMCI'"""
        return self.__cod_symbol

    @property
    def fch_expiracion(self) -> date:
        """Fecha de expiración como objeto date"""
        return self.__fch_expiracion

    @property
    def imp_ejercicio(self) -> float:
        """Precio de strike"""
        return self.__imp_ejercicio

    @property
    def cod_tipo_opcion(self) -> str:
        """Tipo de opción: 'C' (Call) o 'P' (Put)"""
        return self.__cod_tipo_opcion

    # ------------------------------------------------------------------ #
    # Generación de código OCC                                            #
    # ------------------------------------------------------------------ #

    def get_codigo_occ(self) -> str:
        """
        Genera el código OCC estándar.
        Formato: <SYMBOL padded 6><YYMMDD><C|P><strike * 1000 padded 8>
        Ejemplo: 'SMCI 07FEB25 38 C' -> 'SMCI  250207C00038000'
        """
        symbol_pad = self.__cod_symbol.ljust(6)
        fecha_str  = self.__fch_expiracion.strftime('%y%m%d')
        strike_int = int(round(self.__imp_ejercicio * 1000))
        strike_str = str(strike_int).zfill(8)
        return f"{symbol_pad}{fecha_str}{self.__cod_tipo_opcion}{strike_str}"

    def get_codigo_occ_extendido(self) -> str:
        """
        Genera el còdigo OCC Extendido
        Formato: <SYMBOL><YYYYMMDD><C|P><strike * 1000 padded 8>
        Ejemplo: SOXL20220422C00030000
        """
        fecha_str  = self.__fch_expiracion.strftime('%Y%m%d')
        strike_int = int(round(self.__imp_ejercicio * 1000))
        strike_str = str(strike_int).zfill(8)
        return f"{self.__cod_symbol}{fecha_str}{self.__cod_tipo_opcion}{strike_str}"

    def __repr__(self):
        return f"<ContratoOpcionHumanReadable {self.__raw!r} -> OCC: {self.get_codigo_occ()}>"

class ContratoOpcion:
    def __init__(self, value):
        self.__imp_ejercicio = None
        self.__cod_tipo_opcion = None
        self.__fch_expiracion = None
        self.__cod_symbol_subyacente = None
        self.__value = self.parse(value)        

    def parse(self, valor):
        if valor in [None,""]:
            return None
        
        self.__imp_ejercicio = self.__extraer_ejercicio(valor=valor)
        self.__cod_tipo_opcion = self.__extraer_cod_tipo_opcion(valor=valor)
        self.__fch_expiracion  = self.__extraer_fch_expiracion(valor=valor)
        self.__cod_symbol_subyacente = self.__extraer_cod_symbol_subyacente(valor=valor)

        return valor
            
    def __extraer_ejercicio(self, valor):
        str_ejercicio = valor[-8:]
        return float(int(str_ejercicio))/1000
    
    def __extraer_cod_tipo_opcion(self, valor):
        cod_tipo_opcion = valor[-9:-8]
        if cod_tipo_opcion not in ["P","C"]:
            raise AppException(msg=f"No se encuentra el tipo de opcion en el codigo {valor}, valor encontrado {cod_tipo_opcion}")
        
        return cod_tipo_opcion

    def __extraer_fch_expiracion(self, valor):
        return datetime.strptime(valor[-17:-9],"%Y%m%d").date()
    
    def __extraer_cod_symbol_subyacente(self, valor):
        return valor[:-17]
                
    @property
    def imp_ejercicio(self):
        return self.__imp_ejercicio
    
    @property
    def cod_tipo_opcion(self):
        return self.__cod_tipo_opcion
    
    @property
    def fch_expiracion(self):
        return self.__fch_expiracion
    
    @property
    def cod_symbol_subyacente(self):
        return self.__cod_symbol_subyacente
    
    @property
    def value(self):
        return self.__value