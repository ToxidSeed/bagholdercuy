# Documentación de Ingeniería de Datos - Proyecto Bagholder

## Entidad: `tb_movimiento_saldo`

### 1. Definición de la Entidad
La tabla `tb_movimiento_saldo` actúa como el **registro histórico y de auditoría** de las aplicaciones del algoritmo **FIFO**. A diferencia de `tb_transaccion_saldo` (que rastrea el inventario vivo), esta tabla documenta el evento preciso en que una transacción de cierre consume el saldo de una de apertura, consolidando el impacto financiero (ganancia o pérdida realizada).

### 2. Modelo Físico (DDL)
```sql
CREATE TABLE `tb_movimiento_saldo` (
  `id_movimiento_saldo` binary(16) NOT NULL,
  `id_transaccion_apertura` binary(16) NOT NULL,
  `id_transaccion_cierre` binary(16) NOT NULL,
  `ctd_aplicada` decimal(15,3) NOT NULL,
  `ctd_saldo_final_apertura` decimal(15,3) NOT NULL,
  `imp_ganancia` decimal(17,2) NOT NULL DEFAULT 0.00,
  `fch_hr_registro` datetime(3) NOT NULL DEFAULT current_timestamp(3),
  PRIMARY KEY (`id_movimiento_saldo`)
);
```

### 3. Diccionario de Datos

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| **id_movimiento_saldo** | binary(16) | UUID único del registro de aplicación. |
| **id_transaccion_apertura** | binary(16) | Referencia a la transacción que originó el lote (Maker). |
| **id_transaccion_cierre** | binary(16) | Referencia a la transacción que consume el lote (Taker). |
| **ctd_aplicada** | decimal(15,3) | Cantidad de unidades/acciones "neteadas" en este vínculo. |
| **ctd_saldo_final_apertura** | decimal(15,3) | Remanente del lote de apertura inmediatamente después de este movimiento. |
| **imp_ganancia** | decimal(17,2) | Beneficio neto (P&L realizado) en este emparejamiento específico. |
| **fch_hr_registro** | datetime(3) | Marca de tiempo del sistema al momento de la ejecución del motor. |

### 4. Especificaciones Funcionales y Reglas de Negocio

* **Trazabilidad de Lotes (Mapping):** Cada registro establece un vínculo físico e inmutable entre una apertura y el cierre que la consumió.
* **Granularidad de Aplicación:** Si una única transacción de cierre consume múltiples lotes de apertura, se generarán **tantos registros en esta tabla como lotes hayan sido afectados**.
* **Snapshot de Auditoría (`ctd_saldo_final_apertura`):** Almacena el remanente del lote de apertura inmediatamente después de este movimiento. Es vital para reconstruir estados de cuenta en cualquier punto del tiempo.
* **Cálculo de Ganancia Realizada:** Representa el P&L realizado en el emparejamiento específico de lotes.
    * **Fórmula:** $imp\_ganancia = ctd\_aplicada \times (imp\_unitario\_cierre - imp\_unitario\_apertura)$
* **Inmutabilidad:** Una vez registrado por el motor, el movimiento no debe ser modificado manualmente para garantizar la integridad de los reportes.

### 5. Flujo en el Motor de Reproceso (FIFO)

1.  **Identificación:** El motor detecta una transacción marcada como **Cierre**.
2.  **Búsqueda:** Localiza el saldo disponible más antiguo (según `fch_hr_transaccion` y `orden_fifo`) en `tb_transaccion_saldo`.
3.  **Cálculo:** Determina la `ctd_aplicada` como el valor mínimo entre el total del cierre y el saldo disponible del lote.
4.  **Registro:** Inserta el movimiento en `tb_movimiento_saldo` con la ganancia calculada.
5.  **Actualización de Inventario:** Actualiza los saldos remanentes en las tablas de inventario para reflejar el consumo.


