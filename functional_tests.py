from selenium import webdriver
import unittest

class NewViwitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_list_and_retrieve_it(self):
        # The user checks out the home page of a to-do app :
        self.browser.get('http://localhost:8000') 

        # The user can see the page title and header mention to-do lsits
        self.assertIn('To-Do', self.browser.title)
        self.fail("Finish the test!")

        # The user is invited to enter a to-do item
        # The user types "Buy vine for next date"
        # When user hits Enter the page updates and now lists "1: Buy vine for next date"
        # There still is a text box inviting user to type a nex item. The user enters "Buy cheese"
        # When user hits Enter the page updates and now lists both items
        # The app generates a URL related to the user's list
        # When visiting said URL the app shows the list    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
