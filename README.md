<h1 align="center">
  <img alt="logo" src="https://www.python.org/static/community_logos/python-logo-generic.svg" style="width: 600px; height: 900;">
</h1>


## Introduction
This project is a tool developed to extract information about complaints from the Reclame Aqui website.
Reclame Aqui is a platform widely used by Brazilian consumers to register their complaints about products and services from different companies.

## Features
 - 📊 Data Extraction: The project uses web scraping techniques to extract relevant data from complaints registered on Reclame Aqui.
 - 📈 Data Analysis: In addition to extraction, the project can also include functionalities to analyze the extracted data.




## Install
```bash
pip install -r requirements.txt

```
## 🚀 Run

```bash
ptyhon main.py
```

## ☠️ Attention
Attention, so that the project adapts to your problem, change the values ​​of the variables according to your objective, the variables in question are in the `main() function`
```python
async def main():
    pages = 0 # here
    company = "company" # here
    query = "&status=EVALUATED" #here
    url = f"/empresa/{company}/lista-reclamacoes"
    for i in range(id):
	if i == 0: # here
	    break
```


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
