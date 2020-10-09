import json
import os
import pickle

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers import auto_login, get_driver


def save_as_json(driver, path: str):
    with open(path, 'w') as f:
        f.write(json.dumps(driver.get_cookies()))


def save_as_pkl(driver, path: str):
    with open(path, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)


if __name__ == '__main__':

    if not os.path.exists("./cookies"):
        os.mkdir("./cookies")

    driver = get_driver("c")

    auto_login(driver)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_is("Illinois Media Space"))
    # wait.until(EC.title_contains("part of title"))
    save_as_json(driver, "cookies/mediaspace.json")

    driver.get("https://illinois.edu/")
    save_as_json(driver, "cookies/illinois.json")

    driver.quit()
