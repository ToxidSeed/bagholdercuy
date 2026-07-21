from reader.seriediaria import SerieDiariaReader
from sqlalchemy.exc import ProgrammingError
from config.extensions import db
import pytest

class SessionExcepcionMock:    
    def execute(self, stmt):
        raise ProgrammingError("select",{}, BaseException("No existe la tabla xxxx"))

class TestSerieDiariaReader:    
    def test_get_min_fch_serie_x_num_dias_separacion(self, monkeypatch):   
        def mock_execute(*args, **kwargs):
            return SessionExcepcionMock()

        with pytest.raises(ProgrammingError) as execinfo:
            monkeypatch.setattr(db, "session", mock_execute())
            result = SerieDiariaReader.get_min_fch_serie_x_num_dias_separacion(cod_symbol="LABU", num_dias_separacion=4)

            
    