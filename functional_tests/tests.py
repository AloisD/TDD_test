from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # The user checks out the home page of a to-do app :
        self.browser.get(self.live_server_url) 

        # The user can see the page title and header mention to-do lsits
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # The user is invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # The user types "Buy vine for next date"
        inputbox.send_keys('Buy vine for next date')

        # When user hits Enter the page updates and now lists "1: Buy vine for next date"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy vine for next date')

        # There still is a text box inviting user to type a nex item. The user enters "Buy cheese"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy cheese')
        inputbox.send_keys(Keys.ENTER)

        # When user hits Enter the page updates and now lists both items
        self.wait_for_row_in_list_table('1: Buy vine for next date')
        self.wait_for_row_in_list_table('2: Buy cheese')
        
        # Satisfied, our first user goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User n°1 starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy vine for next date')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy vine for next date')

        # User n°1 notices that his list has a unique URL
        user_n1_list_url = self.browser.current_url
        self.assertRegex(user_n1_list_url, '/lists/.+')

        # User n°2 comes along

        ## we need a new browser session to make sure that no information
        ## of user n°1 is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User n°2 visits the home page. There is no sign of user n°1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy vine for next date', page_text)
        self.assertNotIn('Buy cheese', page_text)

        # User n°2 starts a new listby entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Iron my shirt')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Iron my shirt')

        # User n°2 gets his own unique url
        user_n2_list_url = self.browser.current_url
        self.assertRegex(user_n2_list_url, '/lists/.+')
        self.assertNotEqual(user_n2_list_url, user_n1_list_url)

        # Again, no trace of user n°1's list here
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy vine for next date', page_text)
        self.assertIn('Iron my shirt', page_text)

        # Satisfied, both users go back to sleep
