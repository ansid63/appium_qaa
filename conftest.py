import pytest
import os
import allure
import textwrap
import sys
import copy
from datetime import datetime
from appium import webdriver


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope='function')
def driver(request):
    ANDROID_BASE_CAPS = {
    'app': os.path.abspath('ApiDemos-debug.apk'),
    'automationName': 'UIAutomator2',
    'platformName': 'Android',
    'platformVersion': '11.0',
    'deviceName': 'Android Emulator',
    'appActivity': '.app.SearchInvoke'}
    PACKAGE = 'io.appium.android.apis'
    ALERT_DIALOG_ACTIVITY = '.app.AlertDialogSamples'


    EXECUTOR = 'http://127.0.0.1:4723/wd/hub'

    caps = copy.copy(ANDROID_BASE_CAPS)

    driver = webdriver.Remote(
        command_executor=EXECUTOR,
        desired_capabilities=caps
    )

    driver.implicitly_wait(10)
    yield driver
    
    if request.node.rep_call.failed:
        try:
            allure.attach(driver.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
        except:
            pass

    driver.quit()