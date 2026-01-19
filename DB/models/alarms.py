from sqlalchemy import (
    Column, Integer, String, ForeignKey, Double, Enum as SQLEnum)

from sqlalchemy.orm import relationship

#Base declarativa para cada modelo
from ..core import Base

#Declaraciones Enum Generales de la DB
from ..enums import Comparators, AlarmLevel, AlarmChannels 

class AlarmLevels(Base):
    __tablename__='alarm_levels'
    id= Column(Integer, primary_key=True)
    alarm_severity=Column(SQLEnum(AlarmLevel), nullable=False)

    def __repr__(self):
        return f'<Niveles de severidad de alarma {self.id} >'

class AlarmChannel(Base):
    __tablename__='alarm_channels'
    id= Column(Integer, primary_key=True)
    channel_name=Column(SQLEnum(AlarmChannels), nullable=False)
    def __repr__(self):
        return f'<Canales de notificación {self.id} >'

class AlarmCoolDown(Base):
    __tablename__='alarm_cooldown'
    id= Column(Integer, primary_key=True)
    cooldown_options=Column(Integer, nullable=False)
    def __repr__(self):
        return f'<Tiempo cooldown opcion {self.id} >'

class AlarmNewTime(Base):
    __tablename__='alarm_new_event_time'
    id= Column(Integer, primary_key=True)
    new_event_time=Column(Integer, nullable=False)
    def __repr__(self):
        return f'<Tiempo para considerar nuevo evento {self.id} >'

class AlarmRule(Base): #Modelo para reglas de alarma, aplicable a cualquier parametro
    __tablename__='alarm_rules'
    
    id = Column(Integer, primary_key=True)
    meter_id = Column(Integer, ForeignKey('meters.id'))
    parameter = Column(Integer, ForeignKey('parameters_pvm3.id'))
    threshold = Column(Double, nullable=False)
    comparator = Column(SQLEnum(Comparators), nullable=False)
    level = Column(Integer, ForeignKey('alarm_levels.id'))
    comment=Column(String(40),nullable=False)
    
    def __repr__(self):
        return f'<AlarmRule {self.id}: {self.parameter} {self.comparator} {self.threshold}>'
    
class AlarmEvent(Base): #Modelo para registrar eventos de alarmas
    __tablename__='alarm_events'
    id= Column(Integer, primary_key=True)
    measure_id=Column(Integer , ForeignKey('measurements.id'),nullable = False )
    rule_id=Column(Integer , ForeignKey('alarm_rules.id'),nullable = False )
    def __repr__(self):
        return f'<Alarma generada en: {self.measure_id} >'

class AlarmNotifConf(Base):
    __tablename__='alarm_config'
    id= Column(Integer, primary_key=True)
    meter_id=Column(Integer , ForeignKey('meters.id'),nullable = False )
    alarm_level=Column(Integer , ForeignKey('alarm_levels.id'),nullable = False )
    alarm_channel=Column(Integer , ForeignKey('alarm_channels.id'),nullable = False )
    t_cool_down=Column(Integer , ForeignKey('alarm_cooldown.id'),nullable = False )
    t_new_event=Column(Integer , ForeignKey('alarm_new_event_time.id'),nullable = False )
    def __repr__(self):
        return f'<Configuracion de notifiaciones para: {self.meter_id} >'

class AlarmNotif(Base):
    __tablename__='alarm_notif'
    id= Column(Integer, primary_key=True)
    rule_id=Column(Integer , ForeignKey('alarm_rules.id'),nullable = False )
    first_trigger=Column(Integer , ForeignKey('measurements.id'),nullable = False )
    last_trigger=Column(Integer , ForeignKey('measurements.id'),nullable = False )
    last_notif=Column(Integer , ForeignKey('measurements.id'),nullable = False )
    event_counter=Column(Integer,nullable = False)
    def __repr__(self):
        return f'<Notificaciones para: {self.rule_id} >'
