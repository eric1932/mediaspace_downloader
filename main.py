import csv
import json
import time

from browsermobproxy import Server, Client
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import video_urls
from helpers import *


def load_cookies_from_json(driver, path: str):
    with open(path, "r") as f:
        cookies = json.loads(f.readline())
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_video_info(video_url: str, proxy: Client) -> (str, str):
    driver.get(video_url)

    title = driver.find_element_by_class_name("entryTitle").text

    # load video iframe
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kplayer_ifp"))
        )
    finally:
        pass
    # iframe = driver.find_element_by_id("kplayer_ifp")
    driver.switch_to.frame(iframe)

    # start proxy
    proxy.new_har(title, options={'captureHeaders': True, 'captureContent': False})

    # play video
    try:
        video_play = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='videoHolder']/a"))
        )
        video_play.click()
        print("clicked play button")
    finally:
        pass
    # driver.find_element_by_xpath("//div[@class='videoHolder']/a").click()

    wait = 3
    print(f"now wait for {wait} secs")
    time.sleep(wait)  # TODO
    result = proxy.har

    last_entry = {}
    for entry in result['log']['entries']:
        url = entry['request']['url']
        if "index.m3u8" in url or "a.m3u8" in url:
            # _content = entry['response']['content']['text']
            last_entry = entry

    if last_entry:
        print("found m3u8")
        return title, last_entry['request']['url']
    else:
        print("m3u8 not found")
        return None


if __name__ == '__main__':
    # browsermob
    # Mac
    proxy_server = Server('/home/vagrant/opt/browsermob-proxy-2.1.4/bin/browsermob-proxy')
    # Vagrant
    # proxy_server = Server('/home/vagrant/opt/browsermob-proxy-2.1.4/bin/browsermob-proxy')
    # Linux
    # proxy_server = Server('/home/eric/opt/browsermob-proxy-2.1.4/bin/browsermob-proxy')

    proxy_server.start()
    proxy = proxy_server.create_proxy()

    driver = get_driver(browser="c", proxy=proxy, headless=True)
    # driver = get_driver(browser="f", proxy=proxy, headless=True)

    auto_login(driver)

    try:
        # save m3u8 to file
        # title = title.replace("/", " ")
        # urlretrieve(url, f"{title}.m3u8")
        # append m3u8 to list
        lst = [get_video_info(u, proxy) for u in video_urls]
        lst = [x for x in lst if x]

        with open("urls.csv", "w") as f:
            csv_writer = csv.writer(f)
            for tup in lst:
                csv_writer.writerow(tup)
    finally:
        # clean up
        proxy.close()
        proxy_server.stop()
        driver.quit()
