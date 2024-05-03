import json
import logging
import random
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.propagate = True


def scroll_page() -> None:
    x = random.randint(0, 450)
    y = random.randint(0, 540)
    driver.execute_script(f"window.scrollTo({x}, {y})")


def check_block_page(n: int = 0) -> None:
    n += 1
    logger.info("Checando se a pagina esta bloqueada")
    block_page = driver.find_element(By.ID, "sec-overlay")
    if block_page.get_attribute("style") == "display: block;":
        logger.info(block_page.get_attribute("style"))
        logger.info(f"Pagina bloqueda, espere alguns segundos, tentativa {n}")
        sleep(10)
        check_block_page(n)


def check_button_next_page(n: int = 0) -> webdriver.Firefox:
    n += 1
    try:
        wait = WebDriverWait(driver, 5)
        button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@aria-label='botão de navegação para a próxima página']",
                )
            ),
            "Botão não esta visivel.",
        )
    except:
        logger.error(
            f"Botão não esta visivel. tentando de novo, tentativa {n}"
        )
        check_button_next_page(n)
    if button.is_displayed():
        return button
    else:
        check_button_next_page(n)


def remove_block() -> None:
    try:
        element_block = driver.find_element(By.CLASS_NAME, "cc-window")
        driver.execute_script("arguments[0].remove()", element_block)
        logger.info("Elemento de block removido.")
    except Exception as error:
        logger.error(f"Elemento não encrontrado -> continue...")


def get_urls() -> list[str]:
    urls: list[str] = []
    xpath_links = '//div[@class="sc-1pe7b5t-0 eJgBOc"]/a'
    elementes = driver.find_elements(By.XPATH, xpath_links)

    if not elementes:
        return urls

    return [url.get_attribute("href") for url in elementes]


def get_urls_page(n: int = 0) -> list[str]:
    n += 1
    try:
        check_block_page()
        scroll_page()
        sleep(random.uniform(0.2, 0.8))
        check_button_next_page()
        remove_block()
        return get_urls()
    except Exception as error:
        logger.error(f"erro: {error}\n-> tentativa: {n}")
        get_urls_page(n)


def check_urls_claims_in_page():
    page_html = driver.page_source
    texts_error = [
        "Ops, algo deu errado",
        "Ops! Não conseguimos ir até a página",
    ]

    return texts_error in page_html


def main_get_urls(
    url: str,
    file_ulrs_claims: str,
    total_pages: int = 1,
    init_page: int = 1,
):
    """
    # ☠️ most functions in this context are recursive.
    # ☠️  careful when calling them, pay attention to the logs
    ##
    ----
    ```python

    sys.setrecursionlimit(110)
    ```
    """
    global driver

    sys.setrecursionlimit(100)

    user_agent = "--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
    firefox_options = Options()
    firefox_options.add_argument(user_agent)

    driver = webdriver.Firefox(options=firefox_options)

    driver.get(url)

    logger.info("INICIANDO ELEMENTOS DA PAGINA....")
    sleep(random.uniform(3, 9))

    for i in range(init_page, total_pages):
        if not check_urls_claims_in_page():
            logger.error(
                f"A pagina não cotem links de reclamações, indo para a proxima pagina {i} de {total_pages}"
            )
            continue

        with open(file_ulrs_claims, "r", encoding="utf-8") as file:
            ulrs_file: list[str] = json.load(file)

        urls: list[str] = get_urls_page()
        ulrs_file.extend(urls)

        with open(file_ulrs_claims, "w", encoding="utf-8") as file:
            logger.info(f"Salvando urls, total: {len(ulrs_file)}")
            json.dump(ulrs_file, file, ensure_ascii=False, indent=4)

        logger.info(f"Proxima pagina: {i} de {total_pages}")

        sleep(random.uniform(0.2, 0.8))

        check_block_page()
        button = check_button_next_page()

        remove_block()
        button.click()

    driver.close()

    return ulrs_file
