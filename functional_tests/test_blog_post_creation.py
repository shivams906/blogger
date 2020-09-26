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
                f"{self.live_server_url}/blogger/add/", self.browser.current_url
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
        body = wait_for(lambda: self.browser.find_element_by_tag_name("body")).text
        self.assertIn("title", body)
        self.assertIn("content", body)
