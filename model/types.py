# model/types.py
import uuid
from sqlalchemy import TypeDecorator, BINARY

class BinaryUUID(TypeDecorator):
    """
    Tipo personalizado para optimizar UUID en MySQL (BINARY(16)).
    Maneja la conversión automática entre:
    Python (uuid.UUID) <--> Base de Datos (bytes)
    """
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, bytes):
            return value
        if isinstance(value, str):
            value = uuid.UUID(value)
        return value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(bytes=value)