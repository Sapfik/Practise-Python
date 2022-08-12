from pprint import pprint
import os
import signal
import sys
import logging
import traceback
from selenium.common.exceptions import TimeoutException, InvalidCookieDomainException
from seleniumwire import webdriver
from seleniumwire.thirdparty.mitmproxy.exceptions import HttpReadDisconnect, TcpDisconnect, TlsException
import logger
from send_email import send_email

from common_config import DRIVER_PATH, LOGFILE_PATH, EMAIL_ADDR_FROM, EMAIL_ADDR_TO, PLATFORM


class SeleniumDriver():
    """The Selenium Chrome Driver class.
    """

    def __init__(self, cookie_page_url=None):
        """Initizling the class.

        Args:
            cookie_page_url (string, optional): The URL of the page for setting cookies. Defaults to None.
        """
        self.driver = None
        self.logger = logger.get_logger(__name__, LOGFILE_PATH)
        self.cookie_page_url = cookie_page_url
        self.timeout_time = 10
        self.proxy = None

    def quit(self):
        """Quiting the driver
        """
        pid = int(self.driver.service.process.pid)

        try:
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            self.logger.warning(
                f'The error during the driver closing has been occured: {e}')

        try:
            os.kill(pid, signal.SIGTERM)
            return True
        except:
            return False

    def init_driver(self, wire_options):
        """Initializing the driver.

        Args:
            wire_options (dict): The dictionary of driver's options.
        """

        if 'proxy' in wire_options:
            self.proxy = wire_options['proxy']

        chrome_options = webdriver.ChromeOptions()
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.default_content_settings.images': 2,
            'profile.managed_default_content_settings.javascript': 2,
            'profile.managed_default_content_settings.mixed_script': 2,
            'profile.managed_default_content_settings.media_stream': 2,
            'profile.managed_default_content_settings.stylesheets': 2
        }

        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(
            executable_path=DRIVER_PATH,
            seleniumwire_options=wire_options,
            options=chrome_options)

        driver.set_page_load_timeout(self.timeout_time)

        self.driver = driver

    def get_page_source(self, url):
        """Getting the page's URL source code.

        Args:
            url (string): The page's URL.

        Returns:
            string: The page's URL source code.
        """

        page_source = None

        try:
            self.driver.get(url)
            page_source = self.driver.page_source
            return page_source

        except Exception as error:
            self.logger.warning(
                f'Во время получения кода страницы {url} встретилась ошибка: {error}.')
            self.logger.warning(
                ''.join(traceback.format_tb(error.__traceback__)))

            email_subject = '«Автостатистик». Ошибка при получении кода страницы'

            if self.proxy is not None:
                email_message = f'Возможно проблема с прокси. Необходимо проверить прокси: {self.proxy}. Текст ошибки: {error}'
            else:
                email_message = f'Текст ошибки: {error}'

            send_notification(email_subject, email_message)
            return False

    def set_cookies(self, cookies):
        """Setting the driver cookies

        Args:
            cookies (dict): The dictionary of cookies to set.
        """

        if self.cookie_page_url is None:
            self.logger(
                'URL для простановки cookies не указан при инициализации класса.')
            return False

        try:
            self.driver.get(self.cookie_page_url)
            self.driver.add_cookie(cookies)
        except Exception as error:
            self.logger.warning(
                ''.join(traceback.format_tb(error.__traceback__)))

            email_subject = '«Автостатистик». Ошибка при установке cookie'

            if self.proxy is not None:
                self.logger.warning(
                    f'Во время установки cookie для прокси {self.proxy} встретилась ошибка: {error}.')
                email_message = f'Возможно проблема с прокси. Необходимо проверить прокси: {self.proxy}. Текст ошибки: {error}'
            else:
                self.logger.warning(
                    f'Ошибка установки cookie: {error}.')
                email_message = f'Текст ошибки: {error}'

            send_notification(email_subject, email_message)
            return False

        return True


def send_notification(email_subject, email_message):
    """Sending the notification

    Args:
        email_subject (str): The email subject.
        email_message (str): The email message.
    """

    if PLATFORM == 'linux64':
        send_email(email_subject, EMAIL_ADDR_FROM,
                   EMAIL_ADDR_TO, email_message)
