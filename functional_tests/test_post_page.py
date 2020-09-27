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
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys("title")
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

    def test_delete_post_link(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post
        wait_for(lambda: self.browser.find_element_by_link_text("Add Post")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_title")).send_keys("title")
        wait_for(lambda: self.browser.find_element_by_id("id_content")).send_keys(
            "content"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()

        # She clicks on the delete link
        wait_for(lambda: self.browser.find_element_by_link_text("delete")).click()

        # She is taken to a page to confirm deletion
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/posts/title/delete/",
            )
        )
        wait_for(lambda: self.assertIn("delete title", self.browser.title))

        # She sees a link to cancel the deletion and clicks on it
        wait_for(lambda: self.browser.find_element_by_link_text("cancel")).click()

        # She is taken back to post's page
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/blogger/posts/title/"
            )
        )

        # She clicks on the delete link again
        wait_for(lambda: self.browser.find_element_by_link_text("delete")).click()

        # She clicks on confirm to delete
        wait_for(lambda: self.browser.find_element_by_id("id_confirm")).click()

        # She is redirected to home page and her post is not there
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/blogger/"
            )
        )

        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        wait_for(lambda: self.assertNotIn("title", main_content))
