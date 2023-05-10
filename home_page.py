import softest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# In aceasta clasa verificam pagina principala si redirectionarea catre alte pagini dupa ce acestea sunt accesate.
# O eroarea a unui test ne aduce modificarea paginii principale sau o eroare de functionare a site-ului


class HomePageTest(softest.TestCase):
    # Variabile in care am salvat metoda de cautare a elementelor in pagina
    HEAD = (By.XPATH, '//h1[text() = "Welcome to the-internet"]')
    AUTH_URL = (By.LINK_TEXT, 'Basic Auth')
    CONTEXT_URL = (By.LINK_TEXT, 'Context Menu')
    FORM_URL = (By.LINK_TEXT, 'Form Authentication')
    ALERTS = (By.LINK_TEXT, 'JavaScript Alerts')
    H_ALERTS = (By.XPATH, '//h3')

    def setUp(self) -> None:
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.get("https://the-internet.herokuapp.com/")
        self.driver.implicitly_wait(5)

    def tearDown(self) -> None:
        self.driver.quit()

    # Verificam daca numele paginii accesate este corect
    def test_page_title(self):
        actual = self.driver.title
        expected = 'The Internet'
        self.soft_assert(self.assertEqual, expected, actual, f'Error: Expected: {expected} Actual: {actual}')

    # Se verifica titlul de pe pagina principala
    def test_head(self):
        expected = 'Welcome to the-internet'
        actual = self.driver.find_element(*self.HEAD).text
        self.soft_assert(self.assertEqual, expected, actual, f'Error: Expected head_title: {expected} Actual: {actual}')

    # Verificam navigarea catre pagina basic_auth dupa url
    def test_basicauth_url(self):
        self.driver.find_element(*self.AUTH_URL).click()
        current_url = self.driver.current_url
        expected_url = 'https://the-internet.herokuapp.com/basic_auth'
        self.assertEqual(current_url, expected_url, f'Error: Url actual{current_url} in loc de {expected_url}')

    # Se verifica url-ul paginii context menu dupa ce am facut clik pe link-ul acesteia
    def test_context_url(self):
        self.driver.find_element(*self.CONTEXT_URL).click()
        current_url = self.driver.current_url
        expected_url = 'https://the-internet.herokuapp.com/context_menu'
        self.assertEqual(current_url, expected_url, f'Error: Url actual{current_url} in loc de {expected_url}')

    # Verificam ca ne aflam pe pagina de logare dupa ce am accesat-o
    def test_form_url(self):
        self.driver.find_element(*self.FORM_URL).click()
        current_url = self.driver.current_url
        expected_url = 'https://the-internet.herokuapp.com/login'
        self.assertEqual(current_url, expected_url, f'Error: Url actual{current_url} in loc de {expected_url}')

    # Verificam daca ne aflam pe pagina de alerte
    def test_jsalert_PAGE(self):
        self.driver.find_element(*self.ALERTS).click()
        expected = 'JavaScript Alerts'
        actual = self.driver.find_element(*self.H_ALERTS).text
        self.soft_assert(self.assertEqual, expected, actual, f'Error: Expected head_title: {expected} Actual: {actual}')
