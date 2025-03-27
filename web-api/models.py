from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    alias = Column(String)  # 종목명
    region = Column(String)  # 한국/미국
    price = Column(Float)  # 현재가
    volume = Column(Integer)  # 거래량
    high = Column(Float)  # 고가
    low = Column(Float)  # 저가
    open = Column(Float)  # 시가
    previous_close = Column(Float)  # 전일종가
    is_open = Column(Boolean, default=True)  # 장 열림/마감
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    prices = relationship("StockPrice", back_populates="stock")
    predictions = relationship("StockPrediction", back_populates="stock")

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    timestamp = Column(DateTime(timezone=True), index=True)
    price = Column(Float)  # 가격
    volume = Column(Integer)  # 거래량
    ma5 = Column(Float)  # 5일 이동평균
    ma20 = Column(Float)  # 20일 이동평균
    upper_band = Column(Float)  # 볼린저 밴드 상단
    lower_band = Column(Float)  # 볼린저 밴드 하단

    stock = relationship("Stock", back_populates="prices")

class StockPrediction(Base):
    __tablename__ = "stock_predictions"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    timestamp = Column(DateTime(timezone=True), index=True)
    predicted_price = Column(Float)  # AI 예측가
    confidence = Column(Float)  # 예측 신뢰도 (0~1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stock = relationship("Stock", back_populates="predictions") 