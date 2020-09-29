from .base import *


class PostPageTest(FunctionalTest):
    def test_edit_post_link(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post
        self.create_a_post(title="title", content="content")

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
        self.create_a_post(title="title", content="content")

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

    def test_only_authors_can_see_the_link_to_edit_or_delete(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and is taekn to post's page
        self.create_a_post(title="title", content="content")

        # She sees the link to edit and delete
        wait_for(lambda: self.browser.find_element_by_link_text("edit"))
        wait_for(lambda: self.browser.find_element_by_link_text("delete"))

        # She closes the browser
        self.browser.quit()

        # Meredith opens her browser
        self.browser = webdriver.Firefox(firefox_binary="/usr/lib/firefox/firefox")

        # She goes to the homepage
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She goes to edith's post
        wait_for(lambda: self.browser.find_element_by_link_text("title")).click()

        # She doesn't see edit or delete link
        wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("edit"), []
            )
        )
        wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("delete"), []
            )
        )

        # She signs up and logs in
        self.signup(username="meredith123", password="top_secret")
        self.login(username="meredith123", password="top_secret")

        # She goes to edith's post again
        wait_for(lambda: self.browser.find_element_by_link_text("title")).click()

        # She doesn't see edit or delete link
        wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("edit"), []
            )
        )
        wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("delete"), []
            )
        )

    def test_author_name_links_to_author_page(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and is taken to post's page
        self.create_a_post(title="title", content="content")

        # She sees the link to edit and delete
        wait_for(lambda: self.browser.find_element_by_link_text("edit"))
        wait_for(lambda: self.browser.find_element_by_link_text("delete"))

        # She closes the browser
        self.browser.quit()

        # Meredith opens her browser
        self.browser = webdriver.Firefox(firefox_binary="/usr/lib/firefox/firefox")

        # She goes to the homepage
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She goes to edith's post
        wait_for(lambda: self.browser.find_element_by_link_text("title")).click()

        # She clicks on edith's name
        wait_for(lambda: self.browser.find_element_by_link_text("edith123")).click()

        # She is taken to edith's profile page
        wait_for(lambda: self.assertIn("edith123's profile", self.browser.title))
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/bloggers/edith123/",
            )
        )

    def test_can_comment_on_the_post(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and is taekn to post's page
        self.create_a_post(title="title", content="content")

        # She clicks on add comment link
        wait_for(lambda: self.browser.find_element_by_link_text("add comment")).click()

        # She is on the add comment page
        wait_for(lambda: self.assertIn("Add comment", self.browser.title))

        # She writes her comment and clicks on submit
        wait_for(lambda: self.browser.find_element_by_id("id_comment_text")).send_keys(
            "edith's comment"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()

        # Her comment is now shown below the post
        comment = wait_for(lambda: self.browser.find_element_by_id("id_comment")).text
        self.assertIn("edith's comment", comment)

        # She closes the browser
        self.browser.quit()

        # Meredith opens her browser
        self.browser = webdriver.Firefox(firefox_binary="/usr/lib/firefox/firefox")

        # She goes to the homepage
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="meredith123", password="top_secret")
        self.login(username="meredith123", password="top_secret")

        # She goes to edith's post
        wait_for(lambda: self.browser.find_element_by_link_text("title")).click()

        # She also clicks on add comment link
        wait_for(lambda: self.browser.find_element_by_link_text("add comment")).click()

        # She writes her comment and clicks on submit
        wait_for(lambda: self.browser.find_element_by_id("id_comment_text")).send_keys(
            "meredith's comment"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_submit")).click()

        # Her comment is now shown below edith's comment
        comments = wait_for(lambda: self.browser.find_elements_by_id("id_comment"))
        self.assertEqual("edith's comment", comments[0].text)
        self.assertEqual("meredith's comment", comments[1].text)

        # She closes the browser
        self.browser.quit()
