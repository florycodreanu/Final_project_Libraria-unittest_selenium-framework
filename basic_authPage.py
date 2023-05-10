import softest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Authentication(softest.TestCase):
    USERNAME = 'admin'
    PASSWORD = 'admin'
    LOGIN_CONFIRM_TEXT = (By.XPATH, "//div[@class='example']/p")

    def setUp(self) -> None:
        s = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=s)
        self.chrome.maximize_window()
        self.chrome.implicitly_wait(5)

    def tearDown(self) -> None:
        self.chrome.quit()

    def test_auth(self):
        self.chrome.get('https://' + self.USERNAME + ':' + self.PASSWORD + '@the-internet.herokuapp.com/basic_auth')
        sleep(3)
        expected_text = "Congratulations! You must have the proper credentials."
        actual_text = self.chrome.find_element(*self.LOGIN_CONFIRM_TEXT).text
        self.soft_assert(self.assertEqual, expected_text, actual_text, "Error, authentication not succeded")
