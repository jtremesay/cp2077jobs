#!/usr/bin/env python3
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    output_dir = Path("html")
    output_dir.mkdir(exist_ok=True)

    driver = webdriver.Firefox()
    driver.get("https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Main_Jobs")

    links = [
        (link.get_attribute("title"), link.get_attribute("href"))
        for link in driver.find_elements(By.CSS_SELECTOR, ".navbox li a")
    ]
    for link_title, link_href in links:
        page_file = output_dir / f"{link_title}.html"
        if page_file.exists():
            print(f"{link_title} already exists, skipping")
            continue
        print(f"Saving {link_title} from {link_href}")

        driver.get(link_href)
        content_node = driver.find_element(By.CSS_SELECTOR, ".mw-parser-output")
        page_file.write_text(content_node.get_attribute("outerHTML"))

    driver.quit()


if __name__ == "__main__":
    main()
