from contextlib import contextmanager
import pytest
from _pytest.fixtures import FixtureRequest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.base_page import BasePage
from ui.locators.vk_locators import LoginPageLocators, PortalPersonalPageLocators


class BaseCase:
    authorize = True

    @contextmanager
    def switch_to_window(self, current, close=False):
        for w in self.driver.window_handles:
            if w != current:
                self.driver.switch_to.window(w)
                break
        yield
        if close:
            self.driver.close()
        self.driver.switch_to.window(current)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.login_page = LoginPage(driver)
        self.portal_page = None
        if self.authorize:
            cookies = request.getfixturevalue('cookies')

            self.driver.get(self.config['url'])

            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            self.driver.refresh()

            self.portal_page = MainPage(driver)


@pytest.fixture(scope='session')
def credentials():
    login = "example@mail.com" 
    password = "password"
    return login, password

@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    login, password = credentials
    login_page = LoginPage(driver)
    main_page = login_page.login(login, password)

    # checks if page loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(main_page.locators.BUTTON_SEARCH)
    )

    cookies = driver.get_cookies()
    driver.quit()

    return cookies


class LoginPage(BasePage):
    url = 'https://education.vk.company/'
    locators = LoginPageLocators()

    def __init__(self, driver):
         driver.get(self.url)
         super().__init__(driver)
    
    def login(self, user, password):
        self.click(self.locators.BUTTON_LOGIN_MODAL)
        self.click(self.locators.BUTTON_CONTINUE_WITH_EMAIL_PASSWORD)
        email_input = self.click(self.locators.INPUT_EMAIL)
        email_input.send_keys(user)
        password_input = self.click(self.locators.INPUT_PASSWORD)
        password_input.send_keys(password)
        self.click(self.locators.SUBMIT_BUTTON)

        return MainPage(self.driver)


class MainPage(BasePage):
    url = 'https://education.vk.company/feed/'
    locators = PortalPersonalPageLocators()

    def __init__(self, driver):
        driver.get(self.url)
        super().__init__(driver)

    def search(self, query):
        search_btn = self.find(self.locators.BUTTON_SEARCH)
        search_btn.click()
        search_input = self.find(self.locators.INPUT_SEARCH)
        search_input.send_keys(query)
        search_input.send_keys(Keys.ENTER)

    def show_disciplines_list(self):
        self.find(self.locators.SHOW_CARDS_DISCIPLINES).click()

    def find_card(self, card_locator, card_text_link_locator, name):
        cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(card_locator)
        )
        for card in cards:
            element = card.find_element(*card_text_link_locator)
            text = element.get_attribute("textContent")

            if text.strip() == name:
                print("True", text)
                ActionChains(self.driver).move_to_element(element).perform()
                return element

        return None


class TestLogin(BaseCase):
    authorize = False

    def test_login(self, credentials):
        ME = 'Черепнин Михаил'
        login, password = credentials
        self.login_page.login(login, password)

        assert ME in self.driver.page_source


class TestLK(BaseCase):

    def test_lk1(self):
        USER = 'Сергей Дранцев'

        self.portal_page.search(USER)
        assert USER in self.driver.page_source

        card = self.portal_page.find(self.portal_page.locators.CARD_PROFILE)
        card.click()
        assert USER in self.driver.page_source

    def test_lk2(self):
        DISCIPLINE = 'Обеспечение качества в разработке ПО'
        SEMINAR_TOPIC = 'End-to-End тесты на Python'

        self.portal_page.show_disciplines_list()
        assert DISCIPLINE in self.driver.page_source

        discipline = self.portal_page.find_card(
            self.portal_page.locators.CARD_DISCIPLINE,
            self.portal_page.locators.CARD_DISCIPLINE_TEXT,
            DISCIPLINE
        )
        current_window = self.driver.current_window_handle
        discipline.click()

        with self.switch_to_window(current_window, close=False):
            seminar = self.portal_page.find_card(
                self.portal_page.locators.CARD_LESSON,
                self.portal_page.locators.CARD_LESSON_TEXT,
                SEMINAR_TOPIC
            )
            seminar.click()

            assert SEMINAR_TOPIC in self.driver.page_source
        

    def test_lk3(self):
        pass
