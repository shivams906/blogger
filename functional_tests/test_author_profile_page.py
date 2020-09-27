from .base import *


class AuthorProfilePageTest(FunctionalTest):
    def test_author_profile_page(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and returns to home page
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys("title")
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()
        wait_for(lambda: self.browser.find_element_by_link_text("Home")).click()

        # She goes to her profile page linked by her username
        wait_for(lambda: self.browser.find_element_by_id("id_user")).click()
        wait_for(lambda: self.assertIn("edith123's profile", self.browser.title))
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/bloggers/edith123/",
            )
        )

        # She is shown all posts by her
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)

        # Meredith also goes to home page in her browser
        self.browser.quit()
        self.browser = webdriver.Firefox(firefox_binary="/usr/lib/firefox/firefox")

        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="meredith123", password="top_secret")
        self.login(username="meredith123", password="top_secret")

        # She clicks on edith's username to go to her profile page
        wait_for(lambda: self.browser.find_element_by_link_text("edith123")).click()
        wait_for(lambda: self.assertIn("edith123's profile", self.browser.title))
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/bloggers/edith123/",
            )
        )

        # She is shown all posts by edith
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)

    def test_post_title_links_to_post(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and returns to home page
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys("title")
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()
        wait_for(lambda: self.browser.find_element_by_link_text("Home")).click()

        # She goes to her profile page linked by her username
        wait_for(lambda: self.browser.find_element_by_id("id_user")).click()
        wait_for(lambda: self.assertIn("edith123's profile", self.browser.title))
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/bloggers/edith123/",
            )
        )

        # She is shown all posts by her
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)

        # She clicks on one of the posts
        wait_for(lambda: self.browser.find_element_by_link_text("title")).click()

        # She is taken to the post's page
        wait_for(lambda: self.assertIn("title", self.browser.title))
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/blogger/posts/title/"
            )
        )
