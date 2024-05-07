import json
import logging

from get_urls_pages import main_get_urls
from scraping import (check_and_update_json, clean_claims, get_dados,
                      get_total_page, request)
from to_excel import json_to_excel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.propagate = True


def main() -> None:
    """
    # ☠️ Change the indicated values no `README.md`.
    ------
    ### ☠️ `main_get_urls()` It's a worrying feature.

    """

    url_base: str = "https://www.reclameaqui.com.br"
    file_json: str = "claims_list"
    file_ulrs_claims: str = "links_claims"
    company: str = "itau"
    filter: str = "&status=EVALUATED"
    url: str = f"/empresa/{company}/lista-reclamacoes"

    urls_file_json: bool = False

    # Um aquivo de urls antigo que pode ser juntado com um novo
    urls_file_old: str = "new_urls_claims.json"

    init_page: int = 1
    error_trial_limit: int = 10
    file_xlsx: str = "claims_list"
    url_claims: str = f"{url_base}{url}/?pagina=1{filter}"
    claims: list[dict] = []

    total_pages = get_total_page(url_claims)
    logger.info(f"Total de paginas: {total_pages}")

    file_json: str = check_and_update_json(file_json)

    if not urls_file_json:
        file_ulrs_claims: str = check_and_update_json(file_ulrs_claims)
        urls = main_get_urls(
            url=url_claims,
            file_ulrs_claims=file_ulrs_claims,
            urls_file_old=None,
            total_pages=total_pages,
            init_page=init_page,
            error_trial_limit=error_trial_limit,
        )
    else:
        with open("new_urls_claims.json", "r", encoding="utf-8") as file:
            urls: list[str] = json.load(file)
        if len(urls) == 0:
            logger.fatal("Não á URLS no arquivo json.")
            return

    logger.info(f"Foram encontradas {len(urls)}.")

    for url in urls:
        try:
            logger.info(url)
            response = request(url)
            claim_dict = get_dados(response, url)
            claims.append(claim_dict)
        except Exception as error:
            logger.fatal(error)
            continue

    claims: list[dict] = clean_claims(claims)

    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(claims, file, ensure_ascii=False, indent=4)

    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(claims, file, ensure_ascii=False, indent=4)

    with open(file_json, "r", encoding="utf-8") as file:
        claims: list[str] = json.load(file)

    json_to_excel(claims, file_xlsx)


if __name__ == "__main__":
    main()
