import time

import softest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ContextMenu(softest.TestCase):
    BOX = (By.ID, "hot-spot")

    def setUp(self) -> None:
        s = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=s)
        self.chrome.maximize_window()
        self.chrome.get("https://the-internet.herokuapp.com/context_menu")
        self.chrome.implicitly_wait(2)

    def tearDown(self) -> None:
        self.chrome.quit()

    def test_context(self):
        action = ActionChains(self.chrome)  # Ne ajuta sa dam click dr
        elem = self.chrome.find_element(*self.BOX)
        time.sleep(2)
        action.context_click(elem).perform()
        time.sleep(2)
        alert = self.chrome.switch_to.alert
        text = alert.text
        self.soft_assert(self.assertEqual, text, "You selected a context menu", "Error, text is incorrect")
        alert.accept()
        time.sleep(2)

