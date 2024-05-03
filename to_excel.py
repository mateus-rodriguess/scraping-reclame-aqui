import json
import logging

import pandas as pd


def json_to_excel(file_json: str) -> None:

    with open(file_json, "r", encoding="utf-8") as file:
        file = json.load(file)

    colunas = {
        "title": "Titulo",
        "status": "Status",
        "description": "Descrição",
        "chat": "Mensagens",
        "date": "Data",
        "final_consideration.message": "Mensagem de consideração final",
        "final_consideration.service_note": "Nota do serviço",
        "final_consideration.make_business": "Faria negocios futuros?",
        "final_consideration.date": "Data da consideração final",
        "link": "Link",
    }
    
    file_xlsx = file_json.replace(".json", ".xlsx")
    df = pd.json_normalize(file).rename(columns=colunas)

    df.to_excel(file_xlsx, index=False)
    logging.info(f"Save: {file_xlsx}")
