from .base import *


class RegistrationTest(FunctionalTest):
    def test_signup_login_logout(self):
        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/blogger/")
        wait_for(lambda: self.assertIn("blogger", self.browser.title))

        # She finds a link to signup page and clicks on it
        wait_for(lambda: self.browser.find_element_by_link_text("Sign Up")).click()

        # She is taken to the signup page
        wait_for(lambda: self.assertIn("Sign Up", self.browser.title))

        # She enters her desired username and password and clicks on signup
        wait_for(lambda: self.browser.find_element_by_id("id_username")).send_keys(
            "edith123"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password1")).send_keys(
            "top_secret"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password2")).send_keys(
            "top_secret"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_signup")).click()

        # She is taken to login page on successful signup
        wait_for(lambda: self.assertIn("Login", self.browser.title))

        # She enters her username and password and clicks on login
        wait_for(lambda: self.browser.find_element_by_id("id_username")).send_keys(
            "edith123"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password")).send_keys(
            "top_secret"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_login")).click()

        # She is taken to the home page and her name appears on the page
        wait_for(lambda: self.assertIn("Home", self.browser.title))
        content = wait_for(lambda: self.browser.find_element_by_tag_name("body").text)
        self.assertIn("edith123", content)

        # She clicks on the logout link
        wait_for(lambda: self.browser.find_element_by_link_text("Logout")).click()

        # She logs in again to see the home page
        wait_for(lambda: self.browser.find_element_by_link_text("Login")).click()
        wait_for(lambda: self.browser.find_element_by_id("id_username")).send_keys(
            "edith123"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password")).send_keys(
            "top_secret"
        )
        wait_for(lambda: self.browser.find_element_by_id("id_login")).click()
        wait_for(lambda: self.assertIn("Home", self.browser.title))
        body = wait_for(lambda: self.browser.find_element_by_tag_name("body"))
        self.assertIn("edith123", body.text)
