from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.auth.models import User
from roomate_app.models import Apartment, MyUser, Chore

#Feature: A logged in user can create a new apartment or join an existing apartment
#NOTE: the token of Apartment objects are not randomly generated for some reason. 
# So they are seeded in this test
class ApartmentTests(StaticLiveServerTestCase):
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
        #Before data
        self.auth_user1 = User.objects.create(username='user1')
        self.auth_user1.set_password('abc1233456789')
        self.auth_user1.save()

        #Dummy user
        self.dummy = User.objects.create(username='user2')
        self.dummy.set_password('abc1233456789')
        self.dummy.save()
        #New Apartment
        self.apartment = Apartment.objects.create(token='2fsaghsehrtjstuertudtudrht')
        self.apt_token = self.apartment.token
        #Apartment with chores
        self.apartment_chore = Apartment.objects.create(token='65465sd4gr65s4hs1h65ar')
        self.apt_chore_token = self.apartment_chore.token
        
        Chore.objects.create(apt_id=self.apartment_chore, name="Clean kitchen",
                                creator=self.dummy)
        Chore.objects.create(apt_id=self.apartment_chore, name="Wash dishes",
                                creator=self.dummy)
        Chore.objects.create(apt_id=self.apartment_chore, name="Take out trash",
                                creator=self.dummy)
        #Log in
        self.selenium.get('%s%s' % (self.live_server_url, '/users/login/'))
        self.selenium.find_element_by_name("username").send_keys('user1')
        self.selenium.find_element_by_name("password").send_keys('abc1233456789')
        self.selenium.find_element_by_xpath('//*[@id="card"]/div/form/button').click()
    
    #From dashboard, the user can create a new apartment.
    def test_user_create_apt_BDD(self):
        self.selenium.find_element_by_id('create-apt').click()
        result = self.selenium.find_element_by_xpath('/html/body/div')

        self.assertIn("Create a new Chore", result.text)

        self.auth_user1 = User.objects.get(pk=self.auth_user1.id)
        self.assertIsNotNone(self.auth_user1.myuser.myApt)

    #From dashboard, the user can join an existing apartment
    def test_user_join_apt_BDD(self):
        self.selenium.find_element_by_id('join-apt').click()
        self.selenium.find_element_by_xpath('//*[@id="id_apt_token"]').send_keys(self.apt_token)
        self.selenium.find_element_by_name('submit').click()
        result = self.selenium.find_element_by_xpath('/html/body/div')
        
        self.assertIn("Create a new Chore", result.text)

        self.auth_user1 = User.objects.get(pk=self.auth_user1.id)
        self.assertEqual(self.auth_user1.myuser.myApt, Apartment.objects.get(token=self.apt_token))

    #From dashboard, the user provides incorrect token.
    def test_user_join_apt_sad_BDD(self):
        self.selenium.find_element_by_id('join-apt').click()
        self.selenium.find_element_by_xpath('//*[@id="id_apt_token"]').send_keys('a')
        self.selenium.find_element_by_name('submit').click()
        result = self.selenium.find_element_by_xpath('/html/body/div')
        self.assertIn("Failed To Join An Apartment", result.text)

    #The user should see chores associted to an apartment after joining
    def test_user_join_apt_chore(self):
        self.selenium.find_element_by_id('join-apt').click()
        self.selenium.find_element_by_xpath('//*[@id="id_apt_token"]').send_keys(self.apt_chore_token)
        self.selenium.find_element_by_name('submit').click()
        result = self.selenium.find_element_by_xpath('/html/body')
        
        self.auth_user1 = User.objects.get(pk=self.auth_user1.id)
        self.assertEqual(self.auth_user1.myuser.myApt, Apartment.objects.get(token=self.apt_chore_token))

        self.assertIn("Clean kitchen", result.text)
        self.assertIn("Wash dishes", result.text)
        self.assertIn("Take out trash", result.text)