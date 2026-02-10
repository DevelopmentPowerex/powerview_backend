

TEMP_GEN_GRAPHS_PATH=r"C:\Users\jeras\Documents\PowerView\backend_pv\OnDemand\report_generator\temp\gen_graphs"
GRAPH_PATH=r'\temp\gen_graphs'

PREMADE_ORDERS={
    "V_all_1":(['vA','vB','vC'],'chart_voltage_PN'),
    "V_all_2":(['vAB','vBC','vCA'],'chart_voltage_PP'),
    "I_all":(['iA','iB','iC'],'chart_current'),
    "P_all":(['PA','PB','PC','P'],'chart_active_power'),
    "Q_all":(['QA','QB','QC','Q'],'chart_reactive_power'),
    "S_all":(['SA','SB','SC','S'],'chart_aparent_power'),
    "Wh_all_p":(["P_kWh_A","P_kWh_B","P_kWh_C","P_kWh_T"],'chart_active_positive_energy'),
    "Wh_all_r":(["R_kWh_A","R_kWh_B","R_kWh_C","R_kWh_T"],'chart_active_reverse_energy'),
    "varh_all_p":(["P_kvarh_A","P_kvarh_B","P_kvarh_C","P_kvarh_T"],'chart_reactive_positive_energy'),
    "varh_all_r":(["R_kvarh_A","R_kvarh_B","R_kvarh_C","R_kvarh_T"],'chart_reactive_reverse_energy'),
    'F':(['F'],'chart_frequency'),
    'PF':(['PF'],'chart_power_factor')
}

PARAMETERS_FILTER=[# Parametros que se deben eliminar de la extracción por falta de uso
    "Signal_strength", #Frecuencia e intensidad de señal de transmisión
    "P_Active_demand", ##Demanda de potencia activa positiva actual
    "ICCID", #identificador único de placa
    "PT", #Valor de transformador de potencia del medidor
    "CT", #Valor de transformador de corriente del medidor (relación de transformación)
    "R_Active_demand", #Demanda de potencia activa inversa actual
    "P_Reactive_demand", #Demanda de potencia reactiva positiva actual
    "R_Reactive_demand", #Demanda de potencia reactiva inversa actual
    "kWh_spike", #Energía total activa en "periodo spike"
    "kWh_peak", #Energía total activa en "periodo peak"
    "kWh_flat", #Energía total activa en "periodo flat"
    "kWh_valley", #Energía total activa en "periodo valley"
    "C1_kvarh", #Energía reactiva en 1er cuadrante
    "C2_kvarh", #Energía reactiva en 2do cuadrante
    "C3_kvarh", #Energía reactiva en 3er cuadrante
    "C4_kvarh", #Energía reactiva en 4to cuadrante 
    "TA","TB","TC","TN"
] 

PARAMETERS_FOR_REPORT={
    "V_all_1":('V','VOLTAJES FASE NEUTRO [V]'),
    "vA":('V','Voltaje entre Fase A  y Neutro [vA]'),
    "vB":('V','Voltaje entre Fase B  y Neutro [vB]'),
    "vC":('V','Voltaje entre Fase C  y Neutro [vC]'),

    "V_all_2":('V','VOLTAJES FASE FASE [V]'),
    "vAB":('V','Voltaje entre Fases  A y B [vAB]'),
    "vBC":('V','Voltaje entre Fases  B y C [vBC]'),
    "vCA":('V','Voltaje entre Fases  C y A [vCA]'),

    "I_all":('A','CORRIENTES POR FASE [A]'),
    "iA":('A','Corriente en Fase A [iA]'),
    "iB":('A','Corriente en Fase B [iB]'),
    "iC":('A','Corriente en Fase C [iC]'), 

    "P_all":('kW','POTENCIA ACTIVA POR FASE [kW]'),
    "PA":('kW','Potencia Activa en Fase A [PA]'),
    "PB":('kW','Potencia Activa en Fase B [PB]'), 
    "PC":('kW','Potencia Activa en Fase C [PC]'),
    "P":('kW','Potencia Activa Total [P]'),

    "Q_all":('kVAR','POTENCIA REACTIVA POR FASE [kVAR]'),
    "QA":('kVAR','Potencia Reactiva en Fase A [QA]'), 
    "QB":('kVAR','Potencia Reactiva en Fase B [QB]'),
    "QC":('kVAR','Potencia Reactiva en Fase C [QC]'),
    "Q":('kVAR','Potencia Reactiva Total [Q]'),

    "S_all":('kVA','POTENCIA APARENTE POR FASE [kVA]'),
    "SA":('kVA','Potencia Aparente en Fase A [SA]'),
    "SB":('kVA','Potencia Aparente en Fase B [SB]'), 
    "SC":('kVA','Potencia Aparente en Fase C [SC]'), 
    "S" :('kVA','Potencia Aparente Total [S]'),

    "Wh_all_p":('kWh','ENERGIA ACTIVA POSITIVA POR FASE [kWh]'),
    "P_kWh_A":('kWh','Energía activa en Fase A: Positiva'),
    "P_kWh_B":('kWh','Energía activa en Fase B: Positiva'),
    "P_kWh_C":('kWh','Energía activa en Fase C: Positiva'),
    "P_kWh_T":('kWh','Energía Activa Positiva Total') ,

    "Wh_all_r":('kWh','ENERGIA ACTIVA INVERSA POR FASE [kWh]'),
    "R_kWh_A":('kWh','Energía activa en Fase A: Inversa'),
    "R_kWh_B":('kWh','Energía activa en Fase B: Inversa'),
    "R_kWh_C":('kWh','Energía activa en Fase C: Inversa'),
    "R_kWh_T":('kWh','Energía Activa Inversa Total'),

    "varh_all_p":('kVarh','ENERGIA REACTIVA POSITIVA POR FASE [kVarh]'),
    "P_kvarh_A":('kVarh','Energía reactiva en Fase A: Positiva'),
    "P_kvarh_B":('kVarh','Energía reactiva en Fase B: Positiva'),
    "P_kvarh_C":('kVarh','Energía reactiva en Fase C: Positiva'),
    "P_kvarh_T":('kVarh','Energía Reactiva Positiva Total'),

    "varh_all_r":('kVarh','ENERGIA REACTIVA INVERSA POR FASE [kVarh]'),
    "R_kvarh_A":('kVarh','Energía reactiva en Fase A: Inversa'),
    "R_kvarh_B":('kVarh','Energía reactiva en Fase B: Inversa'),
    "R_kvarh_C":('kVarh','Energía reactiva en Fase C: Inversa'),
    "R_kvarh_T":('kVarh','Energía Reactiva Inversa Total'),

    "PF":('','Factor de Potencia'),
    "F":('Hz','Frecuencia [Hz]'), 
    "iF":('A','Corriente de Fuga [A]'),
 
}

