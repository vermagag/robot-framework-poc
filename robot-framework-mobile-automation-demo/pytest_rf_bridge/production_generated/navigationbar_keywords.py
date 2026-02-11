"""
Auto-generated from: NavigationBarPo.robot
Total keywords: 1
Libraries: 

Generated using RF native parser - handles ALL RF syntax correctly.
"""


class NavigationKeywords:
    """
    Wrapper for RF keywords from Navigation.
    
    Keywords in this class: 1
    """
    
    # Locators
    LOGIN_ICON = "accessibility_id=Login"

    def __init__(self, bridge):
        """Initialize with RF bridge."""
        self.bridge = bridge
        
    def navigate_to_login_screen(self):
        """Navigate to the login screen."""
        self.bridge.click_element(self.LOGIN_ICON, self.bridge.small_retry_count)
