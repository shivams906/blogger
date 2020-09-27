from .base import *


class PostPageTest(FunctionalTest):
    def test_edit_post_link(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys(
            "Edith's title"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()

        # She clicks on the edit link
        wait_for(lambda: self.browser.find_element_by_link_text("edit")).click()

        # She changes the content and submits
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "changed content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()

        # She sees the changed post
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("changed content", main_content)
