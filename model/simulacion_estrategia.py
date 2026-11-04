from config.extensions import db


class SimulacionEstrategiaModel(db.Model):
    __tablename__ = "tb_simulacion_estrategia"
    __table_args__ = (
        db.Index("ix_sim_estrategia_usuario_fecha", "id_usuario", "fec_creacion"),
        db.Index("ix_sim_estrategia_subyacente", "id_subyacente_symbol"),
    )

    id_simulacion_estrategia = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único del guardado completo de simulación.",
    )
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("tb_usuario.id", name="fk_sim_estrategia_usuario"),
        nullable=False,
        comment="Usuario propietario del guardado; referencia a tb_usuario.id.",
    )
    id_subyacente_symbol = db.Column(
        db.Integer,
        db.ForeignKey("tb_symbol.id_symbol", name="fk_sim_estrategia_symbol"),
        nullable=False,
        comment="Instrumento subyacente; referencia a tb_symbol.id_symbol.",
    )
    nombre = db.Column(
        db.String(120), nullable=False, comment="Nombre asignado al guardado."
    )
    etiqueta = db.Column(
        db.String(40),
        nullable=False,
        default="ESTRATEGIA",
        server_default="ESTRATEGIA",
        comment="Categoría o etiqueta para clasificar el guardado.",
    )
    notas = db.Column(db.Text, nullable=True, comment="Notas libres del guardado.")
    moneda_id = db.Column(
        db.String(3),
        nullable=False,
        default="USD",
        server_default="USD",
        comment="Código ISO de la moneda de los importes.",
    )
    fec_creacion = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        comment="Fecha y hora de creación del guardado.",
    )
    fec_actualizacion = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        comment="Fecha y hora de la última modificación del guardado.",
    )

    subyacente = db.relationship("SymbolModel", foreign_keys=[id_subyacente_symbol])
    grupos = db.relationship(
        "SimulacionGrupoModel",
        back_populates="estrategia",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="SimulacionGrupoModel.orden",
    )

    def __repr__(self):
        return (
            f"<SimulacionEstrategia {self.id_simulacion_estrategia} "
            f"nombre={self.nombre!r}>"
        )
