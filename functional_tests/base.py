from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

User = get_user_model()

MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary("/usr/lib/firefox/firefox")
        )

    def tearDown(self):
        self.browser.quit()

    def signup(self, username, password):
        wait_for(lambda: self.browser.find_element_by_link_text("Sign Up")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_username")).send_keys(
            username
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password1")).send_keys(
            password
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password2")).send_keys(
            password
        )
        wait_for(lambda: self.browser.find_element_by_id("id_signup")).click()

    def login(self, username, password):
        wait_for(lambda: self.browser.find_element_by_link_text("Login")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_username")).send_keys(
            username
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password")).send_keys(
            password
        )
        wait_for(lambda: self.browser.find_element_by_id("id_login")).click()


def wait_for(function):
    start_time = time.time()
    while True:
        try:
            return function()
        except WebDriverException as exception:
            if time.time() - start_time > MAX_WAIT:
                raise exception
            time.sleep(0.5)