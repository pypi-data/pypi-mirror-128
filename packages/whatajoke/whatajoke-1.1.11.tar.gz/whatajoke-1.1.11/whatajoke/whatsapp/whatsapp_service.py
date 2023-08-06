import os
import shutil
import time
from os.path import abspath

from selenium import webdriver
from selenium.webdriver import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

whatsapp_url: str = "https://web.whatsapp.com/"

sleep_time = 3

input_search_xpath = "//*[@id=\"side\"]/div[1]/div/label/div/div[2]"
input_message_xpath = "//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]"
open_group_xpath = "//*[@id=\"main\"]/header/div[2]/div[1]/div/span"
qr_xpath = "//*[@id=\"app\"]/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas"


def get_user_data_folder_abs_path() -> str:
    dirname = os.path.dirname(__file__)

    relative_path_to_user_data_folder = "../../User_Data"
    user_data_folder_path = os.path.join(dirname, relative_path_to_user_data_folder)
    user_data_folder_path_abs = abspath(user_data_folder_path)

    return user_data_folder_path_abs


def select_contact_xpath(contact) -> str:
    return '//span[@title="{}"]'.format(contact)


def assert_correct_contact(group: str, group_title_element):
    assert group_title_element.text == group


def send_message(group: str, message: str, headed: bool):
    user_data_folder_abs_path = get_user_data_folder_abs_path()

    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={user_data_folder_abs_path}')

        if not headed:
            options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 ' \
                         'Safari/537.36 '
            options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        driver.get(whatsapp_url)

        input_box_search = WebDriverWait(driver, 50) \
            .until(lambda driver: driver.find_element_by_xpath(input_search_xpath))
        input_box_search.click()
        input_box_search.send_keys(group)

        selected_contact = WebDriverWait(driver, 50) \
            .until(lambda driver: driver.find_element_by_xpath(select_contact_xpath(group)))
        selected_contact.click()

        group_title_element = WebDriverWait(driver, 50) \
            .until(lambda driver: driver.find_element_by_xpath(open_group_xpath))
        assert_correct_contact(group, group_title_element)

        message_box = WebDriverWait(driver, 50) \
            .until(lambda driver: driver.find_element_by_xpath(input_message_xpath))
        message_box.send_keys(message + Keys.ENTER)

        # sleep is needed to wait for sending the message
        time.sleep(sleep_time)

    finally:
        driver.quit()


def login():
    user_data_folder_abs_path = get_user_data_folder_abs_path()

    if os.path.isdir(user_data_folder_abs_path):
        shutil.rmtree(user_data_folder_abs_path)

    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={user_data_folder_abs_path}')

        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        driver.get(whatsapp_url)

        WebDriverWait(driver, 50) \
            .until(lambda driver: driver.find_element_by_xpath(qr_xpath))

        WebDriverWait(driver, 50) \
            .until_not(lambda driver: driver.find_element_by_xpath(qr_xpath))

        time.sleep(sleep_time)

    finally:
        driver.quit()
