"""
Pytest fixtures for Robot Framework keyword bridge.
Provides setup and teardown functionality for tests.
"""
import pytest
import os
from pytest_rf_bridge.rf_keyword_bridge import RobotKeywordBridge


@pytest.fixture(scope="function")
def rf_bridge():
    """
    Fixture that provides a RobotKeywordBridge instance.
    Sets up the application before each test and tears it down after.
    """
    # Ensure environment variables are set
    android_home = os.path.expanduser("~/android-sdk")
    os.environ["ANDROID_HOME"] = android_home
    os.environ["ANDROID_SDK_ROOT"] = android_home
    
    # Create bridge instance
    bridge = RobotKeywordBridge()
    
    # Setup: Open application
    bridge.open_android_application()
    
    # Provide bridge to test
    yield bridge
    
    # Teardown: Close application
    try:
        bridge.close_application()
    except:
        pass  # Ignore errors during teardown


@pytest.fixture(scope="session")
def test_credentials():
    """
    Fixture that provides test credentials.
    """
    return {
        "email": "osanda@mailinator.com",
        "password": "osanda@SL"
    }


@pytest.fixture(scope="session")
def alert_messages():
    """
    Fixture that provides expected alert messages.
    """
    return {
        "login_success_title": "Success",
        "login_success_message": "You are logged in!",
        "signup_success_title": "Signed Up!",
        "signup_success_message": "You successfully signed up!"
    }