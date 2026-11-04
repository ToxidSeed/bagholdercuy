# Propuesta de tablas: simulación de estrategias de opciones

## Alcance observado en la interfaz

La pantalla permite elegir un subyacente, crear varios grupos de estrategia, nombrarlos, agregar patas de opciones, cambiar LONG/SHORT y cantidad, duplicar o invertir grupos, y guardar/cargar/eliminar estrategias. El guardado actual persiste en `localStorage` un objeto con metadatos, grupos y contratos. Las métricas (débito/crédito, beneficio/pérdida máxima, breakeven, mark y P&L) se calculan en el cliente.

La propuesta persiste las estrategias guardadas y sus patas. El estado transitorio del simulador (grupo expandido, vista de tarjetas, cotización que se refresca) no requiere persistencia. Las métricas se mantienen derivadas para evitar inconsistencias.

## Relaciones

```text
tb_usuario 1 ── N tb_simulacion_estrategia
tb_symbol 1 ── N tb_simulacion_estrategia (subyacente)
tb_simulacion_estrategia 1 ── N tb_simulacion_grupo
tb_simulacion_grupo 1 ── N tb_simulacion_pata
tb_contrato_opcion 0..1 ── N tb_simulacion_pata
```

Se reutilizan `tb_usuario`, `tb_symbol` y `tb_contrato_opcion`, que son las tablas representadas por los modelos vigentes del proyecto. Las tablas antiguas `tb_stock_symbol` y `tb_option_contract` no se usan en esta propuesta. El subyacente se obtiene por `id_subyacente_symbol` mediante un `JOIN` a `tb_symbol`; no se duplican el símbolo ni el nombre. La pata referencia `tb_contrato_opcion` cuando el contrato existe en el catálogo y conserva `cod_symbol` para poder restaurarla aun si falta esa referencia. El precio del subyacente y su timestamp se consultan en vivo y no se guardan en estas tablas.

## DDL propuesto (MariaDB)

