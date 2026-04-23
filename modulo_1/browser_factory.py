from selenium import webdriver


class BrowserFactory:
    """Responsável por criar e configurar o navegador."""

    @staticmethod
    def create_chrome_driver():
        # Configura as opções do navegador Chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

        # Cria e retorna o driver do Chrome
        return webdriver.Chrome(options=chrome_options)