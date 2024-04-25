import asyncio
import json
import logging
import os
import re
from datetime import datetime

import httpx
import pandas as pd
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.propagate = True


async def request(client: httpx.AsyncClient, url: str = "") -> httpx.Response:
    headers = {
        "User-Agent": r"Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Cookie": r"abck=8A19A02F216E050841B90FF4AE4FD79C~-1~YAAQFBVlaEdP2OiOAQAAZAY3FwsbQOmtbg8HGQ3P0heHnd//W28Iyh3nd7lupONGTZkZV+uQIya616iAQHR4Z3P3hXmgFhq2pOL1+/cbhIH8wfHDoT/85ms8q9KaEjHK9SX4aaPo5Jh9am7DipoSZwPPm2RnmHJNYMT3KbqunlOMb46mw+OGmVaL5lqNosLJEclwUFtMfed7sECj28/oq8PowKtDm8thaGF4CwUU0wgyghadLwSNZwG3KplymXis7woLW+QJscazg0/3oeC+E8FhctT6kdeDKZ4PiDf4X6CUFMZiJITuh8T3eWXl2RCMyjNp2JRxV9AQhtqmfRv5DfFaGRIbTF+zFKXw90wSqSpW4x+Hg7fkaSuUhuP4VqXZJTJZG3nfWtXT/zKyudXMegd9NJhoW/XtCgM7TOdx~-1~-1~-1; _gcl_au=1.1.817180335.1713980297; _…1J6HxIAFguIgm304fKwDCserlcRSEkOCEKVUCly2izZof2VV/ahCXO4sswBXd1MKk7lKE++Q3r34QzGWwCsl9IJRc9P7gY733tZV8VIEuxqtZI3qggNwoeuE9Y/BYDK5USajmBm64mV+i2uVeR5MduzR9i0k7m+JFPX5Bd6RCrsiUYk+6ITewi7JNemh2NoHvH5nYKS5B5X/Uo7gxRAVs6pUhkU65EysIl2E0vHChdWv2qlsp7VKyCQD5w9iN+NvBxpHm4A8md1Ji1s9dcG/zF4aIYYWsdUxKcZtEcD+1DtLR2qw5HcoWtsZMyg==; _hjSession_417945=eyJpZCI6Ijg0ODc0Y2ZmLWQ2MTUtNDU1NS05YTVmLTUxNzlkNDQ3NTMwZiIsImMiOjE3MTQwODA5MzMwNjEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gat_gtag_UA_5435672_2=1",
    }
    url = url_base + url
    text_error_500 = r'<p class="sc-1p4i0ux-2 dteYVH">Estamos trabalhando para resolver o problema. Por favor, tente entrar de novo daqui a pouco.</p>"'
    text_error_page = r"Ops! Não conseguimos ir até a página"

    timeout = httpx.Timeout(20.0, connect=1000.0)
    response = await client.get(url=url, headers=headers, timeout=timeout)

    if text_error_500 in response.text or text_error_page in response.text:
        return None
    else:
        return response


def json_to_excel(file_json: str, file_xlsx: str) -> None:
    current_date = datetime.now().date()
    file_xlsx = f"{ROOT_DIR}/{file_xlsx}_{current_date}.xlsx"

    with open(file_json, "r", encoding="utf-8") as file:
        file_json = json.load(file)

    colunas = {
        "title": "Titulo",
        "description": "Descrição",
        "status": "Status",
        "date": "Data",
        "link": "Link",
        "chat": "Chat",
        "final_consideration.message": "Mensagem",
        "final_consideration.service_note": "Nota do serviço",
        "final_consideration.make_business": "Faria negocios futuros",
        "final_consideration.date": "Data",
    }
    df = pd.json_normalize(file_json).rename(columns=colunas)[
        [item[1] for item in colunas.items()]
    ]

    df.to_excel(file_xlsx, index=False)


def chat_response(complaint_interaction_list: list) -> list:
    chat = []
    final_consideration = []
    response = []
    make_business = None
    service_note = None

    for complaint_interaction in complaint_interaction_list.find_all(
        "div", {"data-testid": "complaint-interaction"}
    ):
        owner = complaint_interaction.find("h2").text
        date = complaint_interaction.find(
            "span", {"class": "sc-1o3atjt-3 bHNkuv"}
        ).text

        if not complaint_interaction.find("h2", {"type": "FINAL_ANSWER"}):
            response = complaint_interaction.find(
                "p", {"class": "sc-1o3atjt-4"}
            )
            chat.append(
                {"owner": owner, "date": date, "response": response.text}
            )

    complaint_evaluation = complaint_interaction_list.find(
        "div", {"data-testid": "complaint-evaluation-interaction"}
    )
    if complaint_evaluation:
        message = complaint_evaluation.find(
            "div", {"data-testid": "complaint-interaction"}
        )

        date = complaint_evaluation.find("span").text

        make_business = complaint_evaluation.find(
            "div", {"data-testid": "complaint-deal-again"}
        )
        service_note = complaint_evaluation.find_all(
            "div", {"class": "sc-uh4o7z-0"}
        )
        regex = re.compile(r"\d+")
        service_note = complaint_evaluation.find_all(string=regex)[-1]
        if make_business:
            make_business = make_business.text

    final_consideration.append(
        {
            "message": message.find("p").text,
            "service_note": service_note,
            "make_business": make_business,
            "date": date,
        }
    )

    return chat, final_consideration


