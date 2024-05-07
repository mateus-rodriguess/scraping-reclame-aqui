import logging
import os
from datetime import datetime

import pandas as pd


def json_to_excel(claims: list[dict], file_name: str = "claims_list") -> None:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    current_date = datetime.now().date()

    file_xlsx = f"{ROOT_DIR}/{file_name}_{current_date}.xlsx"

    colunas = {
        "title": "Titulo",
        "status": "Status",
        "description": "Descrição",
        "chat": "Mensagens",
        "tags": "Categorias",
        "location": "Localização",
        "id": "Id",
        "date": "Data",
        "final_consideration.message": "Mensagem de consideração final",
        "final_consideration.service_note": "Nota do serviço",
        "final_consideration.make_business": "Faria negocios futuros?",
        "final_consideration.date": "Data da consideração final",
        "link": "Link",
    }

    df = pd.json_normalize(claims).rename(columns=colunas)
    df.to_excel(file_xlsx)

    logging.info(f"Save: {file_xlsx}")
