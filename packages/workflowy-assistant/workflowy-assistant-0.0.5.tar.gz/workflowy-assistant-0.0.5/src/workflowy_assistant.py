import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from webdriver_manager.firefox import GeckoDriverManager


class WorkFlowyAssistant(object):
    def __init__(self, username, password, firefox_location):
        self.workflowy_url = 'https://workflowy.com'

        self.workflowy_username = username
        self.workflowy_password = password

        options = Options()
        # No window
        options.headless = True
        # FireFox binary location
        options.binary_location = firefox_location
        # Silent dilevery / no visible logging
        os.environ['WDM_LOG_LEVEL'] = '0'
        # Get latest FireFox webdriver
        self.browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options, service_log_path=os.devnull)

    def __login(self):
        # Login process

        self.__wait_for_element_to_appear('/html/body/div[1]/div/div[1]/nav/a[4]')
        self.__click_button('/html/body/div[1]/div/div[1]/nav/a[4]')
        self.__wait_for_element_to_appear('//*[@id="page"]/div/div[2]/form/div[1]/input')
        self.__fill_text_box('//*[@id="page"]/div/div[2]/form/div[1]/input', self.workflowy_username)
        self.__click_button('//*[@id="page"]/div/div[2]/form/div[2]/div[3]/button/span')
        self.__wait_for_element_to_appear('//*[@id="page"]/div/div[2]/form/div[2]/div[2]/div/input')
        self.__fill_text_box('//*[@id="page"]/div/div[2]/form/div[2]/div[2]/div/input', self.workflowy_password)
        self.__click_button('//*[@id="page"]/div/div[2]/form/div[2]/div[3]/button/span')
        self.__wait_for_element_to_appear('//*[contains(@class,"addChild")]')
        
        # Save cookies to pickle for future use
        pickle.dump(self.browser.get_cookies(), open('cookies.pkl','wb'))

    def __load_or_login(self):
        # Open WF
        self.browser.get(self.workflowy_url)

        try:
            # Test if pickle file opens or exists
            cookies = pickle.load(open('cookies.pkl', 'rb'))
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            self.browser.get(self.workflowy_url)
        except:
            # Otherwise log in
            self.__login()

        try:
            # Check if logged in
            self.__wait_for_element_to_appear('//*[contains(@class,"addChild")]')
        except:
            # Otherwise log in
            self.__login()

    def add_new_bullet(self, id, text):
        # Check if logged in
        self.__load_or_login()

        # Open node
        self.browser.get(f'{self.workflowy_url}/#/{id}')

        # Add empty child
        self.__wait_for_element_to_appear('//*[contains(@class,"addChild")]')
        self.__click_button('//*[contains(@class,"addChild")]')

        # Start ActionChain based on list
        actions = ActionChains(self.browser)

        for i in range(0, len(text)):
            actions.send_keys(text[i])

            if i != len(text)-1:
                # No return after last list item
                actions.send_keys(Keys.RETURN)
        
        # Execute ActionChain
        actions.perform()

        # Time to save new nodes
        time.sleep(5)

    def __click_button(self, xpath: str):
        self.browser.find_element_by_xpath(xpath).click()

    def __wait_for_element_to_appear(self, xpath):
        try:
            element = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except:
            print('Error: element not found in XPATH.')
            self.browser.quit()

    def __fill_text_box(self, xpath: str, text_to_input: str):
        self.browser.find_element_by_xpath(xpath).send_keys(text_to_input)

    def close_browser(self):
        self.browser.close()


if __name__ == '__main__':
    pass