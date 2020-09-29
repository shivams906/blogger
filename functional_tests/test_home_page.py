from .base import *
from django.utils.text import slugify


class HomePageTest(FunctionalTest):
    def test_home_page_shows_posts_by_all_users(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and returns to home page
        self.create_a_post(title="Edith's title", content='content')
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
        self.signup(username="meredith123", password="top_secret")
        self.login(username="meredith123", password="top_secret")
        self.create_a_post(title="Meredith's title", content='content')
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

        meredith_browser.quit()

    def test_post_title_links_to_post_page(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and returns to home page
        self.create_a_post(title='title', content='content')
        wait_for(lambda: self.browser.find_element_by_link_text("Home")).click()

        # She clicks on the title of her post
        wait_for(lambda: self.browser.find_element_by_link_text("title")).click()

        # She is taken to the post's page

        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/posts/{slugify('title')}/",
            )
        )

        wait_for(lambda: self.assertIn("title", self.browser.title))
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("content", main_content)
        self.assertIn("by edith123", main_content)

    def test_post_author_links_to_author_page(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")

        # She signs up and logs in
        self.signup(username="edith123", password="top_secret")
        self.login(username="edith123", password="top_secret")

        # She creates a post and returns to home page
        self.create_a_post(title='title', content='content')
        wait_for(lambda: self.browser.find_element_by_link_text("Home")).click()

        # She clicks on the post's author's name (her name)
        wait_for(lambda: self.browser.find_element_by_link_text("edith123")).click()

        # She is taken to the author's page
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/blogger/bloggers/edith123/",
            )
        )
        wait_for(lambda: self.assertIn("edith123's profile", self.browser.title))
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("edith123", main_content)
