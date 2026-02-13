TEMP_GEN_GRAPHS_PATH=r"C:\Users\jeras\Documents\PowerView\backend_pv\OnDemand\report_generator\temp\gen_graphs"

############### HTML RENDER ###################
STATIC_FOLDER="OnDemand/report_generator/static"

HTML_TEMPLATES_PATH="OnDemand/report_generator/static/templates"

HTML_REPORT_PARTS_TEMPLATES={
    "cover": "cover_template.html",
    "format": "format_template.html",
    "content": "content_template.html",
}

HTML_REPORT_PARTS_RESULT = {
    "cover": "OnDemand/report_generator/temp/report_parts/html/cover_result.html",
    "format": "OnDemand/report_generator/temp/report_parts/html/format_result.html",
    "content": "OnDemand/report_generator/temp/report_parts/html/content_result.html",
}
###############################################

############### PDF RENDER ####################
PDF_RESULT_PATHS={
    'cover':"OnDemand/report_generator/temp/report_parts/pdf/report_cover.pdf",
    'format':"OnDemand/report_generator/temp/report_parts/pdf/report_format.pdf",    
    'content':"OnDemand/report_generator/temp/report_parts/pdf/report_content.pdf",
    'full_content':"OnDemand/report_generator/temp/report_parts/pdf/report_full_content.pdf",
    'final':"OnDemand/report_generator/result/report.pdf"
}
###############################################

############### CSV RENDER ####################
CSV_FINAL_PATH="OnDemand/report_generator/result/report.xlsx"
###############################################

############### COMPRESS TO ZIP ###############
ZIP_REPORT_PATH="OnDemand/report_generator/result/report.zip"
###############################################

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
    "TA",
    "TB",
    "TC",
    "TN"
] 

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

PARAMETERS_FOR_REPORT={
    "V_all_1":('V','VOLTAJES FASE NEUTRO [V]'),
    "vA":('V','Voltaje entre Fase A  y Neutro [vA]','A'),
    "vB":('V','Voltaje entre Fase B  y Neutro [vB]','B'),
    "vC":('V','Voltaje entre Fase C  y Neutro [vC]','C'),

    "V_all_2":('V','VOLTAJES FASE FASE [V]'),
    "vAB":('V','Voltaje entre Fases  A y B [vAB]','AB'),
    "vBC":('V','Voltaje entre Fases  B y C [vBC]','BC'),
    "vCA":('V','Voltaje entre Fases  C y A [vCA]','CA'),

    "I_all":('A','CORRIENTES POR FASE [A]'),
    "iA":('A','Corriente en Fase A [iA]','A'),
    "iB":('A','Corriente en Fase B [iB]','B'),
    "iC":('A','Corriente en Fase C [iC]','C'), 

    "P_all":('kW','POTENCIA ACTIVA POR FASE [kW]'),
    "PA":('kW','Potencia Activa en Fase A [PA]','A'),
    "PB":('kW','Potencia Activa en Fase B [PB]','B'), 
    "PC":('kW','Potencia Activa en Fase C [PC]','C'),
    "P":('kW','Potencia Activa Total [P]','Total'),

    "Q_all":('kVAR','POTENCIA REACTIVA POR FASE [kVAR]'),
    "QA":('kVAR','Potencia Reactiva en Fase A [QA]','A'), 
    "QB":('kVAR','Potencia Reactiva en Fase B [QB]','B'),
    "QC":('kVAR','Potencia Reactiva en Fase C [QC]','C'),
    "Q":('kVAR','Potencia Reactiva Total [Q]','Total'),

    "S_all":('kVA','POTENCIA APARENTE POR FASE [kVA]'),
    "SA":('kVA','Potencia Aparente en Fase A [SA]','A'),
    "SB":('kVA','Potencia Aparente en Fase B [SB]','B'), 
    "SC":('kVA','Potencia Aparente en Fase C [SC]','C'), 
    "S" :('kVA','Potencia Aparente Total [S]','Total'),

    "Wh_all_p":('kWh','ENERGIA ACTIVA POSITIVA POR FASE [kWh]'),
    "P_kWh_A":('kWh','Energía activa en Fase A: Positiva','A'),
    "P_kWh_B":('kWh','Energía activa en Fase B: Positiva','B'),
    "P_kWh_C":('kWh','Energía activa en Fase C: Positiva','C'),
    "P_kWh_T":('kWh','Energía Activa Positiva Total','Total') ,

    "Wh_all_r":('kWh','ENERGIA ACTIVA INVERSA POR FASE [kWh]'),
    "R_kWh_A":('kWh','Energía activa en Fase A: Inversa','A'),
    "R_kWh_B":('kWh','Energía activa en Fase B: Inversa','B'),
    "R_kWh_C":('kWh','Energía activa en Fase C: Inversa','C'),
    "R_kWh_T":('kWh','Energía Activa Inversa Total','Total'),

    "varh_all_p":('kVarh','ENERGIA REACTIVA POSITIVA POR FASE [kVarh]'),
    "P_kvarh_A":('kVarh','Energía reactiva en Fase A: Positiva','A'),
    "P_kvarh_B":('kVarh','Energía reactiva en Fase B: Positiva','B'),
    "P_kvarh_C":('kVarh','Energía reactiva en Fase C: Positiva','C'),
    "P_kvarh_T":('kVarh','Energía Reactiva Positiva Total','Total'),

    "varh_all_r":('kVarh','ENERGIA REACTIVA INVERSA POR FASE [kVarh]'),
    "R_kvarh_A":('kVarh','Energía reactiva en Fase A: Inversa','A'),
    "R_kvarh_B":('kVarh','Energía reactiva en Fase B: Inversa','B'),
    "R_kvarh_C":('kVarh','Energía reactiva en Fase C: Inversa','C'),
    "R_kvarh_T":('kVarh','Energía Reactiva Inversa Total','Total'),

    "PF":('','Factor de Potencia','PF'),
    "F":('Hz','Frecuencia [Hz]','F'), 
    "iF":('A','Corriente de Fuga [A]','Fuga'),
 
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

PARAMETERS_FOR_EVENT_GRAPHS={
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


