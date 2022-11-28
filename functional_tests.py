from selenium import webdriver

browser = webdriver.Firefox()

# The user checks out the home page of a to-do app :
browser.get('http://localhost:8000')

# The user can see the page title and header mention to-do lsits
assert 'To-Do' in browser.title

# The user is invited to enter a to-do item
# The user types "Buy vine for next date"
# When user hits Enter the page updates and now lists "1: Buy vine for next date"
# There still is a text box inviting user to type a nex item. The user enters "Buy cheese"
# When user hits Enter the page updates and now lists both items
# The app generates a URL related to the user's list
# When visiting said URL the app shows the list

browser.quit()
