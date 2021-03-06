from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        # Edith goes to the homepage and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The homepage refreshes, and there is an error message saying that
        # list items can't be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, shich now works
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')

        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Buy milk')
            self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):

        # Edith goes to the homepage and start new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy coke')
        self.get_item_input_box().send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Buy coke')

        # She entered same item accidentally
        self.get_item_input_box().send_keys('Buy coke')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # There is an error which is helpful
        self.check_for_row_in_list_table('1: Buy coke')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You already have this item")
