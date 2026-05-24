# Documentación de Ingeniería de Datos - Sistema de Trading

## 1. Definición de la Entidad: `tb_transaccion`
La tabla `tb_transaccion` es el núcleo del registro de operaciones. Su propósito es actuar como un libro auxiliar de movimientos financieros, capturando cada ejecución de mercado y su impacto dual: el cambio en el inventario de activos y la afectación real en el flujo de caja operativo (efectivo).

### 2. Modelo Físico (DDL)
```sql
CREATE TABLE `tb_transaccion` (
  `id_transaccion` binary(16) NOT NULL,
  `id_transaccion_origen` binary(16) DEFAULT NULL,
  `id_cuenta` int(11) NOT NULL,
  `cod_symbol` varchar(25) NOT NULL,
  `id_instrumento_financiero` int(11) DEFAULT NULL,
  `id_tipo_transaccion` int(11) NOT NULL,
  `id_indicador_apcierre` int NOT NULL,
  `id_evento_origen` int NOT NULL,
  `fch_hr_transaccion` datetime(3) NOT NULL,
  `orden_fifo` int(11) NOT NULL,
  `ind_requiere_revision` tinyint not null, 
  `cantidad` decimal(15,3) NOT NULL,
  `imp_unitario` decimal(17,2) NOT NULL,
  `imp_bruto` decimal(17,2) NOT NULL,
  `fch_hr_registro` datetime(3) NOT NULL DEFAULT current_timestamp(3),  
  PRIMARY KEY (`id_transaccion`)
)
```


### 3. Especificaciones Funcionales y Reglas de Negocio

Para garantizar la integridad de los datos financieros y la correcta conciliación con los reportes de Interactive Brokers, se deben seguir las siguientes definiciones extendidas:

| Campo | Especificación Técnica y Regla de Negocio |
| :--- | :--- |
| **`cantidad`** | **Variación del Inventario de Activos.** Representa el flujo neto de unidades del instrumento. <br> - **Valor Positivo (+):** Incrementa la posición (Compra para abrir *long* o Compra para cubrir *short*). <br> - **Valor Negativo (-):** Disminuye la posición (Venta para cerrar *long* o Venta para abrir *short*). |
| **`imp_unitario`** | **Precio de Ejecución.** Es el valor de mercado por unidad al que se pactó la transacción. Se almacena siempre como valor absoluto positivo para mantener la trazabilidad de precios históricos. |
| **`imp_bruto`** | **Monto Bruto de la Operación (Proceeds).** Define el impacto real en el flujo de efectivo (*cash flow*). <br> - **Lógica:** Se calcula como `(cantidad * imp_unitario) * -1`. <br> - **Signo Negativo (-):** Salida de efectivo (al comprar activos o cubrir cortos). <br> - **Signo Positivo (+):** Entrada de efectivo (al vender activos o abrir cortos). |
| **`orden_fifo`** | **Secuenciador de Liquidación.** Cuando 2 o mas transacciones tienen la misma fecha y hora este secuencial es el que diferencia una de otra. |
| **`ind_requiere_revision`** | **Indicador de Supervisión.** Bandera utilizada por el sistema para señalar transacciones que requieren validación humana antes de su procesamiento o contabilización final. |

### 4. Matriz de Signos y Flujo de Caja

Para garantizar la integridad contable y facilitar la conciliación de saldos de efectivo, la tabla `tb_transaccion` sigue una lógica de signos donde la columna `cantidad` refleja el inventario de activos y `imp_bruto` refleja el movimiento de capital bruto (*Gross Proceeds*).

| Tipo de Operación | Signo Cantidad | Signo Importe Bruto | Descripción del Flujo |
| :--- | :---: | :---: | :--- |
| **Compra (Buy to Open / Cover)** | `+` | `-` | **Incremento de Activos:** El flujo de efectivo es negativo debido a la adquisición de títulos o cobertura de cortos. |
| **Venta (Sell to Close / Open)** | `-` | `+` | **Disminución de Activos:** El flujo de efectivo es positivo por la liquidación de títulos o la apertura de una posición corta. |

#### Resumen de Lógica para Implementación (Python/SQL)
Para normalizar los datos provenientes de fuentes externas hacia el estándar de esta tabla, se aplica la siguiente función lógica:

* **Impacto en Inventario:** `cantidad` (mantiene signo del broker).
* **Impacto en Caja:** `imp_transaccion = (cantidad * imp_unitario) * -1`.



> [!NOTE]
> Esta estructura permite que una simple operación de agregado `SUM(imp_transaccion)` sobre la tabla devuelva el balance neto de capital invertido o recuperado en un periodo determinado, sin necesidad de condicionales adicionales.