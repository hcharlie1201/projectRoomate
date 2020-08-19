from aloe import before, step, world
from aloe.tools import guess_types, hook_not_reentrant
from aloe_django.steps.models import get_model
import aloe_webdriver.django
import aloe_webdriver

BASE_URL = "http://127.0.0.1:8000/"
@step(r'I am on the home page')
def _on_hompage_step(self):
    self.behave_as('When I visit "{}"'.format(BASE_URL))

