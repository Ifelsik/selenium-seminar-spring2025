from selenium.webdriver.common.by import By

class LoginPageLocators:
    BUTTON_LOGIN_MODAL = (By.XPATH, "//a[starts-with(@class, 'AuthButton__SAuthLink')]") 
    BUTTON_CONTINUE_WITH_EMAIL_PASSWORD = (By.XPATH, "//button[normalize-space(text())='Продолжить с помощью почты и пароля']")
    INPUT_EMAIL = (By.ID, 'email')
    INPUT_PASSWORD = (By.ID, 'password')
    SUBMIT_BUTTON = (By.XPATH, '//button[@type="submit"]')

class PortalPersonalPageLocators:
    BUTTON_SEARCH = (By.XPATH, "//div[starts-with(@class, 'styles__SIconFocusableButton')]")
    INPUT_SEARCH = (By.XPATH, '//div[starts-with(@class, "global-search__SSearchContainer")]//input')
    CARD_PROFILE = (By.XPATH, "//table[contains(@class, 'table-users')]//div[contains(@class, 'name')]//a")
    SHOW_CARDS_DISCIPLINES = (By.XPATH, "//div[starts-with(@class, 'styles__SDisciplinesHeader')]")
    CARD_DISCIPLINE = (By.XPATH, "//div[starts-with(@class, 'styles__SDisciplineContainer')]")
    CARD_DISCIPLINE_TEXT = (By.XPATH, ".//div[starts-with(@class, 'styles__SDisciplineTitleLayout')]//a")
    CARD_LESSON = (By.XPATH, "//div[@data-lesson_id and contains(@class, 'LessonCard__SLessonCard')]")
    CARD_LESSON_TEXT = (By.XPATH, ".//a")
    
