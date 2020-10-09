from selenium import webdriver

from config import User, Pass


def auto_login(driver):
    login_url = "https://mediaspace.illinois.edu/user/login"
    driver.get(login_url)
    input_user = driver.find_element_by_id('j_username')
    input_user.send_keys(User)
    input_pass = driver.find_element_by_id('j_password')
    input_pass.send_keys(Pass)
    submit = driver.find_element_by_xpath("//div[@id='submit_button']/input")
    submit.click()


def get_driver(browser: str, proxy=None):
    if "chrome".startswith(browser.lower()):
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        if proxy:
            options.add_argument('--proxy-server={0}'.format(proxy.proxy))
        return webdriver.Chrome(options=options)
    elif "firefox".startswith(browser.lower()):
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        if proxy:
            profile.set_proxy(proxy.selenium_proxy())
        return webdriver.Firefox(firefox_profile=profile)
    else:
        pass
