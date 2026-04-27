# Importa o módulo time para usar pequenas pausas no código
import time

# Importa By para localizar elementos na página
from selenium.webdriver.common.by import By

# Importa Select para manipular campos do tipo <select>
from selenium.webdriver.support.ui import Select

# Importa as condições esperadas do Selenium
from selenium.webdriver.support import expected_conditions as EC

# Importa exceções específicas do Selenium
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException


# Define uma classe que representa as ações feitas no site Automation Exercise
class AutomationExercisePage:

    # Método construtor da classe
    def __init__(self, driver, wait):

        # Guarda o navegador recebido para ser usado nos métodos
        self.driver = driver

        # Guarda o objeto de espera explícita recebido
        self.wait = wait

    # Método para abrir a página inicial do site
    def open_home_page(self):

        # Acessa a URL principal do site
        self.driver.get("http://automationexercise.com")

    # Método para verificar se a página inicial está visível
    def is_home_page_visible(self):

        # Retorna True se o título da página contém o texto esperado
        return "Automation Exercise" in self.driver.title

    # Método para esconder banners fixos na parte inferior da tela
    def hide_bottom_banner(self):

        # Executa um código JavaScript dentro da página
        self.driver.execute_script("""
            const all = document.querySelectorAll('body *');

            all.forEach(element => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();

                const fixed_like = style.position === 'fixed' || style.position === 'sticky';
                const near_bottom = rect.bottom >= window.innerHeight - 5;
                const big_enough = rect.width > 400 && rect.height > 80;

                if (fixed_like && near_bottom && big_enough) {
                    element.style.display = 'none';
                }
            });
        """)

    # Método que tenta clicar no botão de fechar anúncio no contexto atual
    def try_click_close_in_current_context(self):

        # Lista de possíveis seletores para botões de fechar anúncio
        close_button_selectors = [

            # Procura elemento pelo ID dismiss-button-element
            (By.ID, "dismiss-button-element"),

            # Procura elemento pelo ID dismiss-button
            (By.ID, "dismiss-button"),

            # Procura elemento pelo XPath com ID dismiss-button-element
            (By.XPATH, "//*[@id='dismiss-button-element']"),

            # Procura elemento pelo XPath com ID dismiss-button
            (By.XPATH, "//*[@id='dismiss-button']"),

            # Procura qualquer elemento com texto Close
            (By.XPATH, "//*[normalize-space(text())='Close']"),

            # Procura uma div com texto Close
            (By.XPATH, "//div[normalize-space()='Close']"),

            # Procura um span com texto Close
            (By.XPATH, "//span[normalize-space()='Close']"),

            # Procura um botão com texto Close
            (By.XPATH, "//button[normalize-space()='Close']"),

            # Procura um link com texto Close
            (By.XPATH, "//a[normalize-space()='Close']"),
        ]

        # Percorre cada seletor da lista
        for by, value in close_button_selectors:

            # Tenta encontrar e clicar no botão de fechar
            try:

                # Busca todos os elementos que combinam com o seletor atual
                elements = self.driver.find_elements(by, value)

                # Percorre todos os elementos encontrados
                for element in elements:

                    # Verifica se o elemento está visível na tela
                    if element.is_displayed():

                        # Tenta clicar normalmente no elemento
                        try:

                            # Centraliza o elemento na tela
                            self.scroll_center(element)

                            # Clica no elemento
                            element.click()

                            # Aguarda 1 segundo para o anúncio fechar
                            time.sleep(1)

                            # Retorna True indicando que conseguiu fechar
                            return True

                        # Caso o clique normal falhe
                        except Exception:

                            # Tenta clicar usando JavaScript
                            try:

                                # Executa clique via JavaScript
                                self.driver.execute_script("arguments[0].click();", element)

                                # Aguarda 1 segundo para o anúncio fechar
                                time.sleep(1)

                                # Retorna True indicando que conseguiu fechar
                                return True

                            # Caso o clique via JavaScript também falhe
                            except Exception:

                                # Ignora o erro e continua tentando outros elementos
                                pass

            # Caso dê erro ao procurar elementos
            except Exception:

                # Ignora o erro e continua tentando outros seletores
                pass

        # Retorna False se não conseguiu clicar em nenhum botão de fechar
        return False

    # Método para tentar fechar popups de anúncio
    def close_ad_popup(self):

        # Garante que o Selenium está no conteúdo principal da página
        self.driver.switch_to.default_content()

        # Tenta fechar o anúncio no contexto principal
        if self.try_click_close_in_current_context():

            # Volta para o conteúdo principal
            self.driver.switch_to.default_content()

            # Retorna True indicando que conseguiu fechar
            return True

        # Busca todos os iframes da página
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        # Percorre os iframes encontrados
        for index in range(len(iframes)):

            # Tenta entrar no iframe e fechar anúncio dentro dele
            try:

                # Volta para o conteúdo principal
                self.driver.switch_to.default_content()

                # Atualiza a lista de iframes
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

                # Verifica se o índice ainda existe
                if index >= len(iframes):

                    # Pula para o próximo loop
                    continue

                # Entra no iframe atual
                self.driver.switch_to.frame(iframes[index])

                # Tenta clicar no botão de fechar dentro do iframe
                if self.try_click_close_in_current_context():

                    # Volta para o conteúdo principal
                    self.driver.switch_to.default_content()

                    # Retorna True indicando que conseguiu fechar
                    return True

            # Caso ocorra erro ao acessar o iframe
            except Exception:

                # Ignora o erro
                pass

            # Executa sempre, com erro ou sem erro
            finally:

                # Garante que voltou para o conteúdo principal
                self.driver.switch_to.default_content()

        # Se não conseguiu fechar clicando, tenta esconder elementos de anúncio com JavaScript
        self.driver.execute_script("""
            const ids = [
                'dismiss-button-element',
                'dismiss-button',
                'card',
                'ad',
                'ads',
                'creative',
                'feedback',
                'google_ads_iframe'
            ];

            ids.forEach(id => {
                const element = document.getElementById(id);

                if (element) {
                    element.style.display = 'none';
                }
            });

            document.querySelectorAll('iframe').forEach(element => {
                const rect = element.getBoundingClientRect();

                if (rect.width > 200 && rect.height > 100) {
                    element.style.display = 'none';
                }
            });
        """)

        # Aguarda 1 segundo após esconder os elementos
        time.sleep(1)

        # Retorna False porque não conseguiu fechar clicando, apenas escondeu
        return False

    # Método que prepara a página antes de interagir com elementos
    def prepare_page(self):

        # Esconde banners inferiores
        self.hide_bottom_banner()

        # Tenta fechar popups de anúncio
        self.close_ad_popup()

    # Método para centralizar um elemento na tela
    def scroll_center(self, element):

        # Executa JavaScript para rolar a tela até o elemento
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    # Método para clicar em um elemento com mais segurança
    def safe_click(self, by, value):

        # Prepara a página antes do clique
        self.prepare_page()

        # Espera o elemento existir no HTML da página
        element = self.wait.until(
            EC.presence_of_element_located((by, value))
        )

        # Centraliza o elemento na tela
        self.scroll_center(element)

        # Prepara a página novamente antes de clicar
        self.prepare_page()

        # Tenta fazer o clique normal
        try:

            # Espera o elemento ficar clicável
            self.wait.until(
                EC.element_to_be_clickable((by, value))
            )

            # Clica no elemento
            element.click()

        # Caso algum anúncio ou elemento bloqueie o clique
        except ElementClickInterceptedException:

            # Prepara a página novamente
            self.prepare_page()

            # Faz o clique usando JavaScript
            self.driver.execute_script("arguments[0].click();", element)

    # Método para digitar texto em um campo com segurança
    def safe_send_keys(self, by, value, text):

        # Prepara a página antes de digitar
        self.prepare_page()

        # Espera o campo existir no HTML da página
        element = self.wait.until(
            EC.presence_of_element_located((by, value))
        )

        # Centraliza o campo na tela
        self.scroll_center(element)

        # Prepara a página novamente
        self.prepare_page()

        # Limpa o campo antes de digitar
        element.clear()

        # Digita o texto no campo
        element.send_keys(text)

    # Método para selecionar uma opção em um campo select pelo texto visível
    def safe_select_by_text(self, by, value, text):

        # Prepara a página antes da seleção
        self.prepare_page()

        # Espera o campo select existir
        element = self.wait.until(
            EC.presence_of_element_located((by, value))
        )

        # Centraliza o select na tela
        self.scroll_center(element)

        # Prepara a página novamente
        self.prepare_page()

        # Seleciona a opção pelo texto visível
        Select(element).select_by_visible_text(text)

    # Método para esperar aparecer o texto de usuário logado
    def wait_for_logged_in(self):

        # Tenta encontrar o texto de usuário logado
        try:

            # Prepara a página
            self.prepare_page()

            # Espera o link contendo "Logged in as" ficar visível
            return self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//a[contains(., 'Logged in as')]")
                )
            )

        # Caso não encontre dentro do tempo limite
        except TimeoutException:

            # Tenta fechar popup novamente
            self.close_ad_popup()

            # Esconde banners inferiores novamente
            self.hide_bottom_banner()

            # Aguarda 2 segundos
            time.sleep(2)

            # Tenta encontrar novamente o texto de usuário logado
            return self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//a[contains(., 'Logged in as')]")
                )
            )

    # Método para esperar aparecer o texto de conta criada
    def wait_for_account_created(self):

        # Espera o texto Account Created ficar visível
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//b[text()='Account Created!']")
            )
        )

    # Método para esperar aparecer o texto de conta deletada
    def wait_for_account_deleted(self):

        # Tenta encontrar o texto Account Deleted
        try:

            # Prepara a página
            self.prepare_page()

            # Espera o texto Account Deleted ficar visível
            return self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//b[text()='Account Deleted!']")
                )
            )

        # Caso não encontre dentro do tempo limite
        except TimeoutException:

            # Tenta fechar popup novamente
            self.close_ad_popup()

            # Esconde banners novamente
            self.hide_bottom_banner()

            # Aguarda 2 segundos
            time.sleep(2)

            # Tenta encontrar novamente o texto Account Deleted
            return self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//b[text()='Account Deleted!']")
                )
            )

    # Método para ir até a página de cadastro/login
    def go_to_signup_login_page(self):

        # Clica no link Signup / Login
        self.safe_click(By.LINK_TEXT, "Signup / Login")

    # Método para cadastrar um usuário
    def register_user(self, user):

        # Vai para a página de cadastro/login
        self.go_to_signup_login_page()

        # Espera o texto New User Signup aparecer
        signup_text = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[text()='New User Signup!']")
            )
        )

        # Garante que o texto está visível
        assert signup_text.is_displayed()

        # Preenche o nome do usuário
        self.safe_send_keys(By.NAME, "name", user["name"])

        # Preenche o email de cadastro
        self.safe_send_keys(By.XPATH, "//input[@data-qa='signup-email']", user["email"])

        # Clica no botão Signup
        self.safe_click(By.XPATH, "//button[@data-qa='signup-button']")

        # Espera o texto Enter Account Information aparecer
        account_info_text = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//b[text()='Enter Account Information']")
            )
        )

        # Garante que o texto está visível
        assert account_info_text.is_displayed()

        # Seleciona o gênero Mrs
        self.safe_click(By.ID, "id_gender2")

        # Preenche a senha
        self.safe_send_keys(By.ID, "password", user["password"])

        # Seleciona o dia de nascimento
        self.safe_select_by_text(By.ID, "days", "22")

        # Seleciona o mês de nascimento
        self.safe_select_by_text(By.ID, "months", "December")

        # Seleciona o ano de nascimento
        self.safe_select_by_text(By.ID, "years", "2001")

        # Marca a opção newsletter
        self.safe_click(By.ID, "newsletter")

        # Marca a opção de receber ofertas
        self.safe_click(By.ID, "optin")

        # Preenche o primeiro nome
        self.safe_send_keys(By.ID, "first_name", user["first_name"])

        # Preenche o sobrenome
        self.safe_send_keys(By.ID, "last_name", user["last_name"])

        # Preenche a empresa
        self.safe_send_keys(By.ID, "company", user["company"])

        # Preenche o endereço principal
        self.safe_send_keys(By.ID, "address1", user["address1"])

        # Preenche o endereço secundário
        self.safe_send_keys(By.ID, "address2", user["address2"])

        # Seleciona o país
        self.safe_select_by_text(By.ID, "country", user["country"])

        # Preenche o estado
        self.safe_send_keys(By.ID, "state", user["state"])

        # Preenche a cidade
        self.safe_send_keys(By.ID, "city", user["city"])

        # Preenche o CEP
        self.safe_send_keys(By.ID, "zipcode", user["zipcode"])

        # Preenche o número de celular
        self.safe_send_keys(By.ID, "mobile_number", user["mobile_number"])

        # Clica no botão Create Account
        self.safe_click(By.XPATH, "//button[@data-qa='create-account']")

        # Espera aparecer o texto Account Created
        created_text = self.wait_for_account_created()

        # Garante que o texto está visível
        assert created_text.is_displayed()

        # Clica no botão Continue após criar a conta
        self.safe_click(By.XPATH, "//a[@data-qa='continue-button']")

    # Método para fazer login
    def login_user(self, email, password):

        # Vai para a página de cadastro/login
        self.go_to_signup_login_page()

        # Espera o texto Login to your account aparecer
        login_text = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[text()='Login to your account']")
            )
        )

        # Garante que o texto está visível
        assert login_text.is_displayed()

        # Preenche o email de login
        self.safe_send_keys(By.XPATH, "//input[@data-qa='login-email']", email)

        # Preenche a senha de login
        self.safe_send_keys(By.XPATH, "//input[@data-qa='login-password']", password)

        # Clica no botão Login
        self.safe_click(By.XPATH, "//button[@data-qa='login-button']")

        # Espera aparecer o texto Logged in as
        logged_in_text = self.wait_for_logged_in()

        # Garante que o texto está visível
        assert logged_in_text.is_displayed()

    # Método para sair da conta
    def logout_user(self):

        # Clica no link Logout
        self.safe_click(By.LINK_TEXT, "Logout")

    # Método para deletar a conta
    def delete_account(self):

        # Clica no link Delete Account
        self.safe_click(By.LINK_TEXT, "Delete Account")

        # Espera aparecer o texto Account Deleted
        deleted_text = self.wait_for_account_deleted()

        # Garante que o texto está visível
        assert deleted_text.is_displayed()

        # Clica no botão Continue final
        self.safe_click(By.XPATH, "//a[@data-qa='continue-button']")