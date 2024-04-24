import asyncio
import json
import logging
import re

import httpx
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.propagate = True

url_base = "https://www.reclameaqui.com.br"


async def request(client: httpx.AsyncClient, url: str = "") -> httpx.Response:
    headers = {
        "User-Agent": r"Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }

    text_error_500 = r'<p class="sc-1p4i0ux-2 dteYVH">Estamos trabalhando para resolver o problema. Por favor, tente entrar de novo daqui a pouco.</p>"'

    url = url_base + url
    timeout = httpx.Timeout(15.0, connect=60.0)
    response = await client.get(url=url, headers=headers, timeout=timeout)

    if text_error_500 in response.text:
        return None
    else:
        return response


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
            "data": date,
        }
    )

    return chat, final_consideration


async def beautiful_soup(client: httpx.AsyncClient, html: str):
    chat = []
    final_consideration = []

    with open("list_claims_links.json", "r", encoding="utf8") as json_file:
        summary = json.load(json_file)

    try:
        soup = BeautifulSoup(html.text, "lxml")
        container = soup.find("div", {"class": "sc-1pe7b5t-0"})
        title = container.find("h4", {"class": "sc-1pe7b5t-1 bVKmkO"})
        status = container.find("span")

        link = container.find("a").get("href")

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
                "href": f"{url_base}{link}",
                "chat": chat,
                "final_consideration": final_consideration,
            }
        )
        with open("list_claims_links.json", "w", encoding="utf8") as json_file:
            json.dump(summary, json_file, indent=4, ensure_ascii=False)

    except Exception as error:
        logger.error(error)
        with open("list_claims_links.json", "w", encoding="utf8") as json_file:
            json.dump(summary, json_file, indent=4, ensure_ascii=False)


async def main(client: httpx.AsyncClient):
    pages = 13991
    company = "itau"
    filter = "&status=EVALUATED"
    url = f"/empresa/{company}/lista-reclamacoes"

    for i in range(pages):
        if i == 0:
            continue
        if i == pages:
            break
        response = await request(client, url=f"{url}/?pagina={i}{filter}")
        if not response:
            logger.error(f"Erro 500 -> Request id: {i}")
            continue
        if response.status_code == 200:
            await beautiful_soup(client, response)
        else:
            logger.error(f"Status: {response.status_code} -> Request id: {i}")


async def client():
    async with httpx.AsyncClient() as client:
        await main(client)


if __name__ == "__main__":
    try:
        asyncio.run(client())
    except Exception as error:
        logger.error(error)
