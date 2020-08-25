from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.auth.models import User
from roomate_app.models import Apartment, MyUser, Chore

# Feature: A logged in user can create a new chore so that everybody can see it


class ChoreAddTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        # Remove firefox_options=options to display the browser
        cls.selenium = WebDriver(firefox_options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Before data
        self.auth_user1 = User.objects.create(username='user1')
        self.auth_user1.set_password('abc1233456789')
        self.auth_user1.save()

        # New Apartment
        self.apartment = Apartment.objects.create(
            token='2fsaghsehrtjstuertudtudrht')
        self.apt_token = self.apartment.token
        self.auth_user1.myuser.myApt = self.apartment
        self.auth_user1.save()

        # Log in
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user1')
        self.selenium.find_element_by_name(
            "password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath(
            '//*[@id="card"]/div/form/button').click()

    def test_user_leaves_apartment_BDD(self):
        timeout = 5
        self.selenium.get('%s%s' % (self.live_server_url, '/profile/'))
        self.selenium.find_element_by_name("submit").click()
        result = self.selenium.find_element_by_xpath('/html/body')

        self.assertIn("Create a new Apartment", result.text)
        self.assertIn("Join an existing Apartment", result.text)
