from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementClickInterceptedException


class ElementActions:
    """Responsável por interações seguras com os elementos da página."""

    def __init__(self, driver, wait, popup_handler):
        self.driver = driver
        self.wait = wait
        self.popup_handler = popup_handler

    def scroll_to_center(self, element):
        """Rola a página até centralizar o elemento na tela."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    def safe_click(self, by, value):
        """Clica em um elemento tratando popups e overlays."""
        self.popup_handler.prepare_page()

        element = self.wait.until(ec.presence_of_element_located((by, value)))
        self.scroll_to_center(element)
        self.popup_handler.prepare_page()

        try:
            self.wait.until(ec.element_to_be_clickable((by, value)))
            element.click()
        except ElementClickInterceptedException:
            self.popup_handler.prepare_page()
            self.driver.execute_script("arguments[0].click();", element)

    def safe_send_keys(self, by, value, text):
        """Digita com segurança em um campo."""
        self.popup_handler.prepare_page()

        element = self.wait.until(ec.presence_of_element_located((by, value)))
        self.scroll_to_center(element)
        self.popup_handler.prepare_page()

        element.clear()
        element.send_keys(text)

    def safe_select_by_visible_text(self, by, value, text):
        """Seleciona uma opção em um select pelo texto visível."""
        self.popup_handler.prepare_page()

        element = self.wait.until(ec.presence_of_element_located((by, value)))
        self.scroll_to_center(element)
        self.popup_handler.prepare_page()

        Select(element).select_by_visible_text(text)