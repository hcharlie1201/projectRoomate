from aloe import before, step, world
from aloe.tools import guess_types
from aloe_django.steps.models import get_model
import aloe_webdriver

@step("I am on the home page")
def _on_hompage(self):
    self.behave_as('I visit ""')
