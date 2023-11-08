from selenium import webdriver
from selenium.webdriver.common.by import By

class ToGo:
    def __init__(self):
        self.driver = None

    def setup(self):
        self.driver = webdriver.Chrome()

    def teardown(self):
        if self.driver:
            self.driver.quit()

    def login(self, username, password):
        self.driver.get("https://www.myjobtogo.com/Web/Desktop/default.aspx")
        self.driver.set_window_size(1099, 644)
        self.driver.find_element(By.CSS_SELECTOR, "#MainContentPlaceHolder_UsernameTextBox").send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR, "#MainContentPlaceHolder_PasswordTextBox").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".loginbutton").click()
        self.driver.find_element(By.CSS_SELECTOR, "#MainContentPlaceHolder_CancelButton").click()
        self.driver.find_element(By.LINK_TEXT, "My Schedule").click()

    def get_schedule(self):
        return self.driver.find_element(By.XPATH, "//table[@class='schedule']").text

    def next_week_exists(self):
        return len(self.driver.find_elements(By.ID, "nextwk")) > 0

def getToGo(username, password):
    mylist = []
    togo = ToGo()
    try:
        togo.setup()
        togo.login(username, password)
        mylist.append(togo.get_schedule())

        if togo.next_week_exists():
            togo.driver.find_element(By.ID, "nextwk").click()
            mylist.append(togo.get_schedule())
    finally:
        
        togo.teardown()
         
    return mylist
# Usage example:
