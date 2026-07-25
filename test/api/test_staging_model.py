import pytest
from model.staging_market_data import StagingMarketDataModel
from sqlalchemy.dialects import mysql
from sqlalchemy import Index

def test_staging_model_metadata():
    # Verify the table name
    assert StagingMarketDataModel.__tablename__ == "tb_staging_market_data"

def test_staging_model_columns():
    # Verify column existence and attributes
    columns = StagingMarketDataModel.__table__.columns
    
    assert "id_staging" in columns
    assert columns["id_staging"].primary_key is True
    
    assert "proveedor" in columns
    assert columns["proveedor"].nullable is False
    
    assert "endpoint" in columns
    assert columns["endpoint"].nullable is False
    
    assert "ticker" in columns
    assert columns["ticker"].nullable is True
    
    assert "file_path" in columns
    assert columns["file_path"].nullable is False
    
    assert "file_size_kb" in columns
    assert columns["file_size_kb"].nullable is False
    assert columns["file_size_kb"].default.arg == 0
    
    assert "estado" in columns
    assert columns["estado"].nullable is False
    assert columns["estado"].default.arg == "PENDIENTE"
    
    assert "fch_hr_creacion" in columns
    assert columns["fch_hr_creacion"].nullable is False

def test_staging_model_indexes():
    # Verify that indexes are defined correctly
    indexes = StagingMarketDataModel.__table__.indexes
    
    index_names = {idx.name for idx in indexes}
    assert "idx_estado_proveedor" in index_names
    assert "idx_ticker" in index_names
    
    # Check column composition for the composite index
    composite_idx = next(idx for idx in indexes if idx.name == "idx_estado_proveedor")
    idx_cols = [col.name for col in composite_idx.columns]
    assert idx_cols == ["estado", "proveedor"]
    
    # Check column composition for the ticker index
    ticker_idx = next(idx for idx in indexes if idx.name == "idx_ticker")
    ticker_cols = [col.name for col in ticker_idx.columns]
    assert ticker_cols == ["ticker"]
