from unittest import mock, TestCase
from processor.operacion import RegistroMultipleOperacionesManager, AlteracionPosicion
from reader.operacion import OperacionReader
from model.operacion import OperacionModel
from model.posicion import PosicionModel
from datetime import date
from common.AppException import AppException
import copy

class Datos:
    def __init__(self):
        self.posicion = PosicionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,            
            cantidad=50
        )

        self.operacion_1 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=50
        )

        #operacion procesada
        self.operacion_2 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=35
        )

        self.operacion_3 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=65
        )        


class RegistroMultipleOperacionesManagerTest(TestCase):

    @mock.patch("reader.operacion.OperacionReader.get_ultima_operacion_hasta_fecha")
    def test_get_operacion_anterior(self, mock_get_ultima_operacion_hasta_fecha):

        mock_get_ultima_operacion_hasta_fecha.return_value = None

        """
        Caso 1:
         1. No hay ninguna posicion creada
         2. una posicion en proceso
        """

        rmopm = RegistroMultipleOperacionesManager()
        alteracion = AlteracionPosicion()
        operacion = OperacionModel()
        operacion_anterior = rmopm.get_operacion_anterior(alteracion_posicion=alteracion, operacion=operacion)
        self.assertEqual(operacion_anterior, None)

        """
        caso 2:
         1. No hay ninguna posicion creada
         2. 1 operacion procesada
         3. 1 operacion en curso
        """
        rmopm = RegistroMultipleOperacionesManager()        
        alteracion = AlteracionPosicion(posicion=None)        
        operacion_1 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=50
        )

        alteracion.incluir_operacion(operacion=operacion_1)

        mock_get_ultima_operacion_hasta_fecha.return_value = None

        operacion_2 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=10
        )
        operacion_anterior = rmopm.get_operacion_anterior(alteracion_posicion=alteracion, operacion=operacion_2)
        self.assertEqual(operacion_anterior.cantidad,50)

        """
        caso 3:
         1. Existe una posicion
         2. ya existe una posicion que ha generado la posicion
         3. 1 posicion se ha terminado de procesar
         4. 1 posicion esta en proceso
        """
        rmopm = RegistroMultipleOperacionesManager()        
        posicion = PosicionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,            
            cantidad=50
        )

        alteracion = AlteracionPosicion(posicion=posicion)        
        
        #operacion que ha generado previamente la posicion
        operacion_1 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=50
        )

        #operacion procesada
        operacion_2 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=35
        )

        alteracion.incluir_operacion(operacion=operacion_2)

        #operacion en proceso
        operacion_3 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=65
        )

        #la operacion_1 es la que se hizo previamente para generar la posicion
        mock_get_ultima_operacion_hasta_fecha.return_value = operacion_1
        operacion_anterior = rmopm.get_operacion_anterior(alteracion_posicion=alteracion, operacion=operacion_3)
        self.assertEqual(operacion_anterior.cantidad,35)

    @mock.patch("reader.operacion.OperacionReader.get")
    def test_establecer_reproceso(self, mock_operacion_reader_get):
        """
        caso 1:
        1. Si la posicion no existe
        """
        alteracion = AlteracionPosicion()        
        operacion_1 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=65
        )

        registro_multiple_oper_manager = RegistroMultipleOperacionesManager()
        registro_multiple_oper_manager.establecer_reproceso(alteracion=alteracion, operacion=operacion_1)
        self.assertFalse(alteracion.flg_reproceso)

        """
        caso 2:
        1. Si la posicion existe y ya esta marcada como reproceso
        """
        posicion = PosicionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,            
            cantidad=50
        )

        alteracion = AlteracionPosicion(posicion=posicion) 
        alteracion.flg_reproceso = True

        operacion_1 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=50
        )

        #operacion procesada
        operacion_2 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=35
        )        

        #operacion en proceso
        operacion_3 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=65
        )

        registro_multiple_oper_manager = RegistroMultipleOperacionesManager()
        registro_multiple_oper_manager.establecer_reproceso(alteracion=alteracion, operacion=operacion_1)
        self.assertTrue(alteracion.flg_reproceso)

        """
        caso 3:
        1. La posicion existe
        2. No esta marcada como reproceso
        3. No existe la operacion indicada en el campo id_ultima_operacion
        """
        posicion = PosicionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,            
            cantidad=50,
            id_ultima_operacion=500
        )

        alteracion = AlteracionPosicion(posicion=posicion) 
        alteracion.flg_reproceso = False

        operacion_1 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=50
        )

        #operacion procesada
        operacion_2 = OperacionModel(
            id_cuenta=1,
            id_symbol=1,
            id_contrato_opcion=None,
            fch_operacion=date.fromisoformat("2022-11-05"),
            cantidad=35
        )        

        mock_operacion_reader_get.return_value = None
        registro_multiple_oper_manager = RegistroMultipleOperacionesManager()        
        with self.assertRaises(AppException):
            registro_multiple_oper_manager.establecer_reproceso(alteracion=alteracion, operacion=operacion_2)
            
        """
        caso 4:
        1.- La posicion existe
        2.- La posicion no esta marcada como reproceso
        3.- La operacion indicada en la posicion existe en almacenamiento existe en almacenamiento
        4.- la fecha de la operacion de almacenamiento es igual a la fcha de operacion que se esta procesando
        """
        datos = Datos()

        posicion = copy.copy(datos.posicion)
        alteracion = AlteracionPosicion(posicion=posicion, flg_reproceso=False)
        operacion_previa_posicion = copy.copy(datos.operacion_1)
        operacion_en_curso = copy.copy(datos.operacion_2)
        mock_operacion_reader_get.return_value = operacion_previa_posicion
        registro_multiple_oper_manager.establecer_reproceso(alteracion=alteracion, operacion=operacion_en_curso)
        self.assertFalse(alteracion.flg_reproceso)

        """
        caso 5:
        1.- La posicion existe
        2.- La posicion no esta marcada como reproceso
        3.- La operacion indicada en la posicion existe en almacenamiento existe en almacenamiento
        4.- la fecha de la operacion de almacenamiento es menor a la fcha de operacion que se esta procesando
        """
        alteracion = AlteracionPosicion(posicion=posicion, flg_reproceso=False)
        operacion_previa_posicion = copy.copy(datos.operacion_1)
        operacion_previa_posicion.fch_operacion = date.fromisoformat("2023-11-04")
        operacion_en_curso = copy.copy(datos.operacion_2)
        operacion_en_curso.fch_operacion = date.fromisoformat("2023-11-05")
        mock_operacion_reader_get.return_value = operacion_previa_posicion
        registro_multiple_oper_manager.establecer_reproceso(alteracion=alteracion, operacion=operacion_en_curso)
        self.assertFalse(alteracion.flg_reproceso)

        """
        caso 5:
        1.- La posicion existe
        2.- La posicion no esta marcada como reproceso
        3.- La operacion indicada en la posicion existe en almacenamiento existe en almacenamiento
        4.- la fecha de la operacion de almacenamiento es menor a la fcha de operacion que se esta procesando
        """
        alteracion = AlteracionPosicion(posicion=posicion, flg_reproceso=False)
        operacion_previa_posicion = copy.copy(datos.operacion_1)
        operacion_previa_posicion.fch_operacion = date.fromisoformat("2023-11-05")
        operacion_en_curso = copy.copy(datos.operacion_2)
        operacion_en_curso.fch_operacion = date.fromisoformat("2023-11-04")
        mock_operacion_reader_get.return_value = operacion_previa_posicion
        registro_multiple_oper_manager.establecer_reproceso(alteracion=alteracion, operacion=operacion_en_curso)
        self.assertTrue(alteracion.flg_reproceso)


