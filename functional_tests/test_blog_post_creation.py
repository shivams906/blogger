from .base import *


class BlogTest(FunctionalTest):
    def test_blog_post_creation(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")
        wait_for(lambda: self.assertIn("Home", self.browser.title))
        header = wait_for(lambda: self.browser.find_element_by_tag_name("header"))
        self.assertIn("blogger", header.text)

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She clicks on the add post link
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()

        # She is taken to the add post page
        wait_for(
            lambda: self.assertEqual(
                f"{self.live_server_url}/blogger/posts/add/", self.browser.current_url
            )
        )

        # She writes in the title and content and clicks the publish button
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys("title")
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()

        # She is taken to the newly created post's page
        wait_for(
            lambda: self.assertEqual(
                f"{self.live_server_url}/blogger/posts/title/", self.browser.current_url
            )
        )
        wait_for(lambda: self.assertIn("title", self.browser.title))
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("content", main_content)
        self.assertIn("by edith123", main_content)

        # She logs out
        wait_for(lambda: self.browser.find_element_by_link_text("Logout")).click()

        # She is back on the home page
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/blogger/"
            )
        )

        # There is no Add Post link
        self.assertEqual(
            len(wait_for(lambda: self.browser.find_elements_by_link_text("Add Post"))),
            0,
        )
