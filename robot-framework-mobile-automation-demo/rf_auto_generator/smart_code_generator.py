"""
Smart code generator that creates proper implementations based on keyword analysis.
"""
from pathlib import Path
from typing import Dict, List, Set
import re
from rf_auto_generator.rf_native_parser import ParsedResource, ParsedKeyword


class SmartCodeGenerator:
    """
    Generates Python code with proper implementations based on:
    - Keyword names (pattern matching)
    - Keyword dependencies (call chains)
    - Arguments structure
    - RF library usage
    """
    
    def __init__(self, output_dir: str = "pytest_rf_bridge/auto_generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track all generated keywords to avoid conflicts
        self.generated_keywords = set()
        
        # Map of RF library keywords to bridge methods
        self.library_mapping = {
            'Open Application': 'self.bridge.appium.open_application',
            'Close Application': 'self.bridge.close_application',
            'Click Element': 'self.bridge.click_element',
            'Input Text': 'self.bridge.input_text',
            'Wait Until Element Is Visible': 'self.bridge.appium.wait_until_element_is_visible',
            'Wait Until Page Contains Element': 'self.bridge.appium.wait_until_page_contains_element',
            'Element Text Should Be': 'self.bridge.element_text_should_be',
            'Set Appium Timeout': 'self.bridge.appium.set_appium_timeout',
        }
        
    def sanitize_name(self, name: str) -> str:
        """Convert RF keyword name to valid Python method name."""
        # Remove special characters, replace spaces with underscores
        name = re.sub(r"['\"]", '', name)  # Remove quotes
        name = re.sub(r'[^\w\s]', '', name)  # Remove special chars except spaces
        name = name.replace(' ', '_').lower()
        return name
        
    def convert_arg_name(self, arg: str) -> str:
        """Convert RF argument to Python parameter name."""
        # Convert camelCase to snake_case
        arg = re.sub(r'(?<!^)(?=[A-Z])', '_', arg).lower()
        # Remove any remaining special characters
        arg = re.sub(r'[^\w]', '_', arg)
        return arg
        
    def infer_keyword_type(self, keyword: ParsedKeyword) -> str:
        """
        Infer what type of keyword this is based on name and body.
        Returns: 'action', 'verification', 'utility', 'composite', 'library_call'
        """
        name_lower = keyword.name.lower()
        
        # Check if it directly calls library keywords
        if any(lib_kw.lower() in str(keyword.body).lower() for lib_kw in self.library_mapping.keys()):
            return 'library_call'
            
        # Verification keywords
        if any(word in name_lower for word in ['should', 'verify', 'check', 'assert', 'validate']):
            return 'verification'
            
        # Action keywords
        if any(word in name_lower for word in ['click', 'input', 'type', 'select', 'press', 'tap', 'swipe']):
            return 'action'
            
        # Utility keywords (getters, generators)
        if any(word in name_lower for word in ['get', 'generate', 'create', 'random']):
            return 'utility'
            
        # Composite keywords (call multiple other keywords)
        if len(keyword.body) > 2:
            return 'composite'
            
        return 'action'  # Default
        
    def generate_implementation(self, keyword: ParsedKeyword, locators: Dict[str, str]) -> str:
        """
        Generate smart implementation based on keyword analysis.
        """
        kw_type = self.infer_keyword_type(keyword)
        name_lower = keyword.name.lower()
        args = keyword.args
        
        # Convert args to Python params
        py_args = [self.convert_arg_name(arg) for arg in args]
        
        # Generate implementation based on type
        if kw_type == 'library_call':
            return self._generate_library_call_impl(keyword, py_args, locators)
        elif kw_type == 'verification':
            return self._generate_verification_impl(keyword, py_args, locators)
        elif kw_type == 'action':
            return self._generate_action_impl(keyword, py_args, locators)
        elif kw_type == 'utility':
            return self._generate_utility_impl(keyword, py_args)
        elif kw_type == 'composite':
            return self._generate_composite_impl(keyword, py_args, locators)
        else:
            return "        pass  # TODO: Implement this keyword"
            
    def _generate_library_call_impl(self, kw: ParsedKeyword, py_args: List[str], locators: Dict) -> str:
        """Generate implementation for library call keywords."""
        name_lower = kw.name.lower()
        
        # Match patterns
        if 'click element' in name_lower:
            if py_args:
                # Check if first arg is a locator variable
                locator_arg = py_args[0]
                retry_arg = py_args[1] if len(py_args) > 1 else "None"
                return f"        self.bridge.click_element({locator_arg}, {retry_arg})"
            return "        pass  # Click element - args needed"
            
        elif 'input text' in name_lower:
            if len(py_args) >= 2:
                return f"        self.bridge.input_text({py_args[0]}, {py_args[1]}, {py_args[2] if len(py_args) > 2 else 'None'})"
            return "        pass  # Input text - args needed"
            
        elif 'open' in name_lower and 'application' in name_lower:
            if 'android' in name_lower:
                return "        self.bridge.open_android_application()"
            return "        self.bridge.open_android_application()"
            
        elif 'close' in name_lower and 'application' in name_lower:
            return "        self.bridge.close_application()"
            
        return "        pass  # Library call - implement based on RF library"
        
    def _generate_verification_impl(self, kw: ParsedKeyword, py_args: List[str], locators: Dict) -> str:
        """Generate implementation for verification keywords."""
        name_lower = kw.name.lower()
        
        if 'alert' in name_lower and 'title' in name_lower:
            if py_args:
                return f"        self.bridge.alert_title_should_be({py_args[0]})"
                
        elif 'alert' in name_lower and 'message' in name_lower:
            if py_args:
                return f"        self.bridge.alert_message_should_be({py_args[0]})"
                
        elif 'should be visible' in name_lower or 'visible' in name_lower:
            if py_args:
                return f"        self.bridge.element_should_be_visible({', '.join(py_args)})"
                
        elif 'text should be' in name_lower:
            if len(py_args) >= 2:
                return f"        self.bridge.element_text_should_be({', '.join(py_args)})"
                
        return "        pass  # Verification - implement assertion"
        
    def _generate_action_impl(self, kw: ParsedKeyword, py_args: List[str], locators: Dict) -> str:
        """Generate implementation for action keywords."""
        # Actions usually delegate to lower-level keywords
        impl = "        # Action keyword\n"
        for body_line in kw.body[:3]:  # Show first 3 lines as comments
            impl += f"        # {body_line}\n"
        impl += "        pass  # TODO: Implement action"
        return impl
        
    def _generate_utility_impl(self, kw: ParsedKeyword, py_args: List[str]) -> str:
        """Generate implementation for utility keywords."""
        name_lower = kw.name.lower()
        
        if 'random email' in name_lower:
            return "        return self.bridge.get_random_email_address()"
        elif 'random text' in name_lower:
            if py_args:
                return f"        return self.bridge.get_random_text({py_args[0]})"
            return "        return self.bridge.get_random_text()"
        elif 'epoch time' in name_lower:
            return "        import time\n        return int(time.time())"
            
        return "        pass  # Utility - implement helper function"
        
    def _generate_composite_impl(self, kw: ParsedKeyword, py_args: List[str], locators: Dict) -> str:
        """Generate implementation for composite keywords (call multiple keywords)."""
        impl = "        # Composite keyword - orchestrates multiple actions\n"
        
        # List called keywords as comments
        for body_line in kw.body:
            impl += f"        # Calls: {body_line}\n"
            
        impl += "        pass  # TODO: Implement composite workflow"
        return impl
        
    def generate_class(self, parsed: ParsedResource, locators: Dict[str, str] = None) -> str:
        """Generate complete Python class from parsed RF resource."""
        base_name = Path(parsed.filename).stem.replace('Po', '').replace('Screen', '').replace('Bar', '')
        class_name = f"{base_name}Keywords"
        
        code = f'''"""
Auto-generated from: {parsed.filename}
Total keywords: {len(parsed.keywords)}
Libraries: {', '.join(parsed.library_imports)}

Generated using RF native parser - handles ALL RF syntax correctly.
"""


class {class_name}:
    """
    Wrapper for RF keywords from {base_name}.
    
    Keywords in this class: {len(parsed.keywords)}
    """
    
'''
        
        # Add locators as class constants
        if locators:
            code += "    # Locators\n"
            for loc_name, loc_value in locators.items():
                const_name = self._locator_to_const(loc_name)
                code += f'    {const_name} = "{loc_value}"\n'
            code += "\n"
            
        # Constructor
        code += '''    def __init__(self, bridge):
        """Initialize with RF bridge."""
        self.bridge = bridge
        
'''
        
        # Generate methods for each keyword
        for kw in parsed.keywords:
            method_code = self._generate_method(kw, locators or {})
            code += method_code
            
        return code
        
    def _locator_to_const(self, name: str) -> str:
        """Convert locator name to Python constant."""
        # signupContainer -> SIGNUP_CONTAINER
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
        return name.upper()
        
    def _generate_method(self, kw: ParsedKeyword, locators: Dict) -> str:
        """Generate a single method."""
        method_name = self.sanitize_name(kw.name)
        py_args = [self.convert_arg_name(arg) for arg in kw.args]
        
        # Method signature
        params = ""
        if py_args:
            params = ", " + ", ".join(py_args)
            
        doc = kw.doc if kw.doc else f"Execute RF keyword: {kw.name}"
        
        # Generate implementation
        impl = self.generate_implementation(kw, locators)
        
        code = f'''    def {method_name}(self{params}):
        """
        {doc}
        
        RF Keyword: {kw.name}
        Arguments: {', '.join(kw.args) if kw.args else 'None'}
        Returns: {'Yes' if kw.return_value else 'No'}
        """
{impl}
        
'''
        return code
        
    def generate_all(self, parsed_files: List[ParsedResource], locators_map: Dict[str, Dict] = None) -> Dict[str, str]:
        """Generate all wrapper files."""
        generated = {}
        
        for parsed in parsed_files:
            base_name = Path(parsed.filename).stem.replace('Po', '')
            
            # Get locators for this file
            locators = {}
            if locators_map:
                # Try to find matching locators
                for loc_key, loc_vars in locators_map.items():
                    if loc_key.lower() in base_name.lower():
                        locators = loc_vars
                        break
                        
            # Generate class
            code = self.generate_class(parsed, locators)
            
            # Write to file
            output_file = self.output_dir / f"{self.sanitize_name(base_name)}_keywords.py"
            with open(output_file, 'w') as f:
                f.write(code)
                
            generated[str(output_file)] = code
            print(f"✅ Generated: {output_file.name} ({len(parsed.keywords)} keywords)")
            
        return generated
