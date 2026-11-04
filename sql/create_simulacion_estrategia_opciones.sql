-- Crea las tablas para guardar estrategias simuladas de opciones.
-- Requiere las tablas vigentes tb_usuario, tb_symbol y tb_contrato_opcion.

CREATE TABLE tb_simulacion_estrategia (
  id_simulacion_estrategia BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único del guardado completo de simulación.',
  id_usuario INT NOT NULL COMMENT 'Usuario propietario; referencia a tb_usuario.id.',
  id_subyacente_symbol INT NOT NULL COMMENT 'Instrumento subyacente; referencia a tb_symbol.id_symbol.',
  nombre VARCHAR(120) NOT NULL COMMENT 'Nombre asignado por el usuario al guardado.',
  etiqueta VARCHAR(40) NOT NULL DEFAULT 'ESTRATEGIA' COMMENT 'Categoría o etiqueta para clasificar el guardado.',
  notas TEXT NULL COMMENT 'Notas libres asociadas al guardado.',
  moneda_id CHAR(3) NOT NULL DEFAULT 'USD' COMMENT 'Código ISO de la moneda de los importes.',
  fec_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de creación del guardado.',
  fec_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha y hora de la última modificación del guardado.',
  PRIMARY KEY (id_simulacion_estrategia),
  KEY ix_sim_estrategia_usuario_fecha (id_usuario, fec_creacion),
  KEY ix_sim_estrategia_subyacente (id_subyacente_symbol),
  CONSTRAINT fk_sim_estrategia_usuario FOREIGN KEY (id_usuario)
    REFERENCES tb_usuario (id),
  CONSTRAINT fk_sim_estrategia_symbol FOREIGN KEY (id_subyacente_symbol)
    REFERENCES tb_symbol (id_symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tb_simulacion_grupo (
  id_simulacion_grupo BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único del grupo guardado.',
  id_simulacion_estrategia BIGINT NOT NULL COMMENT 'Guardado al que pertenece el grupo.',
  orden SMALLINT NOT NULL COMMENT 'Posición del grupo en la interfaz.',
  nombre VARCHAR(120) NOT NULL COMMENT 'Nombre editable del grupo de estrategia.',
  tipo VARCHAR(40) NOT NULL DEFAULT 'CUSTOM' COMMENT 'Tipo de estrategia; CUSTOM si es definido libremente.',
  fec_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora en que se agregó el grupo al guardado.',
  PRIMARY KEY (id_simulacion_grupo),
  UNIQUE KEY uq_sim_grupo_orden (id_simulacion_estrategia, orden),
  CONSTRAINT fk_sim_grupo_estrategia FOREIGN KEY (id_simulacion_estrategia)
    REFERENCES tb_simulacion_estrategia (id_simulacion_estrategia) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tb_simulacion_pata (
  id_simulacion_pata BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único de la pata de opción.',
  id_simulacion_grupo BIGINT NOT NULL COMMENT 'Grupo al que pertenece la pata.',
  orden SMALLINT NOT NULL COMMENT 'Posición de la pata dentro del grupo.',
  id_contrato_opcion INT NULL COMMENT 'Contrato del catálogo, si está disponible; referencia a tb_contrato_opcion.id_contrato_opcion.',
  cod_symbol VARCHAR(50) NOT NULL COMMENT 'Símbolo OCC del contrato guardado como snapshot.',
  tipo_opcion VARCHAR(4) NOT NULL COMMENT 'Derecho de la opción: CALL o PUT.',
  fecha_vencimiento DATE NOT NULL COMMENT 'Fecha de vencimiento del contrato de opción.',
  strike DECIMAL(18,6) NOT NULL COMMENT 'Precio de ejercicio del contrato.',
  posicion VARCHAR(5) NOT NULL COMMENT 'Sentido de la posición: LONG o SHORT.',
  cantidad INT NOT NULL DEFAULT 1 COMMENT 'Número de contratos; debe ser mayor que cero.',
  multiplicador INT NOT NULL DEFAULT 100 COMMENT 'Unidades del subyacente por contrato.',
  precio_apertura DECIMAL(18,6) NULL COMMENT 'Prima por unidad pagada o recibida al abrir la posición.',
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
