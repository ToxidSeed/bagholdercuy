from pydantic import BaseModel, Field
from typing import Dict, Optional


class AlphavantageMetaData(BaseModel):
    information: Optional[str] = Field(default=None, alias="1. Information")
    symbol: Optional[str] = Field(default=None, alias="2. Symbol")
    last_refreshed: Optional[str] = Field(default=None, alias="3. Last Refreshed")
    output_size: Optional[str] = Field(default=None, alias="4. Output Size")
    time_zone: Optional[str] = Field(default=None, alias="5. Time Zone")


class AlphavantageDailyEntry(BaseModel):
    open: float = Field(..., alias="1. open")
    high: float = Field(..., alias="2. high")
    low: float = Field(..., alias="3. low")
    close: float = Field(..., alias="4. close")
    volume: float = Field(default=0.0, alias="5. volume")


class AlphavantageDailyResponse(BaseModel):
    meta_data: Optional[AlphavantageMetaData] = Field(default=None, alias="Meta Data")
    time_series: Dict[str, AlphavantageDailyEntry] = Field(..., alias="Time Series (Daily)")


class AlphavantageDailyQuote(BaseModel):
    symbol: str
    price_date: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class AlphavantageSeriesLoadParams(BaseModel):
    cod_symbol: str
    fch_desde: Optional[str] = ""
    fch_hasta: Optional[str] = ""
    modo_carga: Optional[str] = "Append"

