from app import app, db

def run():
    with app.app_context():
        # 1. Crear tabla tb_ibkr_contract_map
        db.session.execute(db.text("""
            CREATE TABLE IF NOT EXISTS tb_ibkr_contract_map (
              id_ibkr_contract_map INT NOT NULL AUTO_INCREMENT,
              id_symbol INT NULL,
              id_contrato_opcion INT NULL,
              conid BIGINT NOT NULL,
              fch_registro DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
              fch_audit DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
              PRIMARY KEY (id_ibkr_contract_map),
              UNIQUE KEY uq_ibkr_contract_map_symbol (id_symbol),
              UNIQUE KEY uq_ibkr_contract_map_opcion (id_contrato_opcion),
              KEY idx_ibkr_contract_map_conid (conid),
              CONSTRAINT fk_ibkr_contract_map_symbol FOREIGN KEY (id_symbol) REFERENCES tb_symbol (id_symbol) ON DELETE CASCADE,
              CONSTRAINT fk_ibkr_contract_map_opcion FOREIGN KEY (id_contrato_opcion) REFERENCES tb_contrato_opcion (id_contrato_opcion) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """))

        # 2. Asegurar índice en tb_ibkr_contract(cod_symbol) para que los joins sean instantáneos
        try:
            db.session.execute(db.text("CREATE INDEX idx_ibkr_contract_cod_symbol ON tb_ibkr_contract(cod_symbol)"))
        except Exception:
            pass

        db.session.commit()
        print("Table tb_ibkr_contract_map created or already exists.")

if __name__ == "__main__":
    run()
