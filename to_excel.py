import json
import logging

import pandas as pd

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def json_to_excel(file_json: str, file_xlsx: str) -> None:
    with open(file_json, "r", encoding="utf-8") as file:
        file_json = json.load(file)

    colunas = {
        "title": "Titulo",
        "status": "Status",
        "description": "Descrição",
        "date": "Data",
        "chat": "Mensagens",
        "final_consideration.message": "Mensagem de consideração final",
        "final_consideration.service_note": "Nota do serviço",
        "final_consideration.make_business": "Faria negocios futuros",
        "final_consideration.date": "Data da consideração final",
        "link": "Link",
    }

    df = pd.json_normalize(file_json).rename(columns=colunas)
    df.to_excel(file_xlsx, index=False)
    logger.info(f"Save: {file_xlsx}")


file_json = "./claims_list_2024-04-26.json"
file_xlsx = "./claims_list_x_2.xlsx"

json_to_excel(file_json, file_xlsx)
