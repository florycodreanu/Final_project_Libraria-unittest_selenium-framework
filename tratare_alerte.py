import softest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


class Alerts(softest.TestCase):
    ALERT_BUTTON = (By.XPATH, '//*[text()="Click for JS Alert"]')
    CONFIRM_BUTTON = (By.XPATH, "//*[text()='Click for JS Confirm']")
    PROMPT_BUTTON = (By.XPATH, "//*[text()='Click for JS Prompt']")
    ALERT_MESSAGE = (By.ID, "result")
    ALERTS = (By.LINK_TEXT, 'JavaScript Alerts')

    def setUp(self) -> None:
        s = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=s)
        self.chrome.maximize_window()
        self.chrome.get("https://the-internet.herokuapp.com")
        self.chrome.find_element(*self.ALERTS).click()
        self.chrome.implicitly_wait(5)

    def tearDown(self) -> None:
        self.chrome.quit()

    def test_js_alert_accept(self):
        self.chrome.find_element(*self.ALERT_BUTTON).click()
        sleep(2)
        alert = self.chrome.switch_to.alert  # Ne mutam in fereastra alerta si o salvam intr-o variabila
        alert.accept()  # acceptam alerta folosind metoda accept()
        alert_text = self.chrome.find_element(*self.ALERT_MESSAGE).text  # extragem textul dupa acc alertei
        print(f'Mesajul dupa acceptarea alertei: {alert_text}')
        expected_text = 'You successfully clicked an alert'
        self.soft_assert(self.assertEqual, expected_text, alert_text, f'ERROR: Incorrect result!')

    def test_js_confirm_ok(self):
        self.chrome.find_element(*self.CONFIRM_BUTTON).click()
        confirm = self.chrome.switch_to.alert
        confirm.accept()
        sleep(2)
        confirm_text = self.chrome.find_element(*self.ALERT_MESSAGE)
        print(f'Mesajul dupa acceptarea alertei: {confirm_text}')
        expected_text = 'You clicked: Ok'
        self.soft_assert(self.assertEqual, expected_text, confirm_text, f'ERROR: Incorrect result!')

    def test_js_confirm_cancel(self):
        self.chrome.find_element(*self.CONFIRM_BUTTON).click()
        js_confirm = self.chrome.switch_to.alert
        js_confirm.dismiss()
        js_confirm_text = self.chrome.find_element(*self.ALERT_MESSAGE).text
        print(f'Mesajul dupa acceptarea alertei: {js_confirm_text}')
        expected_text = 'You clicked: Cancel'
        self.soft_assert(self.assertEqual, expected_text, js_confirm_text, f'ERROR: Incorrect result!')

    def test_js_prompt_accept_no_text_insert(self):
        self.chrome.find_element(*self.PROMPT_BUTTON).click()
        js_prompt = self.chrome.switch_to.alert
        js_prompt.accept()
        js_prompt_text = self.chrome.find_element(*self.ALERT_MESSAGE).text
        print(f'Mesajul dupa acceptarea alertei: {js_prompt_text}')
        expected_text = 'You entered:'
        self.soft_assert(self.assertEqual, expected_text, js_prompt_text, f'ERROR: Incorrect result!')

    def test_js_prompt_cancel_no_text_inserted(self):
        self.chrome.find_element(*self.PROMPT_BUTTON).click()
        js_prompt = self.chrome.switch_to.alert
        js_prompt.dismiss()
        js_prompt_text = self.chrome.find_element(*self.ALERT_MESSAGE).text
        print(f'Mesajul dupa acceptarea alertei: {js_prompt_text}')
        expected_text = 'You entered: null'
        self.soft_assert(self.assertEqual, expected_text, js_prompt_text, f'ERROR: Incorrect result!')

    def test_js_prompt_accept_text_insert(self):
        self.chrome.find_element(*self.PROMPT_BUTTON).click()
        js_prompt = self.chrome.switch_to.alert
        js_prompt.send_keys("test")
        js_prompt.accept()
        js_prompt_text = self.chrome.find_element(*self.ALERT_MESSAGE).text
        print(f'Mesajul dupa acceptarea alertei: {js_prompt_text}')
        expected_text = 'You entered: test'
        self.soft_assert(self.assertEqual, expected_text, js_prompt_text, f'ERROR: Incorrect result!')

    def test_js_prompt_cancel_text_inserted(self):
        self.chrome.find_element(*self.PROMPT_BUTTON).click()
        js_prompt = self.chrome.switch_to.alert
        js_prompt.send_keys("test")
        js_prompt.dismiss()
        alert_text = self.chrome.find_element(*self.ALERT_MESSAGE).text
        print(f'Mesajul dupa acceptarea alertei: {alert_text}')
        expected_text = 'You entered: null'
        self.soft_assert(self.assertEqual, expected_text, alert_text, f'ERROR: Incorrect result!')
