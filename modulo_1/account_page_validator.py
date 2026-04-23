import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


class AccountPageValidator:
    """Responsável por validar estados importantes do fluxo."""

    def __init__(self, driver, wait, popup_handler):
        self.driver = driver
        self.wait = wait
        self.popup_handler = popup_handler

    def wait_for_logged_in(self):
        """
        Espera aparecer o texto 'Logged in as'.
        Se falhar, trata popup novamente e tenta outra vez.
        """
        try:
            self.popup_handler.prepare_page()
            return self.wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, "//a[contains(., 'Logged in as')]")
                )
            )
        except TimeoutException:
            self.popup_handler.close_ad_popup()
            self.popup_handler.hide_bottom_banner()
            time.sleep(2)

            return self.wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, "//a[contains(., 'Logged in as')]")
                )
            )

    def wait_for_account_deleted(self):
        """
        Espera aparecer o texto 'Account Deleted!'.
        Se falhar, trata popup novamente e tenta outra vez.
        """
        try:
            self.popup_handler.prepare_page()
            return self.wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, "//b[text()='Account Deleted!']")
                )
            )
        except TimeoutException:
            self.popup_handler.close_ad_popup()
            self.popup_handler.hide_bottom_banner()
            time.sleep(2)

            return self.wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, "//b[text()='Account Deleted!']")
                )
            )