DATOS_PRUEBA=[
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.82, 'QA': -0.52, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 17.09, 'iC': 6.34, 'iF': 0, 'vA': 122.6, 'vB': 120.1, 'vC': 128.7, 'PFA': 0.454, 'PFB': 0.954, 'PFC': 0.44, 'vAB': 210.1, 'vBC': 215.5, 'vCA': 217.6, 'I_unb': 124.28, 'THD_A': 6.12, 'THD_B': 4.58, 'THD_C': 4.51, 'V_unb': 6.78, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:49:42'}, 
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.88, 'PC': 0.32, 'PF': 0.819, 'QA': -0.52, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 16.82, 'iC': 6.4, 'iF': 0, 'vA': 122.3, 'vB': 120.3, 'vC': 129.4, 'PFA': 0.457, 'PFB': 0.953, 'PFC': 0.47, 'vAB': 210.1, 'vBC': 216.2, 'vCA': 218, 'I_unb': 124.28, 'THD_A': 6.06, 'THD_B': 4.65, 'THD_C': 4.71, 'V_unb': 7.49, 'THDC_A': 50, 'THDC_B': 12.19, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:50:42'}, 
        {'meter_id': 1, 'parameters': {'F': 59.97, 'P': 4.72, 'Q': -0.88, 'S': 4.8, 'PA': 0.24, 'PB': 2.88, 'PC': 1.56, 'PF': 0.98, 'QA': -0.52, 'QB': -0.6, 'QC': 0.16, 'SA': 0.56, 'SB': 2.96, 'SC': 1.56, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.46, 'iB': 25.18, 'iC': 13.19, 'iF': 0, 'vA': 123.4, 'vB': 118.1, 'vC': 124, 'PFA': 0.438, 'PFB': 0.979, 'PFC': 0.993, 'vAB': 209.1, 'vBC': 209.6, 'vCA': 214.2, 'I_unb': 136.11, 'THD_A': 5.84, 'THD_B': 4.32, 'THD_C': 3.87, 'V_unb': 5.34, 'THDC_A': 54.54, 'THDC_B': 8.06, 'THDC_C': 21.87, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:51:42'}, 
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.48, 'Q': -1.68, 'S': 2.96, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.82, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 17.05, 'iC': 6.34, 'iF': 0, 'vA': 120.7, 'vB': 119.2, 'vC': 129.2, 'PFA': 0.469, 'PFB': 0.954, 'PFC': 0.431, 'vAB': 207.7, 'vBC': 215.1, 'vCA': 216.4, 'I_unb': 124.28, 'THD_A': 6.05, 'THD_B': 4.53, 'THD_C': 4.64, 'V_unb': 7.88, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:52:42'}, 
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.82, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 17.09, 'iC': 6.34, 'iF': 0, 'vA': 121.6, 'vB': 119.9, 'vC': 129.3, 'PFA': 0.46, 'PFB': 0.954, 'PFC': 0.431, 'vAB': 209.1, 'vBC': 215.8, 'vCA': 217.3, 'I_unb': 126.76, 'THD_A': 5.85, 'THD_B': 4.59, 'THD_C': 4.64, 'V_unb': 7.53, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:53:42'}, 
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.818, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 17.01, 'iC': 6.32, 'iF': 0, 'vA': 121.3, 'vB': 120, 'vC': 130, 'PFA': 0.463, 'PFB': 0.954, 'PFC': 0.424, 'vAB': 208.9, 'vBC': 216.5, 'vCA': 217.6, 'I_unb': 124.28, 'THD_A': 5.94, 'THD_B': 4.59, 'THD_C': 4.84, 'V_unb': 8, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:54:42'}, 
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.821, 'QA': -0.52, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 17.21, 'iC': 6.33, 'iF': 0, 'vA': 121.8, 'vB': 119.9, 'vC': 129.3, 'PFA': 0.459, 'PFB': 0.955, 'PFC': 0.431, 'vAB': 209.3, 'vBC': 215.8, 'vCA': 217.4, 'I_unb': 124.28, 'THD_A': 6.08, 'THD_B': 4.34, 'THD_C': 4.72, 'V_unb': 8.79, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:55:42'},
        {'meter_id': 1, 'parameters': {'F': 60.01, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.32, 'PF': 0.824, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.72, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.55, 'iB': 17.18, 'iC': 6.46, 'iF': 0, 'vA': 121.4, 'vB': 119.1, 'vC': 129.8, 'PFA': 0.467, 'PFB': 0.955, 'PFC': 0.475, 'vAB': 208.2, 'vBC': 215.6, 'vCA': 217.5, 'I_unb': 122.53, 'THD_A': 6.1, 'THD_B': 4.62, 'THD_C': 4.7, 'V_unb': 8.58, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:56:42'},
        {'meter_id': 1, 'parameters': {'F': 59.97, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.823, 'QA': -0.52, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 17.36, 'iC': 6.32, 'iF': 0, 'vA': 122.4, 'vB': 119.3, 'vC': 129.3, 'PFA': 0.456, 'PFB': 0.956, 'PFC': 0.427, 'vAB': 209.3, 'vBC': 215.3, 'vCA': 218, 'I_unb': 126.76, 'THD_A': 6.05, 'THD_B': 4.61, 'THD_C': 4.79, 'V_unb': 8.63, 'THDC_A': 50, 'THDC_B': 11.62, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.4}, 'timestamp': '2025-08-25T10:57:42'},
        {'meter_id': 1, 'parameters': {'F': 59.99, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.82, 'QA': -0.52, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 17.27, 'iC': 6.31, 'iF': 0, 'vA': 122.6, 'vB': 119.3, 'vC': 129.8, 'PFA': 0.448, 'PFB': 0.956, 'PFC': 0.423, 'vAB': 209.4, 'vBC': 215.7, 'vCA': 218.6, 'I_unb': 126.76, 'THD_A': 6.12, 'THD_B': 4.53, 'THD_C': 4.54, 'V_unb': 8.64, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T10:58:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.822, 'QA': -0.52, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.54, 'iB': 17.36, 'iC': 6.34, 'iF': 0, 'vA': 122.4, 'vB': 119.7, 'vC': 130, 'PFA': 0.455, 'PFB': 0.956, 'PFC': 0.424, 'vAB': 209.6, 'vBC': 216.3, 'vCA': 218.6, 'I_unb': 150, 'THD_A': 6.3, 'THD_B': 3.34, 'THD_C': 4.92, 'V_unb': 11.08, 'THDC_A': 50, 'THDC_B': 13.95, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.4, 'P_kWh_C': 335.2, 'P_kWh_T': 1086.8, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T10:59:42'},
        {'meter_id': 1, 'parameters': {'F': 59.97, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.819, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 17.16, 'iC': 6.31, 'iF': 0, 'vA': 121.7, 'vB': 119.1, 'vC': 130.5, 'PFA': 0.461, 'PFB': 0.956, 'PFC': 0.416, 'vAB': 208.5, 'vBC': 216.2, 'vCA': 218.4, 'I_unb': 124.28, 'THD_A': 6.17, 'THD_B': 4.36, 'THD_C': 4.68, 'V_unb': 9.36, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:00:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.821, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 17.25, 'iC': 6.31, 'iF': 0, 'vA': 121.1, 'vB': 118.9, 'vC': 130.9, 'PFA': 0.472, 'PFB': 0.956, 'PFC': 0.418, 'vAB': 207.8, 'vBC': 216.4, 'vCA': 218.2, 'I_unb': 124.28, 'THD_A': 6.03, 'THD_B': 4.46, 'THD_C': 4.58, 'V_unb': 9.7, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:01:42'},
        {'meter_id': 1, 'parameters': {'F': 59.97, 'P': 3.84, 'Q': -0.88, 'S': 3.92, 'PA': 0.24, 'PB': 1.96, 'PC': 1.6, 'PF': 0.97, 'QA': -0.48, 'QB': -0.6, 'QC': 0.16, 'SA': 0.56, 'SB': 2.08, 'SC': 1.6, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.45, 'iB': 17.22, 'iC': 13.31, 'iF': 0, 'vA': 122, 'vB': 122, 'vC': 123.7, 'PFA': 0.459, 'PFB': 0.954, 'PFC': 0.993, 'vAB': 211.3, 'vBC': 212.7, 'vCA': 212.7, 'I_unb': 98.86, 'THD_A': 5.82, 'THD_B': 4.18, 'THD_C': 4.2, 'V_unb': 0.81, 'THDC_A': 54.54, 'THDC_B': 11.9, 'THDC_C': 18.75, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:02:42'},
        {'meter_id': 1, 'parameters': {'F': 59.99, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.821, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.51, 'iB': 17.26, 'iC': 6.32, 'iF': 0, 'vA': 121.1, 'vB': 119.2, 'vC': 130.9, 'PFA': 0.467, 'PFB': 0.956, 'PFC': 0.416, 'vAB': 208.1, 'vBC': 216.6, 'vCA': 218.2, 'I_unb': 126.76, 'THD_A': 6.03, 'THD_B': 4.28, 'THD_C': 4.51, 'V_unb': 9.38, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:03:42'},
        {'meter_id': 1, 'parameters': {'F': 59.99, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.821, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.49, 'iB': 17.15, 'iC': 6.33, 'iF': 0, 'vA': 120.1, 'vB': 119.4, 'vC': 130.3, 'PFA': 0.474, 'PFB': 0.955, 'PFC': 0.422, 'vAB': 207.4, 'vBC': 216.3, 'vCA': 216.9, 'I_unb': 126.76, 'THD_A': 5.92, 'THD_B': 4.19, 'THD_C': 4.45, 'V_unb': 9.1, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:04:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.4, 'Q': -1.68, 'S': 2.96, 'PA': 0.24, 'PB': 1.88, 'PC': 0.28, 'PF': 0.819, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 17, 'iC': 6.27, 'iF': 0, 'vA': 119.8, 'vB': 119, 'vC': 130.5, 'PFA': 0.473, 'PFB': 0.955, 'PFC': 0.413, 'vAB': 206.8, 'vBC': 216.1, 'vCA': 216.8, 'I_unb': 126.76, 'THD_A': 5.93, 'THD_B': 4.2, 'THD_C': 4.52, 'V_unb': 9.51, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:05:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.68, 'S': 2.96, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.817, 'QA': -0.48, 'QB': -0.56, 'QC': -0.64, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.51, 'iB': 17.02, 'iC': 6.3, 'iF': 0, 'vA': 120.3, 'vB': 119.2, 'vC': 131.5, 'PFA': 0.473, 'PFB': 0.955, 'PFC': 0.408, 'vAB': 207.4, 'vBC': 217.1, 'vCA': 218.1, 'I_unb': 124.28, 'THD_A': 5.99, 'THD_B': 4.19, 'THD_C': 4.64, 'V_unb': 9.94, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:06:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 3.76, 'Q': -0.88, 'S': 3.84, 'PA': 0.24, 'PB': 1.92, 'PC': 1.56, 'PF': 0.97, 'QA': -0.48, 'QB': -0.6, 'QC': 0.16, 'SA': 0.56, 'SB': 2.04, 'SC': 1.6, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.47, 'iB': 16.8, 'iC': 13.16, 'iF': 0, 'vA': 121.5, 'vB': 122.5, 'vC': 124.5, 'PFA': 0.465, 'PFB': 0.951, 'PFC': 0.992, 'vAB': 211.3, 'vBC': 213.9, 'vCA': 213, 'I_unb': 100, 'THD_A': 5.68, 'THD_B': 4, 'THD_C': 4.18, 'V_unb': 1.54, 'THDC_A': 54.54, 'THDC_B': 12.19, 'THDC_C': 21.87, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:07:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.88, 'PC': 0.28, 'PF': 0.82, 'QA': -0.48, 'QB': -0.56, 'QC': -0.64, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.5, 'iB': 16.95, 'iC': 6.35, 'iF': 0, 'vA': 119.5, 'vB': 119.4, 'vC': 131.6, 'PFA': 0.48, 'PFB': 0.954, 'PFC': 0.432, 'vAB': 206.8, 'vBC': 217.4, 'vCA': 217.5, 'I_unb': 124.28, 'THD_A': 5.95, 'THD_B': 4.19, 'THD_C': 4.64, 'V_unb': 9.88, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.2, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:08:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.28, 'PB': 1.92, 'PC': 0.28, 'PF': 0.819, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.5, 'iB': 16.85, 'iC': 6.31, 'iF': 0, 'vA': 119.6, 'vB': 120.9, 'vC': 131.1, 'PFA': 0.488, 'PFB': 0.953, 'PFC': 0.416, 'vAB': 208.2, 'vBC': 218.2, 'vCA': 217.1, 'I_unb': 121.73, 'THD_A': 6.03, 'THD_B': 4.47, 'THD_C': 4.5, 'V_unb': 9.35, 'THDC_A': 50, 'THDC_B': 12.19, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:09:42'},
        {'meter_id': 1, 'parameters': {'F': 59.95, 'P': 3.36, 'Q': -1.68, 'S': 3.76, 'PA': 0.24, 'PB': 2.84, 'PC': 0.28, 'PF': 0.891, 'QA': -0.48, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2.88, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 25.35, 'iC': 6.28, 'iF': 0, 'vA': 121.8, 'vB': 115.2, 'vC': 130.2, 'PFA': 0.46, 'PFB': 0.98, 'PFC': 0.414, 'vAB': 205.2, 'vBC': 212.6, 'vCA': 218.2, 'I_unb': 164.83, 'THD_A': 5.92, 'THD_B': 4.25, 'THD_C': 3.99, 'V_unb': 12.17, 'THDC_A': 50, 'THDC_B': 6.34, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:10:42'},
        {'meter_id': 1, 'parameters': {'F': 59.95, 'P': 3.76, 'Q': -0.88, 'S': 3.84, 'PA': 0.24, 'PB': 1.92, 'PC': 1.56, 'PF': 0.97, 'QA': -0.48, 'QB': -0.6, 'QC': 0.16, 'SA': 0.56, 'SB': 2.04, 'SC': 1.56, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.46, 'iB': 16.85, 'iC': 13.19, 'iF': 0, 'vA': 121.5, 'vB': 122.4, 'vC': 123.9, 'PFA': 0.467, 'PFB': 0.952, 'PFC': 0.993, 'vAB': 211.2, 'vBC': 213.3, 'vCA': 212.5, 'I_unb': 100, 'THD_A': 5.85, 'THD_B': 4.25, 'THD_C': 3.79, 'V_unb': 2.03, 'THDC_A': 54.54, 'THDC_B': 12.19, 'THDC_C': 21.87, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:11:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.819, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.5, 'iB': 17.1, 'iC': 6.25, 'iF': 0, 'vA': 121.2, 'vB': 119.5, 'vC': 129.8, 'PFA': 0.462, 'PFB': 0.955, 'PFC': 0.42, 'vAB': 208.4, 'vBC': 215.9, 'vCA': 217.4, 'I_unb': 124.28, 'THD_A': 6.36, 'THD_B': 4.35, 'THD_C': 4.47, 'V_unb': 8.1, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134, 'R_kvarh_C': 142.4, 'R_kvarh_T': 510.8}, 'timestamp': '2025-08-25T11:12:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.819, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 16.89, 'iC': 6.33, 'iF': 0, 'vA': 121, 'vB': 120.6, 'vC': 129.4, 'PFA': 0.468, 'PFB': 0.953, 'PFC': 0.43, 'vAB': 209.2, 'vBC': 216.5, 'vCA': 216.8, 'I_unb': 124.28, 'THD_A': 6.21, 'THD_B': 4.48, 'THD_C': 4.56, 'V_unb': 7.1, 'THDC_A': 50, 'THDC_B': 12.19, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:13:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.76, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.82, 'QA': -0.48, 'QB': -0.6, 'QC': -0.64, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.52, 'iB': 17, 'iC': 6.36, 'iF': 0, 'vA': 121, 'vB': 120.6, 'vC': 131.4, 'PFA': 0.47, 'PFB': 0.954, 'PFC': 0.435, 'vAB': 209.2, 'vBC': 218.3, 'vCA': 218.6, 'I_unb': 124.28, 'THD_A': 5.79, 'THD_B': 4.4, 'THD_C': 4.8, 'V_unb': 9.09, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:14:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 3.36, 'Q': -1.68, 'S': 3.76, 'PA': 0.24, 'PB': 2.8, 'PC': 0.28, 'PF': 0.891, 'QA': -0.48, 'QB': -0.56, 'QC': -0.64, 'SA': 0.56, 'SB': 2.88, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 25.28, 'iC': 6.38, 'iF': 0, 'vA': 120.8, 'vB': 115, 'vC': 131, 'PFA': 0.464, 'PFB': 0.98, 'PFC': 0.411, 'vAB': 204.2, 'vBC': 213.1, 'vCA': 218.1, 'I_unb': 164.83, 'THD_A': 6.05, 'THD_B': 4.35, 'THD_C': 4.2, 'V_unb': 12.27, 'THDC_A': 50, 'THDC_B': 7.93, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:15:42'},
        {'meter_id': 1, 'parameters': {'F': 59.97, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.82, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 16.96, 'iC': 6.31, 'iF': 0, 'vA': 120.3, 'vB': 120.8, 'vC': 129.1, 'PFA': 0.469, 'PFB': 0.953, 'PFC': 0.43, 'vAB': 208.7, 'vBC': 216.4, 'vCA': 216, 'I_unb': 124.28, 'THD_A': 6, 'THD_B': 4.47, 'THD_C': 4.57, 'V_unb': 7.13, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 408.8, 'P_kWh_C': 335.2, 'P_kWh_T': 1087.6, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:16:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.76, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.822, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 17.26, 'iC': 6.35, 'iF': 0, 'vA': 121.1, 'vB': 121, 'vC': 130, 'PFA': 0.463, 'PFB': 0.954, 'PFC': 0.427, 'vAB': 209.6, 'vBC': 217.4, 'vCA': 217.5, 'I_unb': 126.76, 'THD_A': 5.87, 'THD_B': 4.38, 'THD_C': 4.54, 'V_unb': 7.7, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:17:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 3.76, 'Q': -0.96, 'S': 3.92, 'PA': 0.24, 'PB': 2, 'PC': 1.56, 'PF': 0.968, 'QA': -0.48, 'QB': -0.6, 'QC': 0.16, 'SA': 0.56, 'SB': 2.08, 'SC': 1.56, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.5, 'iB': 17.16, 'iC': 13.16, 'iF': 0, 'vA': 122.4, 'vB': 123.2, 'vC': 123, 'PFA': 0.457, 'PFB': 0.953, 'PFC': 0.994, 'vAB': 212.6, 'vBC': 213.2, 'vCA': 212.5, 'I_unb': 101.12, 'THD_A': 5.81, 'THD_B': 4.22, 'THD_C': 3.99, 'V_unb': 0.73, 'THDC_A': 54.54, 'THDC_B': 11.9, 'THDC_C': 21.87, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:18:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.824, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 17.24, 'iC': 6.29, 'iF': 0, 'vA': 121, 'vB': 120.6, 'vC': 129.1, 'PFA': 0.465, 'PFB': 0.955, 'PFC': 0.432, 'vAB': 209.2, 'vBC': 216.2, 'vCA': 216.6, 'I_unb': 124.28, 'THD_A': 5.87, 'THD_B': 4.48, 'THD_C': 4.49, 'V_unb': 6.71, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:19:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.32, 'PF': 0.824, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.51, 'iB': 17.07, 'iC': 6.38, 'iF': 0, 'vA': 121.4, 'vB': 121.5, 'vC': 129.1, 'PFA': 0.465, 'PFB': 0.954, 'PFC': 0.458, 'vAB': 210.3, 'vBC': 217, 'vCA': 216.9, 'I_unb': 124.28, 'THD_A': 5.85, 'THD_B': 4.36, 'THD_C': 4.49, 'V_unb': 6.64, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:20:42'},
        {'meter_id': 1, 'parameters': {'F': 60.01, 'P': 3.76, 'Q': -0.96, 'S': 3.84, 'PA': 0.24, 'PB': 1.96, 'PC': 1.52, 'PF': 0.968, 'QA': -0.48, 'QB': -0.6, 'QC': 0.16, 'SA': 0.56, 'SB': 2.04, 'SC': 1.56, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.44, 'iB': 16.92, 'iC': 13.1, 'iF': 0, 'vA': 121.7, 'vB': 123.3, 'vC': 122.5, 'PFA': 0.457, 'PFB': 0.952, 'PFC': 0.994, 'vAB': 212.1, 'vBC': 212.8, 'vCA': 211.4, 'I_unb': 100, 'THD_A': 5.67, 'THD_B': 4.3, 'THD_C': 3.83, 'V_unb': 1.3, 'THDC_A': 54.54, 'THDC_B': 11.9, 'THDC_C': 22.58, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:21:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 3.76, 'Q': -0.96, 'S': 3.92, 'PA': 0.24, 'PB': 1.96, 'PC': 1.56, 'PF': 0.968, 'QA': -0.48, 'QB': -0.6, 'QC': 0.12, 'SA': 0.56, 'SB': 2.04, 'SC': 1.56, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.46, 'iB': 17, 'iC': 13.23, 'iF': 0, 'vA': 120.7, 'vB': 122.2, 'vC': 122.1, 'PFA': 0.472, 'PFB': 0.953, 'PFC': 0.995, 'vAB': 210.3, 'vBC': 211.5, 'vCA': 210.2, 'I_unb': 100, 'THD_A': 5.56, 'THD_B': 4.25, 'THD_C': 3.93, 'V_unb': 1.15, 'THDC_A': 54.54, 'THDC_B': 9.52, 'THDC_C': 21.87, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:22:42'},
        {'meter_id': 1, 'parameters': {'F': 60.02, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.823, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 17.13, 'iC': 6.32, 'iF': 0, 'vA': 120.2, 'vB': 120.6, 'vC': 129.2, 'PFA': 0.474, 'PFB': 0.954, 'PFC': 0.427, 'vAB': 208.5, 'vBC': 216.3, 'vCA': 216, 'I_unb': 124.28, 'THD_A': 5.67, 'THD_B': 4.23, 'THD_C': 4.49, 'V_unb': 7.75, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:23:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.826, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 17.24, 'iC': 6.3, 'iF': 0, 'vA': 119.9, 'vB': 121.1, 'vC': 128.8, 'PFA': 0.477, 'PFB': 0.955, 'PFC': 0.43, 'vAB': 208.7, 'vBC': 216.4, 'vCA': 215.4, 'I_unb': 126.76, 'THD_A': 5.84, 'THD_B': 4.29, 'THD_C': 4.35, 'V_unb': 7.14, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.2, 'P_kWh_C': 335.6, 'P_kWh_T': 1088, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:24:42'},
        {'meter_id': 1, 'parameters': {'F': 59.95, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.827, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 17.23, 'iC': 6.27, 'iF': 0, 'vA': 119.8, 'vB': 121.3, 'vC': 128.5, 'PFA': 0.48, 'PFB': 0.955, 'PFC': 0.435, 'vAB': 208.8, 'vBC': 216.3, 'vCA': 215, 'I_unb': 124.28, 'THD_A': 5.76, 'THD_B': 4.29, 'THD_C': 4.28, 'V_unb': 6.82, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.6, 'P_kWh_C': 335.6, 'P_kWh_T': 1088.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:25:42'},
        {'meter_id': 1, 'parameters': {'F': 60.01, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.92, 'PC': 0.28, 'PF': 0.826, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.49, 'iB': 17.1, 'iC': 6.32, 'iF': 0, 'vA': 119.7, 'vB': 121.2, 'vC': 128.4, 'PFA': 0.477, 'PFB': 0.954, 'PFC': 0.451, 'vAB': 208.6, 'vBC': 216.1, 'vCA': 214.9, 'I_unb': 124.28, 'THD_A': 5.85, 'THD_B': 4.46, 'THD_C': 4.36, 'V_unb': 7.23, 'THDC_A': 50, 'THDC_B': 9.52, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.6, 'P_kWh_C': 335.6, 'P_kWh_T': 1088.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.4, 'R_kvarh_T': 511.2}, 'timestamp': '2025-08-25T11:26:42'},
        {'meter_id': 1, 'parameters': {'F': 59.96, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.827, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.64, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.48, 'iB': 17.21, 'iC': 6.25, 'iF': 0, 'vA': 119.5, 'vB': 121.1, 'vC': 127.5, 'PFA': 0.48, 'PFB': 0.955, 'PFC': 0.436, 'vAB': 208.3, 'vBC': 215.3, 'vCA': 213.9, 'I_unb': 124.28, 'THD_A': 5.86, 'THD_B': 4.38, 'THD_C': 4.23, 'V_unb': 6.53, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.6, 'P_kWh_C': 335.6, 'P_kWh_T': 1088.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.8, 'R_kvarh_T': 511.6}, 'timestamp': '2025-08-25T11:27:42'},
        {'meter_id': 1, 'parameters': {'F': 60, 'P': 2.56, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.828, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.5, 'iB': 17.27, 'iC': 6.29, 'iF': 0, 'vA': 120.2, 'vB': 121.2, 'vC': 128.6, 'PFA': 0.48, 'PFB': 0.956, 'PFC': 0.437, 'vAB': 209, 'vBC': 216.3, 'vCA': 215.5, 'I_unb': 124.28, 'THD_A': 6, 'THD_B': 4.45, 'THD_C': 4.28, 'V_unb': 6.64, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.6, 'P_kWh_C': 335.6, 'P_kWh_T': 1088.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.8, 'R_kvarh_T': 511.6}, 'timestamp': '2025-08-25T11:28:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 3.44, 'Q': -1.68, 'S': 3.84, 'PA': 0.24, 'PB': 2.92, 'PC': 0.28, 'PF': 0.894, 'QA': -0.52, 'QB': -0.56, 'QC': -0.6, 'SA': 0.56, 'SB': 2.96, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.5, 'iB': 25.79, 'iC': 6.3, 'iF': 0, 'vA': 122.5, 'vB': 115.9, 'vC': 130.4, 'PFA': 0.449, 'PFB': 0.98, 'PFC': 0.412, 'vAB': 206.4, 'vBC': 213.4, 'vCA': 219, 'I_unb': 166.3, 'THD_A': 6.13, 'THD_B': 4.4, 'THD_C': 4.37, 'V_unb': 11.62, 'THDC_A': 50, 'THDC_B': 6.25, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.6, 'P_kWh_C': 335.6, 'P_kWh_T': 1088.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.8, 'R_kvarh_T': 511.6}, 'timestamp': '2025-08-25T11:29:42'},
        {'meter_id': 1, 'parameters': {'F': 59.98, 'P': 2.48, 'Q': -1.68, 'S': 3.04, 'PA': 0.24, 'PB': 1.96, 'PC': 0.28, 'PF': 0.824, 'QA': -0.48, 'QB': -0.6, 'QC': -0.6, 'SA': 0.56, 'SB': 2.04, 'SC': 0.68, 'TA': 0, 'TB': 0, 'TC': 0, 'TN': 0, 'iA': 5.53, 'iB': 17.15, 'iC': 6.28, 'iF': 0, 'vA': 121.2, 'vB': 121, 'vC': 128.9, 'PFA': 0.474, 'PFB': 0.955, 'PFC': 0.432, 'vAB': 209.7, 'vBC': 216.4, 'vCA': 216.6, 'I_unb': 124.28, 'THD_A': 6.11, 'THD_B': 4.46, 'THD_C': 4.34, 'V_unb': 6.38, 'THDC_A': 50, 'THDC_B': 11.9, 'THDC_C': 61.53, 'P_kWh_A': 17.6, 'P_kWh_B': 409.6, 'P_kWh_C': 335.6, 'P_kWh_T': 1088.4, 'R_kWh_A': 0, 'R_kWh_B': 0, 'R_kWh_C': 0, 'R_kWh_T': 0, 'DI_status': 0, 'P_kvarh_A': 4.4, 'P_kvarh_B': 1.6, 'P_kvarh_C': 2.4, 'P_kvarh_T': 26.8, 'R_kvarh_A': 88, 'R_kvarh_B': 134.4, 'R_kvarh_C': 142.8, 'R_kvarh_T': 511.6}, 'timestamp': '2025-08-25T11:30:42'},
]  

M3_MAPPING={ # Mapeo de constantes de mensaje PV-M3
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

PARAMETER_TRANSLATION={
    "vA":('V','Voltaje entre Fase A  y Neutro [vA]'),
    "vB":('V','Voltaje entre Fase B  y Neutro [vB]'),
    "vC":('V','Voltaje entre Fase C  y Neutro [vC]'),
    "vAB":('V','Voltaje entre Fases  A y B [vAB]'),
    "vBC":('V','Voltaje entre Fases  B y C [vBC]'),
    "vCA":('V','Voltaje entre Fases  C y A [vCA]'),
    "iA":('A','Corriente en Fase A [iA]'),
    "iB":('A','Corriente en Fase B [iB]'),
    "iC":('A','Corriente en Fase C [iC]'), 
    "PA":('W','Potencia Activa en Fase A [PA]'),
    "PB":('W','Potencia Activa en Fase B [PB]'), 
    "PC":('W','Potencia Activa en Fase C [PC]'),
    "P":('W','Potencia Activa Total [P]'),
    "QA":('VAR','Potencia Reactiva en Fase A [QA]'), 
    "QB":('VAR','Potencia Reactiva en Fase B [QB]'),
    "QC":('VAR','Potencia Reactiva en Fase C [QC]'),
    "Q":('VAR','Potencia Reactiva Total [Q]'),
    "SA":('VA','Potencia Aparente en Fase A [SA]'),
    "SB":('VA','Potencia Aparente en Fase B [SB]'), 
    "SC":('VA','Potencia Aparente en Fase C [SC]'), 
    "S" :('VA','Potencia Aparente Total [S]'),
    "PFA":('','Factor de Potencia en Fase A [PFA]'),
    "PFB":('','Factor de Potencia en Fase B [PFB]'),
    "PFC":('','Factor de Potencia en Fase C [PFC]'),
    "PF":('','Factor de Potencia General [PF]'),
    "F":('Hz','Frecuencia [F]'), 
    "TA":('°C','Temperatura en Fase A [TA]'),
    "TB":('°C','Temperatura en Fase B [TB]'), 
    "TC":('°C','Temperatura en Fase C [TC]'), 
    "TN":('°C','Temperatura en Neutro [N]'),
    "iF":('A','Corriente de Fuga [iF]'),
    "V_unb":('%','Porcentaje de Desbalance de Voltaje'),
    "I_unb":('%','Porcentaje de Desbalance de Corriente'),
    "P_kWh_T":('kWh','Energía Activa Positiva Total') ,
    "R_kWh_T":('kWh','Energía Activa Inversa Total'),
    "P_kvarh_T":('kVarh','Energía Reactiva Positiva Total'),
    "R_kvarh_T":('kVarh','Energía Reactiva Inversa Total'),
    "DI_status":('bit','Estado de las entradas digitales'), #(bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    "P_kWh_A":('kWh','Energía activa en A: Positiva'),
    "R_kWh_A":('kWh','Energía activa en A: Inversa'),
    "P_kvarh_A":('kVarh','Energía reactiva en A: Positiva'),
    "R_kvarh_A":('kVarh','Energía reactiva en A: Inversa'),
    "P_kWh_B":('kWh','Energía activa en B: Positiva'),
    "R_kWh_B":('kWh','Energía activa en B: Inversa'),
    "P_kvarh_B":('kVarh','Energía reactiva en B: Positiva'),
    "R_kvarh_B":('kVarh','Energía reactiva en B: Inversa'),
    "P_kWh_C":('kWh','Energía activa en C: Positiva'),
    "R_kWh_C":('kWh','Energía activa en C: Inversa'),
    "P_kvarh_C":('kVarh','Energía reactiva en C: Positiva'),
    "R_kvarh_C":('kVarh','Energía reactiva en A: Inversa'),
    "THD_A":('%','Rate de armónicos en A'),
    "THD_B":('%','Rate de armónicos en B'),
    "THD_C":('%','Rate de armónicos en C'),
    "THDC_A":('%','Rate de armónicos de corriente en A'), 
    "THDC_B":('%','Rate de armónicos de corriente en B'), 
    "THDC_C":('%','Rate de armónicos de corriente en C')
}

PARAMETERS_FOR_EVENTS={
    "vA":'Voltaje entre Fase A  y Neutro [V]',
    "vB":'Voltaje entre Fase B  y Neutro [V]',
    "vC":'Voltaje entre Fase C  y Neutro [V]',

    "vAB":'Voltaje entre Fases  A y B [V]',
    "vBC":'Voltaje entre Fases  B y C [V]',
    "vCA":'Voltaje entre Fases  C y A [V]',

    "iA":'Corriente en Fase A [A]',
    "iB":'Corriente en Fase B [A]',
    "iC":'Corriente en Fase C [A]', 

    "PA":'Potencia Activa en Fase A [kW]',
    "PB":'Potencia Activa en Fase B [kW]', 
    "PC":'Potencia Activa en Fase C [kW]',
    "P":'Potencia Activa Total [kW]',

    "QA":'Potencia Reactiva en Fase A [kVar]', 
    "QB":'Potencia Reactiva en Fase B [kVar]',
    "QC":'Potencia Reactiva en Fase C [kVar]',
    "Q":'Potencia Reactiva Total [kVar]',

    "SA":'Potencia Aparente en Fase A [kVA]',
    "SB":'Potencia Aparente en Fase B [kVA]', 
    "SC":'Potencia Aparente en Fase C [kVA]', 
    "S" :'Potencia Aparente Total [kVA]',

    "PF":'Factor de Potencia General',
    "F":'Frecuencia [Hz]', 

    "P_kWh_A":'Energía activa en A: Positiva [kWh]',
    "P_kWh_B":'Energía activa en B: Positiva [kWh]',
    "P_kWh_C":'Energía activa en C: Positiva [kWh]',
    "P_kWh_T":'Energía Activa Positiva Total [kWh]',

    "R_kWh_A":'Energía activa en A: Inversa [kWh]',
    "R_kWh_B":'Energía activa en B: Inversa [kWh]',
    "R_kWh_C":'Energía activa en C: Inversa [kWh]',
    "R_kWh_T":'Energía Activa Inversa Total [kWh]',

    "P_kvarh_A":'Energía reactiva en A: Positiva [kVarh]',
    "P_kvarh_B":'Energía reactiva en B: Positiva [kVarh]',
    "P_kvarh_C":'Energía reactiva en C: Positiva [kVarh]',
    "P_kvarh_T":'Energía Reactiva Positiva Total [kVarh]',

    "R_kvarh_A":'Energía reactiva en A: Inversa [kVarh]',
    "R_kvarh_B":'Energía reactiva en B: Inversa [kVarh]',
    "R_kvarh_C":'Energía reactiva en C: Inversa [kVarh]',
    "R_kvarh_T":'Energía Reactiva Inversa Total [kVarh]',
}

PARAMETERS_CHART_ORDER={
    "Voltajes por línea [V]":"V_all_1",
    "Voltajes por fase [V]":"V_all_2",
    "Corrientes por línea [A]":"I_all",
    "Potencia Activa [W]":"P_all",
    "Potencia Reactiva [VAR]":"Q_all",
    "Potencia Aparente [VA]":"S_all",
    "Frecuencia[Hz]":'F',
    'Factor de Potencia General':'PF',
}

TEMPLATE_DIR = "OnDemand/uS/generate_report/static/templates/"

OUTPUT_HTML = "OnDemand/uS/generate_report/result/editable_report.html"
