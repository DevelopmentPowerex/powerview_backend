import pandas as pd


import logging
logger = logging.getLogger(__name__)


async def generate_csv(circuits,whole_reading):

    circuits_list=[c.get('nickname') for c in circuits]

    out_path=r"C:\Users\jeras\Documents\PowerView\backend_pv\OnDemand\report_generator\result\report.xlsx"

    with pd.ExcelWriter(out_path, engine="openpyxl", datetime_format="yyyy-mm-dd hh:mm:ss") as writer:
        for circuit in circuits_list:
            filtered_reading=[r for r in whole_reading if r.get("circuit")==circuit]
    
            rows = []
            for r in filtered_reading:
                ts = r.get("timestamp")
                reading = r.get("reading") or {}
                row = {"Timestamp": ts, **reading}
                rows.append(row)

            df = pd.DataFrame(rows)

            # Ordena por Timestamp y deja Timestamp como primera columna
            if "Timestamp" in df.columns:
                df = df.sort_values("Timestamp", kind="stable")

            # Asegura que Timestamp sea la primera columna
            cols = ["Timestamp"] + [c for c in df.columns if c != "Timestamp"]
            df = df[cols]
            
            sheet_name = str(circuit)[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return out_path



