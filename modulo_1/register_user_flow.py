import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class RegisterUserFlow:
    """Responsável por executar o fluxo completo de cadastro do usuário."""

    def __init__(self, driver, wait, element_actions, validator):
        self.driver = driver
        self.wait = wait
        self.element_actions = element_actions
        self.validator = validator

    def open_home_page(self):
        """Abre a página inicial e valida o título."""
        self.driver.get("http://automationexercise.com")
        assert "Automation Exercise" in self.driver.title

    def go_to_signup_login(self):
        """Abre a tela de Signup / Login."""
        self.element_actions.safe_click(By.LINK_TEXT, "Signup / Login")

        signup_header = self.wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, "//h2[text()='New User Signup!']")
            )
        )
        assert signup_header.is_displayed()

    def start_signup(self, name, email):
        """Preenche nome e email e inicia o cadastro."""
        self.element_actions.safe_send_keys(By.NAME, "name", name)
        self.element_actions.safe_send_keys(
            By.XPATH,
            "//input[@data-qa='signup-email']",
            email
        )
        self.element_actions.safe_click(
            By.XPATH,
            "//button[@data-qa='signup-button']"
        )

    def fill_account_information(self):
        """Preenche informações iniciais da conta."""
        account_info = self.wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, "//b[text()='Enter Account Information']")
            )
        )
        assert account_info.is_displayed()

        self.element_actions.safe_click(By.ID, "id_gender2")
        self.element_actions.safe_send_keys(By.ID, "password", "Senha@123")
        self.element_actions.safe_select_by_visible_text(By.ID, "days", "22")
        self.element_actions.safe_select_by_visible_text(By.ID, "months", "December")
        self.element_actions.safe_select_by_visible_text(By.ID, "years", "2001")
        self.element_actions.safe_click(By.ID, "newsletter")
        self.element_actions.safe_click(By.ID, "optin")

    def fill_address_information(self):
        """Preenche as informações de endereço."""
        self.element_actions.safe_send_keys(By.ID, "first_name", "Laiana")
        self.element_actions.safe_send_keys(By.ID, "last_name", "Cavalcante")
        self.element_actions.safe_send_keys(By.ID, "company", "UFAM")
        self.element_actions.safe_send_keys(By.ID, "address1", "Rua Rio Japura, 336")
        self.element_actions.safe_send_keys(By.ID, "address2", "Bairro Centro")
        self.element_actions.safe_select_by_visible_text(By.ID, "country", "India")
        self.element_actions.safe_send_keys(By.ID, "state", "Amazonas")
        self.element_actions.safe_send_keys(By.ID, "city", "Iranduba")
        self.element_actions.safe_send_keys(By.ID, "zipcode", "69000000")
        self.element_actions.safe_send_keys(By.ID, "mobile_number", "92999999999")

    def create_account(self):
        """Cria a conta e valida a mensagem de sucesso."""
        self.element_actions.safe_click(
            By.XPATH,
            "//button[@data-qa='create-account']"
        )

        created_text = self.wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, "//b[text()='Account Created!']")
            )
        )
        assert created_text.is_displayed()

    def continue_after_creation(self):
        """Clica em Continue após criar conta e valida login."""
        self.element_actions.safe_click(
            By.XPATH,
            "//a[@data-qa='continue-button']"
        )

        logged_in_text = self.validator.wait_for_logged_in()
        assert logged_in_text.is_displayed()

    def delete_account(self):
        """Exclui a conta criada e valida a exclusão."""
        self.element_actions.safe_click(By.LINK_TEXT, "Delete Account")

        deleted_text = self.validator.wait_for_account_deleted()
        assert deleted_text.is_displayed()

        self.element_actions.safe_click(
            By.XPATH,
            "//a[@data-qa='continue-button']"
        )

    def execute(self):
        """Executa o fluxo completo."""
        user_name = "Laiana"
        user_email = f"laianacavalcante{int(time.time())}@gmail.com"

        self.open_home_page()
        self.go_to_signup_login()
        self.start_signup(user_name, user_email)
        self.fill_account_information()
        self.fill_address_information()
        self.create_account()
        self.continue_after_creation()
        self.delete_account()