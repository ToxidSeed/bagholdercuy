from config.extensions import db


class SimulacionGrupoModel(db.Model):
    __tablename__ = "tb_simulacion_grupo"
    __table_args__ = (
        db.UniqueConstraint(
            "id_simulacion_estrategia", "orden", name="uq_sim_grupo_orden"
        ),
    )

    id_simulacion_grupo = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único del grupo guardado.",
    )
    id_simulacion_estrategia = db.Column(
        db.BigInteger,
        db.ForeignKey(
            "tb_simulacion_estrategia.id_simulacion_estrategia",
            name="fk_sim_grupo_estrategia",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Guardado al que pertenece el grupo.",
    )
    orden = db.Column(
        db.SmallInteger, nullable=False, comment="Posición del grupo en la interfaz."
    )
    nombre = db.Column(
        db.String(120), nullable=False, comment="Nombre editable del grupo."
    )
    tipo = db.Column(
        db.String(40),
        nullable=False,
        default="CUSTOM",
        server_default="CUSTOM",
        comment="Tipo de estrategia; CUSTOM si es definido libremente.",
    )
    fec_creacion = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        comment="Fecha y hora en que se agregó el grupo al guardado.",
    )

    estrategia = db.relationship("SimulacionEstrategiaModel", back_populates="grupos")
    patas = db.relationship(
        "SimulacionPataModel",
        back_populates="grupo",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="SimulacionPataModel.orden",
    )

    def __repr__(self):
        return f"<SimulacionGrupo {self.id_simulacion_grupo} nombre={self.nombre!r}>"
