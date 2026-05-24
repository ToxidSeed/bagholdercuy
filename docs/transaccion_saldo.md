# Documentación de Ingeniería de Datos - Sistema de Trading

## Entidad: `tb_transaccion_saldo`

### 1. Definición de la Entidad
[cite_start]La tabla `tb_transaccion_saldo` tiene una relación 1 a 1 con tu `tb_transaccion` original[cite: 810]. [cite_start]Esta entidad no está guardando "la posición global de un símbolo", sino el saldo restante de un lote específico[cite: 811]. [cite_start]Es una tabla limpia, ligera y perfecta para gestionar la "bolsa de lotes" de tu algoritmo FIFO[cite: 812].

### 2. Modelo Físico (DDL)
```sql
CREATE TABLE `tb_transaccion_saldo` (
  `id_transaccion` binary(16) NOT NULL,
  `ctd_saldo` decimal(15,3) NOT NULL,
  `imp_saldo` decimal(17,2) NOT NULL DEFAULT 0.00,
  `fch_hr_audit` datetime(3) NOT NULL DEFAULT current_timestamp(3)
);

```

### 3. Especificaciones Funcionales y Reglas de Negocio

La tabla `tb_transaccion_saldo` es una tabla auxiliar que se utiliza para mantener el registro de los saldos de las transacciones.

* **Motor FIFO (First-In, First-Out):** Esta estructura es exactamente lo que necesitas para tu motor FIFO (First-In, First-Out), ya que este algoritmo empareja los cierres con las aperturas más antiguas disponibles.
* **Consumo de Lotes:** La lógica principal consiste en ir actualizando (descontando) el `ctd_saldo` de las compras más antiguas cada vez que importes una nueva transacción de venta para consumir el FIFO.


### 4 Estrategia de Cálculo Dinámico

Dado que a la larga quieres ver tus "posiciones", la forma correcta de obtener ese importe promedio dinámico que cambia con las compras y ventas no es guardándolo en una tabla física, sino calculándolo al vuelo (agrupando los lotes):

* **En la Base de Datos (Vista SQL):** Puedes crear una vista que agrupe los saldos sumando las cantidades y los importes totales por símbolo, y que ahí mismo divida uno entre otro.
* **En SQLAlchemy (Backend):** Puedes usar un `@property` en tu modelo o una consulta de agregación (`func.sum`) para entregarle el promedio ya procesado a tu frontend en Vue. Se calculará dinámicamente mediante vistas SQL o en el backend.

### 5. Casuísticas de Prueba y Estados de Tabla

A continuación se detallan los escenarios de movimientos de inventario y cómo debe quedar reflejado el estado final en `tb_transaccion_saldo` (manteniendo registros con saldo 0 para auditoría).

#### Caso 1: Cierre Parcial (Reducción de Inventario)
**Escenario:**
1. Compra 100 SOXL @ 25.00 (Inversión inicial: 2,500.00)
2. Venta 50 SOXL @ 15.00 (Consumo parcial)

**Lógica:** El motor busca el lote de la Tx 1 y reduce la cantidad a la mitad. El importe se recalcula sobre el costo original ($25).

| id_transaccion | ctd_saldo | imp_saldo | fch_hr_audit | Notas |
| :--- | :--- | :--- | :--- | :--- |
| `0xTX001...` | **50.000** | **1250.00** | 2024-05-20... | Saldo remanente (50 * 25.00) |

---

#### Caso 2: Cierre Total (Lote Agotado)
**Escenario:**
1. Compra 100 SOXL @ 30.00 (Inversión inicial: 3,000.00)
2. Venta 100 SOXL @ 25.00 (Consumo total)

**Lógica:** El motor consume la totalidad del lote. Al no haber remanente, ambos valores financieros deben ser exactamente cero.

| id_transaccion | ctd_saldo | imp_saldo | fch_hr_audit | Notas |
| :--- | :--- | :--- | :--- | :--- |
| `0xTX002...` | **0.000** | **0.00** | 2024-05-20... | Lote cerrado totalmente. |

---

#### Caso 3: Cambio de Polaridad (De Long a Short)
**Escenario:**
1. Compra 100 SOXL @ 30.00 (Inversión inicial: 3,000.00)
2. Venta 120 SOXL @ 28.00 (Cierre total + Apertura de corto)

**Lógica:** - Los primeros 100 de la venta agotan la Tx 1 (saldo 0).
- Los 20 restantes de la venta generan una **nueva fila** de inventario negativo en la tabla de saldos, usando el `id_transaccion` de la venta.

| id_transaccion | ctd_saldo | imp_saldo | fch_hr_audit | Notas |
| :--- | :--- | :--- | :--- | :--- |
| `0xTX001...` | **0.000** | **0.00** | 2024-05-20... | Lote Long agotado. |
| `0xTX002...` | **-20.000** | **-560.00** | 2024-05-20... | Apertura Short (20 * 28.00) |

---

#### Resumen de Reglas Aplicadas
1. **Regla de Auditoría:** No se realizan `DELETE` físicos; los lotes consumidos permanecen con `ctd_saldo = 0`.
2. **Regla de Importe:** El `imp_saldo` siempre se actualiza como `ctd_saldo * imp_unitario` de la transacción que originó la fila.
3. **Regla de Signos:** Las posiciones cortas (Short) se representan con valores negativos tanto en cantidad como en importe para diferenciar la dirección de la obligación financiera.