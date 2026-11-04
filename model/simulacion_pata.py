from config.extensions import db


class SimulacionPataModel(db.Model):
    __tablename__ = "tb_simulacion_pata"
    __table_args__ = (
        db.Index("ix_sim_pata_contrato", "cod_symbol"),
        db.UniqueConstraint(
            "id_simulacion_grupo", "orden", name="uq_sim_pata_orden"
        ),
        db.CheckConstraint(
            "tipo_opcion IN ('CALL', 'PUT')", name="chk_sim_pata_tipo"
        ),
        db.CheckConstraint(
            "posicion IN ('LONG', 'SHORT')", name="chk_sim_pata_posicion"
        ),
        db.CheckConstraint("cantidad > 0", name="chk_sim_pata_cantidad"),
    )

    id_simulacion_pata = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único de la pata de opción.",
    )
    id_simulacion_grupo = db.Column(
        db.BigInteger,
        db.ForeignKey(
            "tb_simulacion_grupo.id_simulacion_grupo",
            name="fk_sim_pata_grupo",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Grupo al que pertenece esta pata.",
    )
    orden = db.Column(
        db.SmallInteger, nullable=False, comment="Posición de la pata en el grupo."
    )
    id_contrato_opcion = db.Column(
        db.Integer,
        db.ForeignKey(
            "tb_contrato_opcion.id_contrato_opcion",
            name="fk_sim_pata_contrato_opcion",
        ),
        nullable=True,
        comment="Contrato del catálogo, si está disponible.",
    )
    cod_symbol = db.Column(
        db.String(50),
        nullable=False,
        comment="Símbolo OCC guardado como snapshot para restaurar la pata.",
    )
    tipo_opcion = db.Column(
        db.String(4), nullable=False, comment="Tipo de opción: CALL o PUT."
    )
    fecha_vencimiento = db.Column(
        db.Date, nullable=False, comment="Fecha de vencimiento del contrato."
    )
    strike = db.Column(
        db.Numeric(18, 6), nullable=False, comment="Precio de ejercicio del contrato."
    )
    posicion = db.Column(
        db.String(5), nullable=False, comment="Sentido de la posición: LONG o SHORT."
    )
    cantidad = db.Column(
        db.Integer,
        nullable=False,
        default=1,
        server_default="1",
        comment="Número de contratos; debe ser mayor que cero.",
    )
    multiplicador = db.Column(
        db.Integer,
        nullable=False,
        default=100,
        server_default="100",
        comment="Unidades del subyacente por contrato.",
    )
    precio_apertura = db.Column(
        db.Numeric(18, 6),
        nullable=True,
        comment="Prima por unidad pagada o recibida al abrir la posición.",
    )
    moneda_id = db.Column(
        db.String(3),
        nullable=False,
        default="USD",
        server_default="USD",
        comment="Código ISO de la moneda de la prima.",
    )
    fec_creacion = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        comment="Fecha y hora en que se agregó la pata al grupo.",
    )

    grupo = db.relationship("SimulacionGrupoModel", back_populates="patas")
    contrato_opcion = db.relationship("ContratoOpcionModel")

    def __repr__(self):
        return f"<SimulacionPata {self.id_simulacion_pata} {self.cod_symbol}>"
