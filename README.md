<h1 align="center">
	<img alt="logo" src="https://www.python.org/static/community_logos/python-logo-generic.svg" style="width: 600px; height: 900;">
</h1>


## Introduction
Of course, here's some sample text you can use for your project's README.md on GitHub:
Reclame Aqui Information Extraction Project.
This project is a tool developed to extract information about complaints from the Reclame Aqui website. 
Reclame Aqui is a platform widely used by Brazilian consumers to register their complaints about products and services from various companies.

## Features
Data Extraction: The project uses web scraping techniques to extract relevant data from complaints registered on Reclame Aqui.
including complaint text, company complained about, category, consumer evaluation, among others.
Data Analysis: In addition to extraction, the project can also include functionalities to analyze the extracted data,
identifying trends, patterns and useful insights for companies and consumers.



## Install
    ```bash
        pip install -r requirements.txt

    ```
## Run

    ```bash
        ptyhon main.py
    ``

### Json with the extracted information
```json
    [
        {
            "title": "algo",
            "description": "algo longo",
            "status": "resolvido",
            "date": "23/04/2024 às 14:43",
            "href": "https://www.reclameaqui.com.br/xxx",
            "chat": [
                {
                    "owner": "Resposta da empresa",
                    "date": "24/04/2024 às 12:01",
                    "response": "algo longo"
                }
            ],
            "final_consideration": [
                {
                    "message": "aqui tambem",
                    "service_note": "10",
                    "make_business": "Sim",
                    "data": "24/04/2024 às 14:11"
                }
            ]
        }
    ]
```
