<h1 align="center">
  <img alt="logo" src="https://www.python.org/static/community_logos/python-logo-generic.svg" style="width: 700px; height: 950;">
</h1>

## Introduction

This project is a tool developed to extract information about complaints from the Reclame Aqui website.
Reclame Aqui is a platform widely used by Brazilian consumers to register their complaints about products and services from different companies.

## Features

- 📊 Data Extraction: The project uses web scraping techniques to extract relevant data from complaints registered on Reclame Aqui.
- 📈 Data Analysis: In addition to extraction, the project can also include functionalities to analyze the extracted data.
- 📝 Convert json to xlsx file for analysis.

## Install

- ☠️ Requires `Python` 3.8 or later to run.

```bash
pip install -r requirements.txt
```

## 🚀 Run

```bash
ptyhon main.py
```

## ☠️ Attention

Attention, so that the project adapts to your problem, change the values of the variables according to your objective, the variables in question are in the `main() function`.

```python
def main():
    """
    # ☠️ Change the indicated values no `README.md`
    """

    global file_json
    global url_base
    global ROOT_DIR
    global file_xlsx

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    url_base = "https://www.reclameaqui.com.br"
    file_json = "claims_list" # maybe here
    company = "itau" # here
    _filter = "&status=EVALUATED" # here
    url = f"/empresa/{company}/lista-reclamacoes"

    file_xlsx = "claims_list" # maybe here
    init_page = 1 # maybe here
```

### Json with the extracted information

```json
[
    {
        "title": "Algo  aqui",
        "description": "Algo  aqui",
        "status": "não resolvido",
        "date": "xx/xx/20xx às xx:xx",
        "link": "https://www.reclameaqui.com.br/xx/algo-aqui_xxx/",
        "chat": [
            {
                "owner": "Resposta da empresa",
                "date": "xx/xx/20xx às xx:xx",
                "message_owner": "Algo aqui"
            }
        ],
        "final_consideration": {
            "message": "Algo",
            "service_note": "10",
            "make_business": "Sim",
            "date": "xx/xx/20xx às xx:xx"
        }
    },
]
```
