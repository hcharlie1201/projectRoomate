from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.auth.models import User

#Feature: Registered user can login/logout, and new user and sign up
class HomepageTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        #Remove firefox_options=options to display the browser
        cls.selenium = WebDriver(firefox_options=options)
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        #Before
        auth_user1 = User.objects.create(username='user1')
        auth_user1.set_password('abc1233456789')
        auth_user1.save()
    #A registered user (user1) can login from the home page
    def test_user_login_BDD(self):
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user1')
        self.selenium.find_element_by_name("password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath('//*[@id="card"]/div/form/button').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        result = self.selenium.find_element_by_xpath('/html/body/div')
        self.assertIn("Create a new Apartment", result.text)


    #A new user can register from the home page
    def test_user_register_BDD(self):
        timeout = 5
        self.selenium.get('%s%s' % (self.live_server_url, '/users/register/'))
        self.selenium.find_element_by_name("username").send_keys('user222')
        self.selenium.find_element_by_name("email").send_keys('aaa@example.com')
        self.selenium.find_element_by_xpath('//*[@id="id_password1"]').send_keys('abc@@123456789')
        self.selenium.find_element_by_xpath('//*[@id="id_password2"]').send_keys('abc@@123456789')
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.selenium.find_element_by_xpath('//*[@id="card"]/div[2]/form/button').click()
        registered_user = User.objects.get(username='user222')
        self.assertEqual(registered_user.username, 'user222')
        self.assertEqual(registered_user.email, 'aaa@example.com')
    
    #The user is able to access the login page
    def test_access_login_BDD(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath('/html/body/div/div/div/div/div[1]/a').click()
        self.assertTemplateUsed('registration/login.html')
        self.assertEqual(self.selenium.current_url, '%s%s' % (self.live_server_url, '/users/login/'))

    #The user is able to access the registration page
    def test_access_registration_BDD(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath('/html/body/div/div/div/div/div[2]/a').click()
        self.assertTemplateUsed('registration/register.html')
        self.assertEqual(self.selenium.current_url, '%s%s' % (self.live_server_url, '/users/register/'))

    #The logged in user can logout
    def test_user_logout_BDD(self):
        timeout = 5
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user1')
        self.selenium.find_element_by_name("password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath('//*[@id="card"]/div/form/button').click()
        self.selenium.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[2]/a').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        
        result = self.selenium.find_element_by_xpath('/html/body/div')
        self.assertIn("You have been logged out.", result.text)
        self.assertTemplateUsed('registration/logged_out.html')






