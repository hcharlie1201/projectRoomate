from behave import *

ROOM_URL = "http://127.0.0.1:8000/"

@given("I am on the homepage")
def on_home_page(context):
    context.brower.get(ROOM_URL)