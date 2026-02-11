"""
Core bridge that wraps Robot Framework's AppiumLibrary for use in pytest.
This allows pytest tests to use RF keywords directly.
"""
import os
from AppiumLibrary import AppiumLibrary
from robot.libraries.BuiltIn import BuiltIn
import string
import random
import time


class RobotKeywordBridge:
    """
    Bridge class that wraps AppiumLibrary and provides RF keyword functionality to pytest.
    """
    
    def __init__(self):
        self.appium = AppiumLibrary()
        self.timeout = 60
        self.retry_delay = 1  # seconds
        
        # Android configuration
        self.appium_server_url = "http://localhost:4723"
        self.android_automation_name = "UIAutomator2"
        self.android_platform_name = "android"
        self.android_platform_version = os.getenv("ANDROID_PLATFORM_VERSION", "13")
        self.android_device_name = "Pixel 6"
        
        # Get the app path relative to the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.android_app = os.path.join(project_root, "apps", "wdioNativeDemoApp.apk")
        self.android_app_package = "com.wdiodemoapp"
        self.android_app_activity = ".MainActivity"
        
        # Retry counts
        self.small_retry_count = 2
        self.medium_retry_count = 3
        self.large_retry_count = 5
        
    def open_android_application(self):
        """Open the Android application."""
        self.appium.open_application(
            self.appium_server_url,
            automationName=self.android_automation_name,
            platformName=self.android_platform_name,
            platformVersion=self.android_platform_version,
            deviceName=self.android_device_name,
            app=self.android_app,
            appPackage=self.android_app_package,
            appActivity=self.android_app_activity
        )
        self.appium.set_appium_timeout(self.timeout)
        
    def close_application(self):
        """Close the application."""
        self.appium.close_application()
        
    def click_element(self, locator, retry_count=None):
        """Click on an element with retry logic."""
        if retry_count is None:
            retry_count = self.small_retry_count
            
        for attempt in range(retry_count):
            try:
                self.appium.wait_until_element_is_visible(locator, self.timeout)
                self.appium.click_element(locator)
                return
            except Exception as e:
                if attempt == retry_count - 1:
                    raise
                time.sleep(self.retry_delay)
                
    def input_text(self, locator, text, retry_count=None):
        """Input text into an element with retry logic."""
        if retry_count is None:
            retry_count = self.small_retry_count
            
        for attempt in range(retry_count):
            try:
                self.appium.wait_until_element_is_visible(locator, self.timeout)
                self.appium.input_text(locator, text)
                return
            except Exception as e:
                if attempt == retry_count - 1:
                    raise
                time.sleep(self.retry_delay)
                
    def element_text_should_be(self, locator, expected_text, retry_count=None):
        """Verify element text matches expected value."""
        if retry_count is None:
            retry_count = self.small_retry_count
            
        for attempt in range(retry_count):
            try:
                self.appium.wait_until_element_is_visible(locator, self.timeout)
                self.appium.element_text_should_be(locator, expected_text)
                return
            except Exception as e:
                if attempt == retry_count - 1:
                    raise
                time.sleep(self.retry_delay)
                
    def element_should_be_visible(self, locator, retry_count=None):
        """Verify element is visible."""
        if retry_count is None:
            retry_count = self.small_retry_count
            
        for attempt in range(retry_count):
            try:
                self.appium.wait_until_element_is_visible(locator, self.timeout)
                return
            except Exception as e:
                if attempt == retry_count - 1:
                    raise
                time.sleep(self.retry_delay)
                
    def get_random_text(self, length=8):
        """Generate random text string."""
        return ''.join(random.choices(string.ascii_letters, k=length))
        
    def get_random_email_address(self):
        """Generate random email address."""
        random_text = self.get_random_text()
        return f"{random_text}@mailinator.com"
        
    def alert_title_should_be(self, expected_title):
        """Verify alert title (Android specific)."""
        android_alert_title_locator = "id=android:id/alertTitle"
        self.element_text_should_be(android_alert_title_locator, expected_title, self.small_retry_count)
        
    def alert_message_should_be(self, expected_message):
        """Verify alert message (Android specific)."""
        android_alert_message_locator = "id=android:id/message"
        self.element_text_should_be(android_alert_message_locator, expected_message, self.small_retry_count)