```sql
CREATE TABLE tb_simulacion_estrategia (
  id_simulacion_estrategia BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único del guardado completo de simulación.',
  id_usuario INT NOT NULL COMMENT 'Usuario propietario del guardado; referencia a tb_usuario.id.',
  id_subyacente_symbol INT NOT NULL COMMENT 'Identificador del instrumento subyacente; referencia a tb_symbol.id_symbol.',
  nombre VARCHAR(120) NOT NULL COMMENT 'Nombre asignado por el usuario al guardado.',
  etiqueta VARCHAR(40) NOT NULL DEFAULT 'ESTRATEGIA' COMMENT 'Categoría o etiqueta elegida para clasificar el guardado.',
  notas TEXT NULL COMMENT 'Notas libres asociadas al guardado.',
  moneda_id CHAR(3) NOT NULL DEFAULT 'USD' COMMENT 'Código ISO de la moneda de los importes de la simulación.',
  fec_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora en que se creó el guardado.',
  fec_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha y hora de la última modificación del guardado.',
  PRIMARY KEY (id_simulacion_estrategia),
  KEY ix_sim_estrategia_usuario_fecha (id_usuario, fec_creacion),
  KEY ix_sim_estrategia_subyacente (id_subyacente_symbol),
  CONSTRAINT fk_sim_estrategia_usuario FOREIGN KEY (id_usuario)
    REFERENCES tb_usuario (id),
  CONSTRAINT fk_sim_estrategia_symbol FOREIGN KEY (id_subyacente_symbol)
    REFERENCES tb_symbol (id_symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tb_simulacion_grupo (
  id_simulacion_grupo BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único del grupo dentro de la simulación guardada.',
  id_simulacion_estrategia BIGINT NOT NULL COMMENT 'Guardado al que pertenece el grupo; referencia a tb_simulacion_estrategia.id_simulacion_estrategia.',
  orden SMALLINT NOT NULL COMMENT 'Posición del grupo en la lista de la interfaz.',
  nombre VARCHAR(120) NOT NULL COMMENT 'Nombre editable del grupo de estrategia.',
  tipo VARCHAR(40) NOT NULL DEFAULT 'CUSTOM' COMMENT 'Tipo de estrategia del grupo; CUSTOM cuando es definido libremente.',
  fec_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora en que se agregó el grupo al guardado.',
  PRIMARY KEY (id_simulacion_grupo),
  UNIQUE KEY uq_sim_grupo_orden (id_simulacion_estrategia, orden),
  CONSTRAINT fk_sim_grupo_estrategia FOREIGN KEY (id_simulacion_estrategia)
    REFERENCES tb_simulacion_estrategia (id_simulacion_estrategia) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tb_simulacion_pata (
  id_simulacion_pata BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único de la pata de opción.',
  id_simulacion_grupo BIGINT NOT NULL COMMENT 'Grupo al que pertenece la pata; referencia a tb_simulacion_grupo.id_simulacion_grupo.',
  orden SMALLINT NOT NULL COMMENT 'Posición de la pata dentro del grupo en la interfaz.',
  id_contrato_opcion INT NULL COMMENT 'Contrato de opción del catálogo, si está disponible; referencia a tb_contrato_opcion.id_contrato_opcion.',
  cod_symbol VARCHAR(50) NOT NULL COMMENT 'Símbolo OCC del contrato guardado como snapshot para restaurar la pata.',
  tipo_opcion VARCHAR(4) NOT NULL COMMENT 'Derecho de la opción: CALL o PUT.',
  fecha_vencimiento DATE NOT NULL COMMENT 'Fecha de vencimiento del contrato de opción.',
  strike DECIMAL(18,6) NOT NULL COMMENT 'Precio de ejercicio del contrato.',
  posicion VARCHAR(5) NOT NULL COMMENT 'Sentido de la posición: LONG o SHORT.',
  cantidad INT NOT NULL DEFAULT 1 COMMENT 'Número de contratos; debe ser mayor que cero.',
  multiplicador INT NOT NULL DEFAULT 100 COMMENT 'Cantidad de unidades del subyacente por contrato.',
  precio_apertura DECIMAL(18,6) NULL COMMENT 'Prima por unidad pagada o recibida al establecer la posición.',
  moneda_id CHAR(3) NOT NULL DEFAULT 'USD' COMMENT 'Código ISO de la moneda de la prima.',
  fec_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora en que se agregó la pata al grupo.',
  PRIMARY KEY (id_simulacion_pata),
  UNIQUE KEY uq_sim_pata_orden (id_simulacion_grupo, orden),
  KEY ix_sim_pata_contrato (cod_symbol),
  CONSTRAINT fk_sim_pata_grupo FOREIGN KEY (id_simulacion_grupo)
    REFERENCES tb_simulacion_grupo (id_simulacion_grupo) ON DELETE CASCADE,
  CONSTRAINT fk_sim_pata_contrato_opcion FOREIGN KEY (id_contrato_opcion)
    REFERENCES tb_contrato_opcion (id_contrato_opcion),
  CONSTRAINT chk_sim_pata_tipo CHECK (tipo_opcion IN ('CALL', 'PUT')),
  CONSTRAINT chk_sim_pata_posicion CHECK (posicion IN ('LONG', 'SHORT')),
  CONSTRAINT chk_sim_pata_cantidad CHECK (cantidad > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Correspondencia con la interfaz

| Interfaz / dato | Persistencia |
| --- | --- |
| Guardado: `nombre`, `tipo`/etiqueta, `notas` | `tb_simulacion_estrategia` |
| Instrumento: `symbol`, `name`, `asset_type` | `id_subyacente_symbol`; obtener todos sus datos con un `JOIN` a `tb_symbol` |
| Precio y fecha de cotización del subyacente | Consultar en vivo; no se persisten en las tablas de simulación |
| Cada grupo: nombre, tipo y orden | `tb_simulacion_grupo` |
| Cada contrato/pata: OCC symbol, CALL/PUT, strike, vencimiento, LONG/SHORT, cantidad, precio de apertura | `tb_simulacion_pata` |
| `bid`, `ask`, `last`, delta, theta e ITM | Cotización de mercado, no características permanentes de la pata. Consultarlas al abrir/refrescar. Si se requiere auditoría histórica, añadir tabla de snapshots separada. |
| Prima neta, max profit/loss, breakevens, Mark y P&L | Calcular desde las patas y los datos de mercado; no persistir como fuente de verdad. |
| `expandida`, `vista_cards`, `forzar_expandida` | Estado visual de sesión; no persistir en esta primera versión. |

## Decisiones y reglas recomendadas

1. Una fila de `tb_simulacion_estrategia` representa un guardado completo, que puede incluir varios grupos, igual que el botón actual “Guardar Estrategia”.
2. Guardar cabecera, grupos y patas dentro de una transacción. Al borrar un guardado, `ON DELETE CASCADE` elimina sus grupos y patas.
3. `cantidad` es positiva; el sentido se representa exclusivamente mediante `posicion`. Para calcular flujo firmado se combina posición, precio de apertura, cantidad y multiplicador.
4. Usar `DECIMAL`, no `FLOAT`, para precios y strikes. La precisión elegida admite strikes fraccionarios y primas con más de dos decimales.
5. Los `CHECK` se validan en MariaDB moderno; si el servidor real no los aplica, validar también en la capa de aplicación.
6. Los identificadores de las tablas nuevas usan el nombre de la entidad como prefijo, por ejemplo `id_simulacion_estrategia`; las claves foráneas usan el identificador de la entidad referenciada, por ejemplo `id_simulacion_estrategia` en `tb_simulacion_grupo`.
7. La interfaz usa `id` de cadena para datos locales. La API puede mapear los identificadores SQL a sus DTOs y devolver patas anidadas por grupo sin cambiar el modelo relacional.

## Fuera del primer alcance

No hace falta una tabla de “sesión actual” para habilitar la biblioteca de guardados. Si se requiere restaurar automáticamente un borrador entre dispositivos, añadir luego una cabecera de simulación activa separada o un indicador de borrador y controlar su ciclo de vida. Si se requiere reconstruir exactamente cotizaciones antiguas, agregar `tb_simulacion_pata_cotizacion` con proveedor, timestamp, bid/ask/last y griegas; no mezclar esos snapshots con las definiciones guardadas.
