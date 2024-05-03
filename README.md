<h1 align="center">
  <img alt="logo python" src="https://www.python.org/static/community_logos/python-logo-generic.svg" style="width: 750px; height: 975;">
</h1>
<hr>

## Introduction

This project is a tool developed to extract information about complaints from the Reclame Aqui website.
Reclame Aqui is a platform widely used by Brazilian consumers to register their complaints about products and services from different companies.
<hr>

## Features

- 📊 Data Extraction: The project uses web scraping techniques to extract relevant data from complaints registered on Reclame Aqui.
- 📈 Data Analysis: In addition to extraction, the project can also include functionalities to analyze the extracted data.
- 📝 Convert json to xlsx file for analysis.
<hr>

## Install

- ☠️ Requires `Python` 3.12 or later to run.

```bash
pip install -r requirements.txt
```
<hr>

## 🚀 Run

```bash
ptyhon main.py
```
<hr>

## ☠️ Attention

- Attention, so that the project adapts to your problem, change the values of the variables according to your objective, the variables in question are in the `main() function` in `main.py`.
- This project was for a specific case, so it may not be a solution for everyone.
- `urls_file_json` is a variable that indicates whether there is a file containing the urls, if you have already run the function that captures this.


```python
def main():
    """
    # ☠️ Change the indicated values no `README.md`
    """
    url_base: str = "https://www.reclameaqui.com.br"
    file_json: str = "claims_list" # here
    file_ulrs_claims = "links_claims" # here
    company: str = "itau" # here
    filter: str = "&status=EVALUATED" # here
    url: str = f"/empresa/{company}/lista-reclamacoes"
    init_page = 1 # here maybe
    urls_file_json = False # here maybe
```

<hr>

### Json with the extracted information

```json
[
    {
        "title": "Proteção, só que não...",
        "description": "Algo grande",
        "status": "Não resolvido",
        "chat": [
            {
                "owner": "Resposta da empresa",
                "date": "03/05/2024 às 14:20",
                "chat": "algo grande"
            }
        ],
        "date": "03/05/2024 às 12:15",
        "link": "https://www.reclameaqui.com.br/xxx/algo-grande-xxx",
        "final_consideration": {
            "message": "Colou o texto e não explicou nada.",
            "service_note": "0",
            "make_business": "Não",
            "date": "03/05/2024 às 14:24"
        }
    }
]
```
