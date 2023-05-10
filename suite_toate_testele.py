import unittest
import HtmlTestRunner

from basic_authPage import Authentication
from context_menu_page import ContextMenu
from home_page import HomePageTest
from login_page import Login
from tratare_alerte import Alerts


class TestSuite(unittest.TestCase):

    def test_suite(self):
        teste_de_rulat = unittest.TestSuite()
        teste_de_rulat.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(Alerts),
            unittest.defaultTestLoader.loadTestsFromTestCase(Authentication),
            unittest.defaultTestLoader.loadTestsFromTestCase(ContextMenu),
            unittest.defaultTestLoader.loadTestsFromTestCase(HomePageTest),
            unittest.defaultTestLoader.loadTestsFromTestCase(Login)
        ])
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title='RaportTeste',
            report_name='Smoke Test Result'
        )

        runner.run(teste_de_rulat)
