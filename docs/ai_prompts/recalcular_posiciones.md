Necesito implementar el endpoint para recalcular posiciones.

# Controller:
modulo: controller/posicion.py
clase: PosicionController
funcion: recalcular_posiciones(self, args=None)

* Implementar el schema pydantic RecalcularPosicionesRequest en schemas/posicion.py
    - Los argumentos dentro de args, son los siguientes:
        - id_cuenta: int
        - cod_tipo_procesamiento: Tendrá 2 valores, "TODOS" o "SELECCIONADOS"
        - cod_symbol_list: list[str]
    - Validaciones adicionales que hay que tener en cuenta:
        - Si cod_tipo_procesamiento es "TODOS", no se debe enviar cod_symbol_list
        - Si cod_tipo_procesamiento es "SELECCIONADOS", se debe enviar cod_symbol_list

# Lógica:
modulo: service/posicion.py
clase: PosicionService
funcion: recalcular_posiciones(self, dto: RecalcularPosicionesRequest)

* La lógica es la siguiente:
    - Si cod_tipo_procesamiento es "TODOS", se debe recalcular todas las posiciones de la cuenta
    - Si cod_tipo_procesamiento es "SELECCIONADOS", se debe recalcular solo las posiciones de los symbols enviados en cod_symbol_list

* Cuando recalculan todas las posiciones, se necesita obtener todas las transacciones por cuenta, por ello se debe implementar en reader/transaccion.py, una función que retorne todas las transacciones de la cuenta, ordenadas por fecha y hora de transacción, y por número de orden de transacción.
    - nombre de la función: get_transacciones_x_cuenta(self, id_cuenta: int)

* Cuando se recalculan las posiciones por determinados symbols, implementa una funcion en reader/transaccion.py para poder filtrar por cuenta y por la lista de symbols. Ordenar por fecha y hora de transacción, y por número de orden de transacción.
    - nombre de la función: get_transacciones_x_cuenta_y_symbols(self, id_cuenta: int, cod_symbol_list: list[str])

* Una posición se calcula en base a la cuenta y el symbol.

* Si no hay transacciones con `ind_requiere_revision` = 1, entonces se puede reprocesar las transacciones.

## Validar Transaccion de apertura

* Se tiene que validar que la primera transacción de la cuenta y symbol tiene que ser una transaccion de apertura, caso contrario error, el codigo de una transaccion de apertura es "O", campo IndicadorApcierreModel.cod_indicador.

* Usar para obtener el identificador de apertura/cierre constants/indicador_apcierre.py

## Calcular los saldos de la transacciones

* El modelo es TransaccionSaldoModel, y para el calculo de los saldos, debes basarte en el documento: docs/transaccion_saldo.md

## Calcular los movimientos de saldos

* El modelo es MovimientoSaldoModel, y para el calculo de los movimientos, debes basarte en el documento: docs/movimiento_saldo.md







    