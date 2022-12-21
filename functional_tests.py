from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        # The user checks out the home page of a to-do app :
        self.browser.get('http://localhost:8000') 

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy vine for next date' for row in rows),
            "New to-do item did not appear in table"
        )

        # There still is a text box inviting user to type a nex item. The user enters "Buy cheese"
        self.fail('Finish the test!')

        # When user hits Enter the page updates and now lists both items
        # The app generates a URL related to the user's list
        # When visiting said URL the app shows the list    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
