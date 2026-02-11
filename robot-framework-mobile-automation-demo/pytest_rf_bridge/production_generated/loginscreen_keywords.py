"""
Auto-generated from: LoginScreenPo.robot
Total keywords: 8
Libraries: 

Generated using RF native parser - handles ALL RF syntax correctly.
"""


class LoginKeywords:
    """
    Wrapper for RF keywords from Login.
    
    Keywords in this class: 8
    """
    
    # Locators
    SIGNUP_CONTAINER = "accessibility_id=button-sign-up-container"
    EMAIL_ADDRESS_TEXTBOX = "accessibility_id=input-email"
    PASSWORD_TEXTBOX = "accessibility_id=input-password"
    CONFIRM_PASSWORD_TEXTBOX = "accessibility_id=input-repeat-password"
    SIGNUP_BUTTON = "accessibility_id=button-SIGN UP"
    LOGIN_BUTTON = "accessibility_id=button-LOGIN"

    def __init__(self, bridge):
        """Initialize with RF bridge."""
        self.bridge = bridge
        
    def sign_up_to_the_application(self, email_address, password, confirm_password):
        """Complete signup flow."""
        self.input_email_address(email_address)
        self.input_password(password)
        self.input_confirm_password(confirm_password)
        self.click_on_the_sign_up_button()
        
    def login_to_application(self, email_address, password):
        """Complete login flow."""
        self.input_email_address(email_address)
        self.input_password(password)
        self.click_on_the_login_button()
        
    def click_on_the_sign_up_container(self):
        """Click on the 'Sign up' container."""
        self.bridge.click_element(self.SIGNUP_CONTAINER, self.bridge.small_retry_count)
        
    def input_email_address(self, email_address):
        """Input email address."""
        self.bridge.input_text(self.EMAIL_ADDRESS_TEXTBOX, email_address, self.bridge.small_retry_count)
        
    def input_password(self, password):
        """Input password."""
        self.bridge.input_text(self.PASSWORD_TEXTBOX, password, self.bridge.small_retry_count)
        
    def input_confirm_password(self, confirm_password):
        """Input confirm password."""
        self.bridge.input_text(self.CONFIRM_PASSWORD_TEXTBOX, confirm_password, self.bridge.small_retry_count)
        
    def click_on_the_sign_up_button(self):
        """Click on the 'SIGN UP' button."""
        self.bridge.click_element(self.SIGNUP_BUTTON, self.bridge.small_retry_count)
        
    def click_on_the_login_button(self):
        """Click on the 'LOGIN' button."""
        self.bridge.click_element(self.LOGIN_BUTTON, self.bridge.small_retry_count)
