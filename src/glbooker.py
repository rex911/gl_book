import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class GLBooker(object):
    PAGE_DELAY_SECONDS = 5

    def __init__(self,
                 username,
                 password,
                 url='https://www.goodlifefitness.com/members/bookings/workout',
                 days_later=7,
                 workout_start='6:15PM',
                 workout_end='7:15PM',
                 driver='Safari'):
        """Main class for the booker

        Args:
            username (str): Your Goodlife account username
            password (str): Your Goodlife account password
            url (str, optional): The booking URL.
                Defaults to 'https://www.goodlifefitness.com/members/bookings/workout'.
            days_later (int, optional): How many days later to book. Between 0 and 7.
                Goodlife allows booking 7 days in advance as of Sep 2020.
                Defaults to 7.
            workout_start (str, optional): Must be in the format of 'H:MM[AM/PM]'.
                Defaults to '6:00PM'.
            workout_end (str, optional): Must be in the format of 'H:MM[AM/PM]'.
                Defaults to '7:00PM'.
        """
        self.username = username
        self.password = password
        self.url = url
        self.days_later = days_later
        self.workout_start = workout_start
        self.workout_end = workout_end
        if driver == 'Safari':
            self.driver = webdriver.Safari()
        elif driver == 'Firefox':
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
        else:
            raise ValueError('Unsupported webdriver: {}'.format(driver))

    def login(self):
        self.driver.get(self.url)
        username_element = self.driver.find_element_by_name("Email/Member #")
        username_element.send_keys(self.username)
        password_element = self.driver.find_element_by_name("Password")
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)
        time.sleep(self.PAGE_DELAY_SECONDS)

    def find_book_slot(self):
        # select day
        self.driver.execute_script(
            'document.getElementsByClassName("tile-day")[{}].click()'.format(self.days_later))
        time.sleep(self.PAGE_DELAY_SECONDS)
        # select time slot
        book_slots = self.driver.find_elements_by_class_name('book-slot')
        b = [
            i for i in book_slots
            if '{} - {}'.format(self.workout_start, self.workout_end) in i.text][0]
        click_button = b.find_element_by_class_name('cmp-button__text')
        self.driver.execute_script("arguments[0].click();", click_button)
        time.sleep(self.PAGE_DELAY_SECONDS)

    def agree_and_confirm(self):
        # click agree
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element_by_xpath(
                '//*[@id="codeOfConductAgree"]'))

        # click confirm
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element_by_xpath(
                '//*[@id="confirmBookingButton"]'))

    def book(self):
        self.login()
        self.find_book_slot()
        self.agree_and_confirm()
        self.driver.close()
