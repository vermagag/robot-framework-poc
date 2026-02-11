"""
Pytest version of the Robot Framework login test.
Uses AUTO-GENERATED wrappers from production_generated/
"""
import pytest
from pytest_rf_bridge.pytest_fixtures import rf_bridge, test_credentials, alert_messages
from pytest_rf_bridge.production_generated.common_keywords import CommonKeywords
from pytest_rf_bridge.production_generated.loginscreen_keywords import LoginKeywords
from pytest_rf_bridge.production_generated.navigationbar_keywords import NavigationKeywords


@pytest.mark.smoke
def test_login_with_valid_credentials(rf_bridge, test_credentials, alert_messages):
    """
    Verify that a user can login to the application using valid credentials.
    
    This test uses AUTO-GENERATED Python wrappers from RF keywords.
    """
    # Initialize keyword wrappers
    common = CommonKeywords(rf_bridge)
    login = LoginKeywords(rf_bridge)
    navigation = NavigationKeywords(rf_bridge)
    
    # Test steps (matching RF test)
    navigation.navigate_to_login_screen()
    login.login_to_application(test_credentials["email"], test_credentials["password"])
    common.alert_title_should_be(alert_messages["login_success_title"])
    common.alert_message_should_be(alert_messages["login_success_message"])
    
    print("\n✅ Login test completed successfully using AUTO-GENERATED RF keywords in pytest!")
