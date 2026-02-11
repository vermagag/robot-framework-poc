"""
Production-ready RF parser with CORRECT argument extraction.
Compatible with Robot Framework 7.3.x
"""
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
import re

from robot.parsing import get_model

print("✅ Robot Framework imports successful!")


@dataclass
class ParsedKeyword:
    """Represents a parsed RF keyword."""
    name: str
    args: List[str] = field(default_factory=list)
    doc: str = ""
    body: List[str] = field(default_factory=list)
    return_value: bool = False
    tags: List[str] = field(default_factory=list)
    source_file: str = ""
    

@dataclass
class ParsedResource:
    """Represents a parsed RF resource file."""
    filename: str
    filepath: str
    keywords: List[ParsedKeyword] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    imports: List[str] = field(default_factory=list)
    library_imports: List[str] = field(default_factory=list)
    

class RFNativeParser:
    """Parser using Robot Framework's native parsing API."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        
    def _extract_keyword_name_and_args(self, full_name: str) -> tuple[str, List[str]]:
        """
        Extract keyword name and arguments from RF keyword definition.
        
        RF Format: "Keyword Name [Arguments] ${arg1} ${arg2}"
        Returns: ("Keyword Name", ["arg1", "arg2"])
        """
        # Check if [Arguments] is inline in the keyword name
        if '[Arguments]' in full_name:
            parts = full_name.split('[Arguments]')
            keyword_name = parts[0].strip()
            
            # Extract arguments from the second part
            args = []
            if len(parts) > 1:
                args_str = parts[1].strip()
                # Find all ${varname} patterns
                arg_matches = re.findall(r'\$\{([^}]+)\}', args_str)
                args = arg_matches
                
            return keyword_name, args
        else:
            # No inline arguments
            return full_name.strip(), []
        
    def parse_robot_file(self, filepath: str) -> ParsedResource:
        """Parse a .robot file using RF's native parser."""
        filepath = Path(filepath)
        
        model = get_model(str(filepath))
        
        result = ParsedResource(
            filename=filepath.name,
            filepath=str(filepath)
        )
        
        # Parse all sections
        for section in model.sections:
            if not hasattr(section, 'header') or not section.header:
                continue
                
            header_type = getattr(section.header, 'type', None)
            
            # Settings section
            if header_type == 'SETTING HEADER':
                for item in section.body:
                    item_type = getattr(item, 'type', None)
                    if item_type == 'RESOURCE' and hasattr(item, 'name'):
                        result.imports.append(item.name)
                    elif item_type == 'LIBRARY' and hasattr(item, 'name'):
                        result.library_imports.append(item.name)
                        
            # Variables section
            elif header_type == 'VARIABLE HEADER':
                for item in section.body:
                    if getattr(item, 'type', None) == 'VARIABLE':
                        var_name = item.name.strip('${}@&')
                        var_value = ' '.join(str(v) for v in item.value) if hasattr(item, 'value') else ''
                        result.variables[var_name] = var_value
                        
            # Keywords section
            elif header_type == 'KEYWORD HEADER':
                for item in section.body:
                    if hasattr(item, 'name') and item.name:
                        parsed_kw = self._parse_keyword(item, str(filepath))
                        if parsed_kw:
                            result.keywords.append(parsed_kw)
                            
        return result
        
    def _parse_keyword(self, keyword_node, source_file: str) -> Optional[ParsedKeyword]:
        """Parse a single keyword with CORRECT argument extraction."""
        if not hasattr(keyword_node, 'name') or not keyword_node.name:
            return None
        
        # Extract keyword name and inline arguments
        keyword_name, inline_args = self._extract_keyword_name_and_args(keyword_node.name)
            
        kw = ParsedKeyword(
            name=keyword_name,
            args=inline_args,  # Start with inline args
            source_file=source_file
        )
        
        # Parse keyword body
        if not hasattr(keyword_node, 'body'):
            return kw
            
        for item in keyword_node.body:
            item_type = getattr(item, 'type', None) if hasattr(item, 'type') else None
            
            if not item_type:
                item_type = item.__class__.__name__.upper()
            
            if item_type == 'ARGUMENTS':
                # Also check for [Arguments] in separate line
                # This will ADD to any inline arguments already found
                if hasattr(item, 'tokens'):
                    for token in item.tokens:
                        if hasattr(token, 'value') and token.value:
                            val = token.value.strip()
                            if val.startswith('${') and val.endswith('}'):
                                arg_name = val.strip('${}')
                                if arg_name not in kw.args:  # Avoid duplicates
                                    kw.args.append(arg_name)
                                
            elif item_type == 'DOCUMENTATION':
                if hasattr(item, 'value'):
                    kw.doc = item.value
                elif hasattr(item, 'tokens'):
                    kw.doc = ' '.join(t.value for t in item.tokens if hasattr(t, 'value') and t.value)
                    
            elif item_type == 'TAGS':
                if hasattr(item, 'values'):
                    kw.tags = list(item.values)
                    
            elif 'RETURN' in item_type:
                kw.return_value = True
                
            elif 'KEYWORD' in item_type or item_type in ['IF', 'FOR', 'WHILE', 'TRY']:
                if hasattr(item, 'keyword') and item.keyword:
                    kw.body.append(str(item.keyword))
                elif hasattr(item, 'name') and item.name:
                    kw.body.append(str(item.name))
                    
        return kw
        
    def parse_directory(self, directory: str, pattern: str = "*.robot") -> List[ParsedResource]:
        """Parse all .robot files in a directory."""
        directory = Path(directory)
        results = []
        
        for robot_file in sorted(directory.rglob(pattern)):
            if robot_file.is_file():
                try:
                    parsed = self.parse_robot_file(robot_file)
                    results.append(parsed)
                    
                    # Show parsed details
                    print(f"✅ Parsed: {robot_file.name}")
                    print(f"   Keywords: {len(parsed.keywords)}")
                    if parsed.keywords:
                        for kw in parsed.keywords[:3]:  # Show first 3
                            print(f"     - {kw.name} ({len(kw.args)} args: {', '.join(kw.args)})")
                        if len(parsed.keywords) > 3:
                            print(f"     ... and {len(parsed.keywords) - 3} more")
                    
                except Exception as e:
                    print(f"⚠️  Failed to parse {robot_file.name}: {e}")
                    import traceback
                    traceback.print_exc()
                    
        return results
        
    def analyze_keyword_dependencies(self, parsed_files: List[ParsedResource]) -> Dict[str, Set[str]]:
        """Analyze keyword dependencies."""
        dependencies = {}
        
        all_keywords = {}
        for pf in parsed_files:
            for kw in pf.keywords:
                all_keywords[kw.name.lower()] = kw
                
        for pf in parsed_files:
            for kw in pf.keywords:
                deps = set()
                for body_item in kw.body:
                    body_lower = body_item.lower()
                    for known_kw in all_keywords.keys():
                        if known_kw in body_lower:
                            deps.add(known_kw)
                            
                if deps:
                    dependencies[kw.name] = deps
                    
        return dependencies
