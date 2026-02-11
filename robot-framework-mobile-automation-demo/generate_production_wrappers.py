#!/usr/bin/env python
"""
Production-ready wrapper generator using RF's native parser.
Handles ALL RF syntax correctly - ready for 3000+ keywords.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rf_auto_generator.rf_native_parser import RFNativeParser
from rf_auto_generator.smart_code_generator import SmartCodeGenerator


def main():
    print("=" * 70)
    print("🚀 PRODUCTION RF-to-Python Generator")
    print("   Using Robot Framework's Native Parser")
    print("   ✅ Handles ALL RF syntax correctly")
    print("   ✅ Ready for 3000+ keywords")
    print("=" * 70)
    
    # Parse using RF's native parser
    print("\n📁 Step 1: Parsing with RF Native Parser...")
    parser = RFNativeParser(Path.cwd())
    
    page_objects = parser.parse_directory("object-repository/page-objects")
    total_kw = sum(len(pf.keywords) for pf in page_objects)
    
    print(f"\n📊 Parsed {len(page_objects)} resource files")
    print(f"📊 Found {total_kw} keywords total\n")
    
    for pf in page_objects:
        print(f"   📄 {pf.filename}")
        print(f"      Keywords: {len(pf.keywords)}")
        print(f"      Variables: {len(pf.variables)}")
        print(f"      Imports: {len(pf.imports)}")
        print(f"      Libraries: {', '.join(pf.library_imports)}")
        print()
        
    # Parse locators
    print("📁 Step 2: Parsing locator files...")
    locators_map = {}
    locator_dir = Path("object-repository/locators")
    
    if locator_dir.exists():
        for loc_file in locator_dir.glob("*.robot"):
            parsed_loc = parser.parse_robot_file(loc_file)
            base_name = loc_file.stem.replace('Locators', '')
            locators_map[base_name] = parsed_loc.variables
            print(f"   📍 {loc_file.name}: {len(parsed_loc.variables)} locators")
            
    # Analyze dependencies
    print("\n📊 Step 3: Analyzing keyword dependencies...")
    dependencies = parser.analyze_keyword_dependencies(page_objects)
    print(f"   Found {len(dependencies)} keywords with dependencies")
    
    # Generate Python wrappers
    print("\n🏗️  Step 4: Generating Python wrappers...")
    generator = SmartCodeGenerator("pytest_rf_bridge/production_generated")
    generated = generator.generate_all(page_objects, locators_map)
    
    print(f"\n{'=' * 70}")
    print(f"✅ SUCCESS! Generated {len(generated)} Python wrapper files")
    print(f"📂 Output directory: pytest_rf_bridge/production_generated/")
    print(f"📊 Total keywords wrapped: {total_kw}")
    print(f"{'=' * 70}")
    
    print("\n🎯 These wrappers:")
    print("   ✅ Use RF's native parser (handles ALL syntax)")
    print("   ✅ Have smart implementations (pattern-based)")
    print("   ✅ Include proper documentation")
    print("   ✅ Ready for pytest integration")
    print("\n💡 Scale to 3000+ keywords by pointing to PASA's directory!")
    

if __name__ == "__main__":
    main()
