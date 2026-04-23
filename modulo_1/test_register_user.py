import unittest
from selenium.webdriver.support.ui import WebDriverWait

from browser_factory import BrowserFactory
from popup_handler import PopupHandler
from element_actions import ElementActions
from account_page_validator import AccountPageValidator
from register_user_flow import RegisterUserFlow


class TestRegisterUser(unittest.TestCase):
    """Classe de teste que orquestra a execução do cenário."""

    def setUp(self):
        # Cria o navegador
        self.driver = BrowserFactory.create_chrome_driver()

        # Cria o mecanismo de espera explícita
        self.wait = WebDriverWait(self.driver, 20)

        # Cria o responsável por tratar popups e banners
        self.popup_handler = PopupHandler(self.driver)

        # Cria o responsável por ações seguras nos elementos
        self.element_actions = ElementActions(
            self.driver,
            self.wait,
            self.popup_handler
        )

        # Cria o responsável pelas validações de estado da página
        self.validator = AccountPageValidator(
            self.driver,
            self.wait,
            self.popup_handler
        )

        # Cria o fluxo principal de cadastro
        self.register_flow = RegisterUserFlow(
            self.driver,
            self.wait,
            self.element_actions,
            self.validator
        )

    def test_register_user(self):
        # Executa o fluxo completo
        self.register_flow.execute()

    def tearDown(self):
        # Se houver erro, salva screenshot para depuração
        try:
            for _, error in self._outcome.result.errors:
                if error:
                    self.driver.save_screenshot("erro_teste.png")
                    break
        except Exception:
            pass

        # Fecha o navegador
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()