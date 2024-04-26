import json

import pandas as pd


def json_to_excel() -> None:
    file_json = "./claims_list_x.json"
    file_xlsx = "claims_list_x.xlsx"

    with open(file_json, "r", encoding="utf-8") as file:
        file_json = json.load(file)

    colunas = {
        "title": "Titulo",
        "description": "Descrição",
        "status": "Status",
        "date": "Data",
        "link": "Link",
        "chat": "Menagens",
        "final_consideration.message": "Mensagem",
        "final_consideration.service_note": "Nota do serviço",
        "final_consideration.make_business": "Faria negocios futuros",
        "final_consideration.date": "Data",
    }

    df = pd.json_normalize(file_json).rename(columns=colunas)[
        [item[1] for item in colunas.items()]
    ]

    df.to_excel(file_xlsx, index=False)


json_to_excel()
