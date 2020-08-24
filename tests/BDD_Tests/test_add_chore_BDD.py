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

        self.auth_user2 = User.objects.create(username='user2')
        self.auth_user2.set_password('abc1233456789')
        self.auth_user2.save()

        self.auth_user3 = User.objects.create(username='user3')
        self.auth_user3.set_password('abc1233456789')
        self.auth_user3.save()
        # New Apartment
        self.apartment = Apartment.objects.create(
            token='2fsaghsehrtjstuertudtudrht')
        self.apt_token = self.apartment.token
        self.auth_user1.myuser.myApt = self.apartment
        self.auth_user1.save()
        # Apartment with chores
        self.apartment_chore = Apartment.objects.create(
            token='65465sd4gr65s4hs1h65ar')
        self.apt_chore_token = self.apartment_chore.token

        Chore.objects.create(apt_id=self.apartment_chore, name="Clean kitchen",
                             creator=self.auth_user2)
        Chore.objects.create(apt_id=self.apartment_chore, name="Wash dishes",
                             creator=self.auth_user2)
        Chore.objects.create(apt_id=self.apartment_chore, name="Take out trash",
                             creator=self.auth_user2)
        self.auth_user2.myuser.myApt = self.apartment_chore
        self.auth_user2.save()
        self.auth_user3.myuser.myApt = self.apartment_chore
        self.auth_user3.save()
        # Log in and join apt
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user1')
        self.selenium.find_element_by_name(
            "password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath(
            '//*[@id="card"]/div/form/button').click()

    # User can add a chore to a new apartment
    def test_add_chore_clean_apt_BDD(self):
        self.selenium.find_element_by_xpath('/html/body/div/a').click()
        self.selenium.find_element_by_name('name').send_keys('wash dishes')
        self.selenium.find_element_by_name(
            'description').send_keys('wash dishes')
        self.selenium.find_element_by_name('submit').click()
        result = self.selenium.find_element_by_xpath('/html/body')

        self.assertIn("wash dishes", result.text)
        self.assertIn("user1", result.text)
    
    #User should delete a chore
    def test_delete_chore(self):
        self.selenium.find_element_by_xpath('/html/body/div/a').click()
        self.selenium.find_element_by_name('name').send_keys('wash dishes')
        self.selenium.find_element_by_name(
            'description').send_keys('wash dishes')
        self.selenium.find_element_by_name('submit').click()
        self.selenium.find_element_by_link_text('Delete').click()
        result = self.selenium.find_element_by_xpath('/html/body')
        self.assertIn("Successfully delete.", result.text)

    # User can add a chore to an apartment that already has chores and they are also the owner
    def test_add_chore_w_chore_apt_BDD_1(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user2')
        self.selenium.find_element_by_name(
            "password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath(
            '//*[@id="card"]/div/form/button').click()

        self.selenium.find_element_by_name("createchore").click()
        self.selenium.find_element_by_name('name').send_keys('wash dishes')
        self.selenium.find_element_by_name(
            'description').send_keys('wash dishes')
        self.selenium.find_element_by_name('submit').click()
        result = self.selenium.find_element_by_xpath('/html/body')

        self.assertIn("wash dishes", result.text)
        self.assertIn("user2", result.text)

    # User can add a chore to an apartment that already has chores and they are NOT the owner
    def test_add_chore_w_chore_apt_BDD_2(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user3')
        self.selenium.find_element_by_name(
            "password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath(
            '//*[@id="card"]/div/form/button').click()

        self.selenium.find_element_by_name("createchore").click()
        self.selenium.find_element_by_name('name').send_keys('Mop the floor')
        self.selenium.find_element_by_name(
            'description').send_keys('Mop the floor')
        self.selenium.find_element_by_name('submit').click()
        result = self.selenium.find_element_by_xpath('/html/body')

        self.assertIn("Mop the floor", result.text)
        self.assertIn("user3", result.text)
