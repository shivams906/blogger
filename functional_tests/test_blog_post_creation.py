from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 5


class BlogTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary("/usr/lib/firefox/firefox")
        )

    def tearDown(self):
        self.browser.quit()

    def test_blog_post_creation(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")
        wait_for(lambda: self.assertIn("Home", self.browser.title))
        self.fail("finish the test")

        # She clicks on the add post link
        # She writes in the content and clicks the publish button
        # She is taken to the newly created post's page


def wait_for(function):
    start_time = time.time()
    while True:
        try:
            return function()
        except WebDriverException as exception:
            if time.time() - start_time > MAX_WAIT:
                raise exception
            time.sleep(0.5)