async def beautiful_soup(client: httpx.AsyncClient, response):
    chat = []
    final_consideration = []
    with open(file_json, "r", encoding="utf8") as json_file:
        summary = json.load(json_file)

    try:
        soup = BeautifulSoup(response.text, "lxml")
        lista_claims = soup.find(
            "div", {"class": "sc-1sm4sxr-0 iwOeoe"}
        ).find_all("div", {"class": "sc-1pe7b5t-0 eJgBOc"})
        for container in lista_claims:
            link = container.find("a").get("href")
            title = container.find("h4", {"class": "sc-1pe7b5t-1 bVKmkO"})
            status = container.find("span")

            response = await request(client, link)
            cotaniner_container_chat = BeautifulSoup(response.text, "lxml")

            cotaniner_claim = cotaniner_container_chat.find(
                "div", {"data-testid": "complaint-content-container"}
            )
            description = cotaniner_claim.find(
                "p", {"data-testid": "complaint-description"}
            ).text

            date = cotaniner_claim.find(
                "span", {"data-testid": "complaint-creation-date"}
            ).text
            chat, final_consideration = chat_response(cotaniner_container_chat)

            summary.append(
                {
                    "title": title.text.lower(),
                    "description": description,
                    "status": status.text.lower(),
                    "date": date,
                    "link": f"{url_base}{link}",
                    "chat": chat,
                    "final_consideration": final_consideration[0],
                }
            )
        with open(file_json, "w", encoding="utf8") as json_file:
            json.dump(summary, json_file, indent=4, ensure_ascii=False)
    except Exception as error:
        logger.error(error)
        with open(file_json, "w", encoding="utf8") as json_file:
            json.dump(summary, json_file, indent=4, ensure_ascii=False)


async def get_total_page(client, url: str) -> int | None:
    response = await request(client, url)

    soup = BeautifulSoup(response.text, "lxml")

    page_total = soup.find("span", {"data-testid": "pages-label"})

    if not page_total:
        logger.fatal(
            "Não foi encontrado o total de paginas, procure manualmente."
        )
        return None
    total_page = int(page_total.text.split()[-1])
    logger.info(f"Total de paginas: {total_page}")
    return total_page


async def client() -> None:
    async with httpx.AsyncClient() as client:
        await main(client)


def check_and_update_json(name_file: str) -> str:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    current_date = datetime.now().date()
    file_json = f"{ROOT_DIR}/{name_file}_{current_date}.json"

    if os.path.exists(file_json):
        modification_date = datetime.fromtimestamp(
            os.path.getmtime(file_json)
        ).date()
        if modification_date == current_date:
            with open(file_json, "w") as json_file:
                json_file.write("[]")
            logger.info(
                f"O arquivo JSON {file_json} foi atualizado com uma matriz vazia."
            )
        else:
            new_json_file = f"{ROOT_DIR}/claims_list_{current_date}.json"
            with open(new_json_file, "w") as json_file:
                json_file.write("[]")
            logger.info(f"Um novo arquivo JSON {new_json_file} foi criado.")
    else:
        with open(file_json, "w") as json_file:
            json_file.write("[]")
        logger.info(f"Um novo arquivo JSON {file_json} foi criado.")
    return file_json


async def main(client: httpx.AsyncClient) -> None:
    """
    # ☠️ Change the indicated values no `README.md`
    """

    global file_json
    global url_base
    global ROOT_DIR
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    url_base = "https://www.reclameaqui.com.br"
    file_json = "claims_list"
    company = "itau"
    filter = "&status=EVALUATED"
    url = f"/empresa/{company}/lista-reclamacoes"

    file_xlsx = "claims_list"
    init_page = 1
    total_page = await get_total_page(client, f"{url}/?{filter}")
    file_json = check_and_update_json(file_json)

    def start_page(stop, start=0, step=1) -> list:
        return range(start, stop, step)

    for i in start_page(stop=total_page, start=init_page, step=1):
        try:
            response = await request(client, url=f"{url}/?pagina={i}{filter}")
            if not response:
                logger.error(f"Erro 500 -> Request id: {i}, sleep 3 segundos")
                continue
            if response.status_code == 200:
                await beautiful_soup(client, response)
                json_to_excel(file_json, file_xlsx)
            else:
                logger.error(
                    f"Status: {response.status_code} -> Request id: {i}"
                )
        except Exception as error:
            logger.error(f"Request, 3 segundos ate a proxima request: {error}")


if __name__ == "__main__":
    try:
        asyncio.run(client())
    except Exception as error:
        logger.error(error)
