from .base import *


class HomePageTest(FunctionalTest):
    def test_home_page_shows_posts_by_all_users(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She logs in
        self.login(username="edith123", password="password123")

        # She creates a post and returns to home page
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys(
            "Edith's title"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()
        wait_for(lambda: self.browser.find_element_by_link_text("Home")).click()

        # She sees a link to her post with her name beside it
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("Edith's title", main_content)
        self.assertIn("edith123", main_content)

        # Meredith does the same on her browser
        edith_browser = self.browser
        meredith_browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary("/usr/lib/firefox/firefox")
        )
        self.browser = meredith_browser
        self.browser.get(f"{self.live_server_url}/blogger/")
        self.login(username="meredith123", password="password123")
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys(
            "Meredith's title"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()
        wait_for(lambda: self.browser.find_element_by_link_text("Home")).click()

        # She sees both posts on the homepage
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("Meredith's title", main_content)
        self.assertIn("Edith's title", main_content)
        self.assertIn("meredith123", main_content)
        self.assertIn("edith123", main_content)

        # Edith also sees both posts on the hompepage
        self.browser = edith_browser
        self.browser.get(f"{self.live_server_url}/blogger/")
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("Meredith's title", main_content)
        self.assertIn("Edith's title", main_content)
        self.assertIn("meredith123", main_content)
        self.assertIn("edith123", main_content)