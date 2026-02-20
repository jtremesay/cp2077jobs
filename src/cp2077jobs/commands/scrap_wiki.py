#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

from cp2077jobs.settings import HTML_DIR, WIKI_BASE_URL


def main():
    HTML_DIR.mkdir(exist_ok=True)

    driver = webdriver.Firefox()
    driver.get(f"{WIKI_BASE_URL}Cyberpunk_2077_Main_Jobs")

    links = [
        (link.get_attribute("title"), link.get_attribute("href"))
        for link in driver.find_elements(By.CSS_SELECTOR, ".navbox li a")
    ]
    for link_title, link_href in tqdm(links):
        tqdm.write(f"Saving {link_title} from {link_href}")

        page_name = link_href.rsplit("/", 1)[-1]
        page_file = HTML_DIR / f"{page_name}.html"
        if page_file.exists():
            continue

        driver.get(link_href)
        page_file.write_text(
            driver.find_element(By.CSS_SELECTOR, "main.page__main").get_attribute(
                "outerHTML"
            )
        )

    driver.quit()
