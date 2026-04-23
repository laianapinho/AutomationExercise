import time
from selenium.webdriver.common.by import By


class PopupHandler:
    """Responsável por tratar banners, popups e iframes de anúncios."""

    def __init__(self, driver):
        # Recebe a instância do navegador
        self.driver = driver

    def hide_bottom_banner(self):
        """Esconde banners fixos na parte inferior da tela."""
        self.driver.execute_script("""
            const elements = document.querySelectorAll('body *');

            elements.forEach(element => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();

                const is_fixed_like =
                    style.position === 'fixed' || style.position === 'sticky';

                const is_near_bottom =
                    rect.bottom >= window.innerHeight - 5;

                const is_big_enough =
                    rect.width > 400 && rect.height > 80;

                if (is_fixed_like && is_near_bottom && is_big_enough) {
                    element.style.display = 'none';
                }
            });
        """)

    def _try_close_in_current_context(self):
        """
        Tenta fechar o popup no contexto atual:
        página principal ou iframe atual.
        """
        selectors = [
            (By.ID, "dismiss-button-element"),
            (By.ID, "dismiss-button"),
            (By.XPATH, "//*[@id='dismiss-button-element']"),
            (By.XPATH, "//*[@id='dismiss-button']"),
            (By.XPATH, "//*[normalize-space(text())='Close']"),
            (By.XPATH, "//div[normalize-space()='Close']"),
            (By.XPATH, "//span[normalize-space()='Close']"),
            (By.XPATH, "//button[normalize-space()='Close']"),
            (By.XPATH, "//a[normalize-space()='Close']"),
        ]

        # Percorre os seletores possíveis do botão de fechar
        for by, value in selectors:
            elements = self.driver.find_elements(by, value)

            for element in elements:
                if not element.is_displayed():
                    continue

                try:
                    # Rola até o elemento antes de clicar
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});",
                        element
                    )
                    element.click()
                    time.sleep(1)
                    return True
                except Exception:
                    try:
                        # Se o clique normal falhar, tenta via JavaScript
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)
                        return True
                    except Exception:
                        continue

        return False

    def close_ad_popup(self):
        """
        Tenta fechar o popup no conteúdo principal.
        Se não conseguir, tenta dentro de todos os iframes.
        Se ainda falhar, remove os elementos por JavaScript.
        """
        self.driver.switch_to.default_content()

        # Tenta fechar no conteúdo principal
        if self._try_close_in_current_context():
            self.driver.switch_to.default_content()
            return True

        # Procura iframes, porque o anúncio pode estar dentro deles
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        for index in range(len(iframes)):
            try:
                self.driver.switch_to.default_content()
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

                if index >= len(iframes):
                    continue

                # Entra no iframe atual
                self.driver.switch_to.frame(iframes[index])

                # Tenta fechar o popup dentro do iframe
                if self._try_close_in_current_context():
                    self.driver.switch_to.default_content()
                    return True

            except Exception:
                continue
            finally:
                try:
                    self.driver.switch_to.default_content()
                except Exception:
                    pass

        # Fallback: remove popup, overlay e iframes grandes via JavaScript
        self.driver.switch_to.default_content()
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

            document.querySelectorAll('body *').forEach(element => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();

                const is_visible =
                    style.display !== 'none' &&
                    style.visibility !== 'hidden' &&
                    rect.width > 150 &&
                    rect.height > 80;

                const is_centered =
                    rect.left > window.innerWidth * 0.10 &&
                    rect.right < window.innerWidth * 0.90 &&
                    rect.top > window.innerHeight * 0.05 &&
                    rect.bottom < window.innerHeight * 0.95;

                const is_overlay_like =
                    style.position === 'fixed' ||
                    style.position === 'absolute' ||
                    parseInt(style.zIndex || '0') >= 999;

                const is_backdrop =
                    style.position === 'fixed' &&
                    rect.width >= window.innerWidth * 0.8 &&
                    rect.height >= window.innerHeight * 0.8;

                if ((is_visible && is_centered && is_overlay_like) || is_backdrop) {
                    element.style.display = 'none';
                }
            });
        """)
        time.sleep(1)
        return False

    def prepare_page(self):
        """Aplica todos os tratamentos necessários antes da interação."""
        self.hide_bottom_banner()
        self.close_ad_popup()