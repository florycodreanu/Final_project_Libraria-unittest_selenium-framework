# import unittest
import unittest

import softest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


class Login(softest.TestCase):
    FORM_AUTHENTICATION_LINK = (By.XPATH, '//a[@href="/login"]')
    H_ELEMENT = (By.XPATH, '//h2')
    LOGIN_BUTTON = (By.XPATH, '//button[@type="submit"]')
    HREF_LINK = (By.XPATH, '//a[text()="Elemental Selenium"]')
    USER_NAME = (By.ID, 'username')
    PASSWORD = (By.ID, 'password')
    ERROR_MESSAGE_1 = (By.XPATH, '//div[@id="flash"]')
    ERROR_MESSAGE_2 = (By.XPATH, '//div[@id="flash"][(contains(text(),"Your username is invalid"))]')
    ERROR_CLOSED = (By.XPATH, '//a[@class="close"]')
    LABEL_LIST = (By.XPATH, '//label')
    SUCCESS_MESSAGE = (By.XPATH, '//div[@class="flash success"]')
    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')
    ELEM_H4 = (By.TAG_NAME, 'h4')

    def setUp(self):
        self.chrome = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.chrome.maximize_window()
        self.chrome.get('https://the-internet.herokuapp.com/')
        self.chrome.find_element(*self.FORM_AUTHENTICATION_LINK).click()
        self.chrome.implicitly_wait(10)

    def tearDown(self):
        self.chrome.quit()

    # Verificare titlul fisat pe pagina de login
    def test_head(self):
        actual = self.chrome.find_element(*self.H_ELEMENT).text
        expected = 'Login Page'
        self.soft_assert(self.assertEqual, actual, expected, f'Error: Expected: {expected} Actual: {actual}')

    # Verificare Login button afisat
    def test_login_displayed(self):
        button = self.chrome.find_element(*self.LOGIN_BUTTON)
        self.soft_assert(self.assertTrue, button.is_displayed(), 'Butonul de LOGIN nu este vizibil')

    # Verificare ancora elementului de la baza paginii
    # @unittest.skip
    # Decoratorul de mai sus poate fi folosit pentru a sari peste acest test daca se sterge semnul"#"
    def test_href(self):
        actual_link = self.chrome.find_element(*self.HREF_LINK).get_attribute('href')
        self.soft_assert(self.assertEqual, actual_link, 'http://elementalselenium.com/', 'Link-ul este gresit')

    # Verificare mesaj cand apasam butonul de login
    def test_error_displayed(self):
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        error = WebDriverWait(self.chrome, 5).until(ec.presence_of_element_located(self.ERROR_MESSAGE_1))
        self.soft_assert(self.assertTrue, error.is_displayed(), 'Eroarea nu este vizibila')

    # Verificare mesaj eroare user si pass incorecte
    def test_mesaj_eroare(self):
        self.chrome.find_element(*self.USER_NAME).send_keys('tom')
        self.chrome.find_element(*self.PASSWORD).send_keys('SuperSecret!')
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        actual = self.chrome.find_element(*self.ERROR_MESSAGE_2).text
        expected = 'Your username is invalid!'
        self.soft_assert(self.assertEqual, actual, expected, 'Mesajul de eroare nu este afisat!')

    # Verificare inchidere mesaj eroare
    def test_inchidere_mesaj_eroare(self):
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        sleep(5)
        self.chrome.find_element(*self.ERROR_CLOSED).click()
        sleep(5)
        try:
            self.chrome.find_element(*self.ERROR_CLOSED)
        except NoSuchElementException:
            print("The text is not visible on the page! It's ok")

    # Verificare label(numele de deasupra casutelor) sunt cele asteptate
    def test_lista_label(self):
        elem_lista = self.chrome.find_elements(*self.LABEL_LIST)
        user = False
        password = False
        for t in elem_lista:
            if t.text == 'Username':
                user = True
            elif t.text == 'Password':
                password = True
        self.assertTrue(user, 'Textul Username nu se regaseste in lista')
        self.assertTrue(password, 'Textul Password nu se regaseste in lista')

    # Verificare noul url dupa logare sa contina secure
    # Verificam ca dupa logare sa avem mesajul de logare cu succes afisat iar acesta sa contina: 'secure area!'
    def test_verif_secure(self):
        self.chrome.find_element(*self.USER_NAME).send_keys('tomsmith')
        self.chrome.find_element(*self.PASSWORD).send_keys('SuperSecretPassword!')
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        url_dupa_logare = self.chrome.current_url
        self.assertTrue("/secure" in url_dupa_logare, 'Noul url nu contine secure')
        WebDriverWait(self.chrome, 10).until(ec.presence_of_element_located(self.SUCCESS_MESSAGE))
        message = self.chrome.find_element(*self.SUCCESS_MESSAGE)
        self.assertTrue(message.is_displayed(), 'Mesajul asteptat nu este afisat')
        self.assertTrue('secure area!' in message.text, 'Textul cautat nu se afla in mesajul afisat')

    # Verificare login - logout
    def test_verif_login_logout(self):
        self.chrome.find_element(*self.USER_NAME).send_keys('tomsmith')
        self.chrome.find_element(*self.PASSWORD).send_keys('SuperSecretPassword!')
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        self.chrome.find_element(*self.LOGOUT_BUTTON).click()
        sleep(5)
        url_dupa_delogare = self.chrome.current_url
        expected_url = 'https://the-internet.herokuapp.com/login'
        self.assertEqual(url_dupa_delogare, expected_url, f'Invalid url!Actual:{url_dupa_delogare}, Exp:{expected_url}')

    # Brute force password
    @unittest.skip
    def test_brute_force_pass(self):
        var_parole = self.chrome.find_element(*self.ELEM_H4).text.split()
        for password in var_parole:
            self.chrome.find_element(*self.USER_NAME).send_keys('tomsmith')
            self.chrome.find_element(*self.PASSWORD).send_keys(password)
            self.chrome.find_element(*self.LOGIN_BUTTON).click()
            url = self.chrome.current_url
            if "secure" in url:
                print(f'Parola secreta este {password}')
                break
            else:
                print("Nu am reusit sa gasesc parola. Continuam cautarea")
        self.assertTrue('secure' in self.chrome.current_url, 'Nu am reusit sa gasesc parola')
