from enum import Enum

class UserRole(str,Enum):
    END_USER = "end_user"        # Usuario final
    DISTRIBUTOR = "distributor"  # Distribuidor
    ENGINEER = "engineer"  # Departamento técnico
    ADMIN = "admin"              # Administrador del sistema

class Comparators(str,Enum):
    LESS = '<'
    LESS_EQUAL = '<='
    GREATER = '>'
    GREATER_EQUAL = '>='
    EQUAL = '='
    NOT_EQUAL = '!='

class AlarmLevel(int,Enum): 
    LOW = 1
    MID = 2
    CRITICAL = 3

class AlarmState(str,Enum):
    ACTIVE = "active"
    UNACTIVE = "unactive"
    
class AlarmChannels(int,Enum):
    EMAIL = 1
    SMS = 2
    CALL = 3