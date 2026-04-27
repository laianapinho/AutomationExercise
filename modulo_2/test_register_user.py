# Importa o módulo unittest para criar testes automatizados
import unittest

# Importa a classe responsável por criar o navegador
from browser_factory import BrowserFactory

# Importa a classe responsável por criar os dados de usuário
from user_data_factory import UserDataFactory

# Importa a classe que representa as ações feitas na página
from automation_exercise_page import AutomationExercisePage


# Define a classe de teste de cadastro de usuário
class TestRegisterUser(unittest.TestCase):

    # Método executado antes de cada teste
    def setUp(self):

        # Cria o navegador Chrome configurado
        self.driver = BrowserFactory.create_chrome_driver()

        # Cria o objeto de espera explícita
        self.wait = BrowserFactory.create_wait(self.driver)

        # Cria o objeto da página, passando driver e wait
        self.page = AutomationExercisePage(self.driver, self.wait)

    # Método de teste de cadastro de usuário
    def test_register_user(self):

        # Cria os dados do usuário de teste
        user = UserDataFactory.create_user()

        # Abre a página inicial do site
        self.page.open_home_page()

        # Verifica se a página inicial está visível
        self.assertTrue(self.page.is_home_page_visible())

        # Realiza o cadastro do usuário
        self.page.register_user(user)

        # Espera aparecer o texto de usuário logado
        logged_in_text = self.page.wait_for_logged_in()

        # Verifica se o texto de usuário logado está visível
        self.assertTrue(logged_in_text.is_displayed())

        # Faz logout do usuário após o cadastro
        self.page.logout_user()

    # Método executado depois de cada teste
    def tearDown(self):

        # Fecha o navegador
        self.driver.quit()


# Verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":

    # Executa os testes do arquivo
    unittest.main()