#Modelos para la validación para asegurar la integridad de la DB
from pydantic import BaseModel
from datetime import datetime
from typing import Dict,Any

class EntireMeasure(BaseModel):
    serial_number: str
    timestamp: datetime
    parameters: Dict[str, Any] 

class MeasureModel (BaseModel):
    meter_id: int
    timestamp: datetime
    parameters: Dict[str, float]

class RuleModel(BaseModel):
    meter_id : int
    parameter : str
    threshold : int
    comparator : str
    level : int

class EventModel(BaseModel):
    measure_id:int
    rule_id: int

class idRequest(BaseModel):
    id_measure: int


class NotifModel(BaseModel):
    event_id:int
    acked:bool
    first_sent:datetime
    channel: str