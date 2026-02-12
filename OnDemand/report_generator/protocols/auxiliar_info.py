TEMP_GEN_GRAPHS_PATH=r"C:\Users\jeras\Documents\PowerView\backend_pv\OnDemand\report_generator\temp\gen_graphs"

GRAPH_PATH=r'\temp\gen_graphs'

############### HTML RENDER ###################
STATIC_FOLDER=r"OnDemand\report_generator\static"

HTML_TEMPLATES_PATH=r"OnDemand\report_generator\static\templates"

HTML_REPORT_PARTS_TEMPLATES={
    "cover": "cover_template.html",
    "format": "format_template.html",
    "content": "content_template.html",
}

HTML_REPORT_PARTS_RESULT = {
    "cover": r"OnDemand\report_generator\temp\report_parts\html\cover_result.html",
    "format": r"OnDemand\report_generator\temp\report_parts\html\format_result.html",
    "content": r"OnDemand\report_generator\temp\report_parts\html\content_result.html",
}
###############################################

############### PDF RENDER ####################
PDF_RESULT_PATHS={
    'cover':r"OnDemand\report_generator\temp\report_parts\pdf\report_cover.pdf",
    'format':r"OnDemand\report_generator\temp\report_parts\pdf\report_format.pdf",    
    'content':r"OnDemand\report_generator\temp\report_parts\pdf\report_content.pdf",
    'full_content':r"OnDemand\report_generator\temp\report_parts\pdf\report_full_content.pdf",
    'final':r"OnDemand\report_generator\result\report.pdf"
}
###############################################

############### CSV RENDER ####################
CSV_FINAL_PATH=r"OnDemand\report_generator\result\report.xlsx"
###############################################

############### COMPRESS TO ZIP ###############
ZIP_REPORT_PATH=r"OnDemand\report_generator\result\report.zip"
###############################################


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


