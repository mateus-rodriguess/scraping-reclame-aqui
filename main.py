import json
import logging
import os
import re
from datetime import datetime
from typing import Tuple

import requests
from bs4 import BeautifulSoup

from get_urls_pages import main_get_urls
from to_excel import json_to_excel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.propagate = True

session = requests.Session()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.5",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "name": "Sec-Fetch-Mode",
    "Sec-Fetch-Site": "none",
    "valSec-Fetch-Userue": "?1",
    "Upgrade-Insecure-Request": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Host": "www.reclameaqui.com.br",
}


def request(url: str = "") -> requests.Response:
    text_error_500 = r'<p class="sc-1p4i0ux-2 dteYVH">Estamos trabalhando para resolver o problema. Por favor, tente entrar de novo daqui a pouco.</p>"'
    text_error_page = r"Ops! Não conseguimos ir até a página"

    response = session.get(url=url, headers=headers, timeout=10)
    if text_error_500 in response.text or text_error_page in response.text:
        return None
    else:
        return response


def clean_claims(claims: list[dict]) -> list[dict]:
    unique_keys = set()
    unique_dicts = []

    for dictionary in claims:
        key = dictionary["title"]
        if key not in unique_keys:
            unique_keys.add(key)
            unique_dicts.append(dictionary)

    logger.info(
        f"De {len(claims)} foram encontrada {len(unique_dicts)} reclamações unicas."
    )
    return unique_dicts


def get_total_page(url: str) -> int | None:
    response = request(url)

    page_html = BeautifulSoup(response.text, "html.parser")
    page_total = page_html.find("span", {"data-testid": "pages-label"})

    if not page_total:
        logger.fatal(
            "Não foi encontrado o total de paginas, procure manualmente."
        )
        return None

    return int(page_total.text.split()[-1])


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


def chat_response(containers: BeautifulSoup) -> Tuple[list[dict], dict]:
    chat = []
    final_consideration = {}

    for container in containers.find_all(
        "div", {"data-testid": "complaint-interaction"}
    ):

        owner = container.find("h2").text
        date = container.find("span", {"class": "sc-1o3atjt-3 bHNkuv"}).text

        if not container.find("h2", {"type": "FINAL_ANSWER"}):
            message_owner = container.find("p", {"class": "sc-1o3atjt-4"}).text
            chat.append(
                {
                    "owner": owner,
                    "date": date,
                    "chat": message_owner,
                }
            )

    complaint = containers.find(
        "div", {"data-testid": "complaint-evaluation-interaction"}
    )

    if complaint:
        message = complaint.find(
            "div", {"data-testid": "complaint-interaction"}
        )

        date = complaint.find("span").text

        make_business = complaint.find(
            "div", {"data-testid": "complaint-deal-again"}
        )
        service_note = complaint.find_all("div", {"class": "sc-uh4o7z-0"})
        regex = re.compile(r"\d+")
        service_note = complaint.find_all(string=regex)[-1]

        if make_business:
            make_business = make_business.text
        if message:
            message = message.find("p").text

    final_consideration = {
        "message": message,
        "service_note": service_note,
        "make_business": make_business,
        "date": date,
    }

    return chat, final_consideration


def get_dados(containers: requests.Response, url: str) -> list:
    claims = {}
    containers = BeautifulSoup(containers.text, "html.parser")

    detail = containers.find(
        "div", {"data-testid": "complaint-content-container"}
    )
    status = (
        detail.find("div", {"data-testid": "complaint-status"})
        .find("span")
        .text
    )
    title = detail.find("h1", {"data-testid": "complaint-title"}).text
    date = detail.find("span", {"data-testid": "complaint-creation-date"}).text

    cotaniner_claim = containers.find(
        "div", {"data-testid": "complaint-content-container"}
    )
    description = cotaniner_claim.find(
        "p", {"data-testid": "complaint-description"}
    ).text

    chat, final_consideration = chat_response(
        containers.find("div", {"data-testid": "complaint-interaction-list"})
    )

    claims = {
        "title": title,
        "description": description,
        "status": status,
        "chat": chat,
        "date": date,
        "link": url,
        "final_consideration": final_consideration,
    }

    return claims


def main() -> None:
    """
    # ☠️ Change the indicated values no `README.md`
    ------
    ### ☠️ `main_get_urls()` It's a worrying feature.

    """

    url_base: str = "https://www.reclameaqui.com.br"
    file_json: str = "claims_list"
    file_ulrs_claims = "links_claims"
    company: str = "itau"
    filter: str = "&status=EVALUATED"
    url: str = f"/empresa/{company}/lista-reclamacoes"
    urls_file_json = True
    init_page = 1

    file_json: str = check_and_update_json(file_json)

    url_claims: str = f"{url_base}{url}/?pagina=1{filter}"

    total_pages = get_total_page(url_claims)
    logger.info(f"Total de paginas: {total_pages}")

    if not urls_file_json:
        file_ulrs_claims: str = check_and_update_json(file_ulrs_claims)
        urls = main_get_urls(
            url=url_claims,
            file_ulrs_claims=file_ulrs_claims,
            total_pages=total_pages,
            init_page=init_page,
        )
    else:
        with open("urls.json", "r", encoding="utf-8") as file:
            urls: list[str] = json.load(file)

    claims = []
    try:
        for url in urls:
            logger.info(url)
            response = request(url)
            claim_dict = get_dados(response, url)
            claims.append(claim_dict)
            
    except Exception as error:
        logger.fatal(error)

    claims: list[dict] = clean_claims(claims)
    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(claims, file, ensure_ascii=False, indent=4)

    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(claims, file, ensure_ascii=False, indent=4)

    json_to_excel(file_json)

if __name__ == "__main__":
    main()
