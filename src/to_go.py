from selenium import webdriver
from selenium.webdriver.common.by import By
from ref import TO_GO_USERNAME,TO_GO_PASSWORD
class ToGo:
    '''Requires username and password for togo
    needs setup(), login(), and getSchedule()
    or just run main()'''

    def __init__(self, username=TO_GO_USERNAME , password=TO_GO_PASSWORD):
        self.driver = None
        self.username = username
        self.password = password
        self._weekList = []
    def setup(self):
        self.driver = webdriver.Chrome()

    def closeDriver(self) -> None:
        if self.driver:
            self.driver.quit()
            
    def login(self) -> None:
        self.driver.get("https://www.myjobtogo.com/Web/Desktop/default.aspx")
        self.driver.set_window_size(1099, 644)
        self.driver.find_element(By.CSS_SELECTOR, "#MainContentPlaceHolder_UsernameTextBox").send_keys(self.username)
        self.driver.find_element(By.CSS_SELECTOR, "#MainContentPlaceHolder_PasswordTextBox").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".loginbutton").click()
        self.driver.find_element(By.CSS_SELECTOR, "#MainContentPlaceHolder_CancelButton").click()
        self.driver.find_element(By.LINK_TEXT, "My Schedule").click()

    def get_schedules(self) -> list:
        _scrape = self.driver.find_element(By.XPATH, "//table[@class='schedule']").text
        # return self.driver.find_element(By.XPATH, "//table[@class='schedule']").text
        self._weekList.append(_scrape)
        self._week2Link = self.driver.find_elements(By.ID, "nextwk")
        
        if len(self._week2Link) > 0:
            self._week2Link[0].click()
            _scrape = self.driver.find_element(By.XPATH, "//table[@class='schedule']").text
            self._weekList.append(_scrape)
        
        self.closeDriver()
        return self._weekList
        
def main():
    tg = ToGo()
    
    tg.setup()
    tg.login()
    return tg.get_schedules()
    #tg.closeDriver()
    

if __name__ == 'main':
    main()         