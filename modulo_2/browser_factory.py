# Importa o webdriver do Selenium, usado para controlar o navegador
from selenium import webdriver

# Importa o WebDriverWait, usado para criar esperas explícitas
from selenium.webdriver.support.ui import WebDriverWait


# Define uma classe responsável por criar o navegador e a espera
class BrowserFactory:

    # Define um método estático, ou seja, pode ser chamado sem criar objeto da classe
    @staticmethod
    def create_chrome_driver():

        # Cria um objeto de opções para configurar o navegador Chrome
        options = webdriver.ChromeOptions()

        # Configura o Chrome para abrir maximizado
        options.add_argument("--start-maximized")

        # Desabilita notificações do navegador
        options.add_argument("--disable-notifications")

        # Desabilita o bloqueio de popups do navegador
        options.add_argument("--disable-popup-blocking")

        # Cria e retorna uma instância do Chrome com as opções configuradas
        return webdriver.Chrome(options=options)

    # Define um método estático para criar o objeto de espera explícita
    @staticmethod
    def create_wait(driver, timeout=20):

        # Cria e retorna uma espera explícita usando o driver e o tempo limite informado
        return WebDriverWait(driver, timeout)