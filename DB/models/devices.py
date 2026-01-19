from ..core import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

class Meter(Base):
    __tablename__='meters'

    id= Column(Integer, primary_key=True)
    serial_number=Column(String, unique= True, nullable = False)
    model=Column(Integer, ForeignKey('device_models.id') , nullable = True)
    project_id=Column(Integer, ForeignKey('projects.id') , nullable = True)
    nickname= Column(String(20),nullable=False)
    
    def __repr__(self):
        return f'<Medidor: {self.serial_number} >'

class DeviceModel(Base):
    __tablename__='device_models'

    id= Column(Integer, primary_key=True)
    model_name=Column(String(20) , nullable = False)

    def __repr__(self):
        return f'<Modelo de dispositivo: {self.model_name} >'
    
class ParametersPVM3(Base):
    __tablename__='parameters_pvm3'
    id= Column(Integer, primary_key=True)
    param_code = Column(String(20), unique=True, nullable=False) 
    description = Column(String(100), nullable=False) 
    unit = Column(String(10), nullable=False)               
    
    def __repr__(self):
        return f'<{self.param_code} - {self.description}>'
    
class ModelBParam(Base):
    __tablename__='available_params_per_model'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('device_models.id'), nullable=False)
    parameter_id = Column(Integer, ForeignKey('parameters_pvm3.id'), nullable=False)

    def __repr__(self):
        return f'<{self.model_id} - {self.parameter_id}>'