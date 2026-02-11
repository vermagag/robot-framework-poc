"""
Pytest version of the Robot Framework signup test.
Uses AUTO-GENERATED wrappers from production_generated/
"""
import pytest
import time
from pytest_rf_bridge.pytest_fixtures import rf_bridge, test_credentials, alert_messages
from pytest_rf_bridge.production_generated.common_keywords import CommonKeywords
from pytest_rf_bridge.production_generated.loginscreen_keywords import LoginKeywords
from pytest_rf_bridge.production_generated.navigationbar_keywords import NavigationKeywords


@pytest.mark.smoke
def test_signup_new_user(rf_bridge, test_credentials, alert_messages):
    """
    Verify that a new user can sign up to the application.
    
    This test uses AUTO-GENERATED Python wrappers from RF keywords.
    """
    # Initialize keyword wrappers
    common = CommonKeywords(rf_bridge)
    login = LoginKeywords(rf_bridge)
    navigation = NavigationKeywords(rf_bridge)
    
    # Generate random email for signup
    random_email = common.get_random_email_address()
    
    # Test steps (matching RF test)
    print("\n📱 Step 1: Navigating to login screen...")
    navigation.navigate_to_login_screen()
    
    print("📱 Step 2: Clicking on signup container...")
    login.click_on_the_sign_up_container()
    
    print("📱 Step 3: Waiting for signup form to load...")
    time.sleep(2)
    
    print(f"📱 Step 4: Signing up with email: {random_email}")
    login.sign_up_to_the_application(random_email, test_credentials["password"], test_credentials["password"])
    
    print("📱 Step 5: Verifying success alert...")
    common.alert_title_should_be(alert_messages["signup_success_title"])
    common.alert_message_should_be(alert_messages["signup_success_message"])
    
    print(f"\n✅ Signup test completed successfully using AUTO-GENERATED RF keywords in pytest!")
    print(f"   Generated email: {random_email}")
