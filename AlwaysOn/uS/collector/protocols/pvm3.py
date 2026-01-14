M3_MAPPING={
    0:"serial_number",
    1: "vA", 2: "vB", 3: "vC", #Voltajes de cada línea
    4: "vAB", 5: "vBC", 6: "vCA", #Voltajes de cada fase
    7: "iA", 8: "iB", 9: "iC", #Corrientes de cada línea
    10: "PA", 11: "PB", 12: "PC", 13: "P", #Potencia Activa por línea y total
    14: "QA", 15: "QB", 16: "QC", 17: "Q", #Potencia Reactiva por línea y total
    18: "SA", 19: "SB", 20: "SC", 21: "S" , #Potencia Aparente por línea y total
    22: "PFA",23: "PFB",24: "PFC",25: "PF", #Factor de Potencia por línea y total
    26: "F", 27:"Signal_strength", #Frecuencia e intensidad de señal de transmisión
    28: "P_kWh_T", #Indication value of total positive active energy
    29: "R_kWh_T", #Indication value of total reverse active energy
    30: "P_kvarh_T", #Indication value of total positive reactive energy
    31: "R_kvarh_T", #Indication value of total reverse reactive energy
    32: "P_Active_demand", ##Demanda de potencia activa positiva actual
    33: "ICCID", #identificador único de placa
    34: "PT", #Valor de transformador de potencia del medidor
    35: "CT", #Valor de transformador de corriente del medidor (relación de transformación)
    ##A partir de aquí son las direcciones del segundo mensaje
    36: "TA", 37: "TB", 38: "TC", 39: "TN", #Temperaturas en líneas y neutro
    40: "iF", #Corriente de fuga
    41: "DI_status", #Estado de las entradas digitales (bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    42: "P_kWh_A", 43: "R_kWh_A", #Energía activa en A: Positiva e Inversa/Reversa
    44: "P_kvarh_A", 45: "R_kvarh_A", #Energía reactiva en A: Positiva e Inversa/Reversa
    46: "P_kWh_B", 47: "R_kWh_B", #Energía activa en B: Positiva e Inversa/Reversa
    48: "P_kvarh_B", 49: "R_kvarh_B", #Energía reactiva en B: Positiva e Inversa/Reversa
    50: "P_kWh_C", 51: "R_kWh_C", #Energía activa en C: Positiva e Inversa/Reversa
    52: "P_kvarh_C", 53: "R_kvarh_C", #Energía reactiva en C: Positiva e Inversa/Reversa
    54: "THD_A", 55: "THD_B", 56: "THD_C" , #Rate de harmonicos de voltaje por línea
    57: "THDC_A",58: "THDC_B",59: "THDC_C", #Rate de harmonicos de corriente por línea
    60: "R_Active_demand", #Demanda de potencia activa inversa actual
    61: "P_Reactive_demand", #Demanda de potencia reactiva positiva actual
    62: "R_Reactive_demand", #Demanda de potencia reactiva inversa actual
    63: "V_unb", #Desbalance de voltaje en %
    64: "I_unb", #Desbalance de corriente en %
    65: "kWh_spike", #Energía total activa en "periodo spike"
    66: "kWh_peak", #Energía total activa en "periodo peak"
    67: "kWh_flat", #Energía total activa en "periodo flat"
    68: "kWh_valley", #Energía total activa en "periodo valley"
    69: "C1_kvarh", #Energía reactiva en 1er cuadrante
    70: "C2_kvarh", #Energía reactiva en 2do cuadrante
    71: "C3_kvarh", #Energía reactiva en 3er cuadrante
    72: "C4_kvarh"  #Energía reactiva en 4to cuadrante 
}