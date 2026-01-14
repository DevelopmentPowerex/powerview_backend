from ..core import Base
from sqlalchemy import Column, Integer,ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import JSONB

class Measurement(Base):
    __tablename__='measurements'

    id= Column(Integer, primary_key=True)
    meter_id= Column(Integer , ForeignKey('meters.id'),nullable = False )
    timestamp=Column(DateTime, nullable = False, index=True)
    parameters=Column(JSONB, nullable=False)

    def __repr__(self):
        return f'<Medicion a las {self.ts} para el medidor {self.sn}>'