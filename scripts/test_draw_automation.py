#!/usr/bin/env python3
"""
🧪 Test script for Draw Automation System
Tests the draw automation with sample data.
"""

import json
import sys
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent))

from draw_automation import DrawAutomationSystem

def test_draw_automation():
    """Test the draw automation system with sample data."""
    
    print("🧪 Testing Draw Automation System...")
    
    # Sample draw data
    test_data = {
        "headline": "Express Entry Health Draw: 4,500 ITAs Issued at CRS 470",
        "summary": "IRCC conducted a healthcare-specific draw on July 25, 2025",
        "invitation": 4500,
        "cutoff": 470,
        "draw_type": "Health",
        "date": "2025-07-25",
        "source": "IRCC Official",
        "impact_level": "Critical"
    }
    
    # Initialize automation system
    automation = DrawAutomationSystem()
    
    try:
        # Process the test data
        result = automation.process_draw_data(test_data)
        
        if result["success"]:
            print("✅ Test PASSED!")
            print(f"📄 Article URL: {result['article_url']}")
            print(f"📝 Title: {result['title']}")
            print(f"💬 Message: {result['message']}")
        else:
            print("❌ Test FAILED!")
            print(f"🚨 Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test FAILED with exception: {e}")
        import traceback
        traceback.print_exc()

def test_template_variables():
    """Test template variable replacement."""
    
    print("\n🔧 Testing Template Variable Replacement...")
    
    automation = DrawAutomationSystem()
    
    # Sample analysis data
    analysis = {
        "title": "Test Draw Article",
        "description": "Test description",
        "keywords": "test, keywords",
        "executive_summary": "Test executive summary",
        "immediate_effects": "Test immediate effects",
        "strategic_implications": "Test strategic implications",
        "quick_facts": ["Fact 1", "Fact 2"],
        "user_impact": {
            "user_type_1": {"icon": "🇨🇦", "title": "Test", "description": "Test description"},
            "user_type_2": {"icon": "📋", "title": "Test", "description": "Test description"},
            "user_type_3": {"icon": "🏢", "title": "Test", "description": "Test description"}
        },
        "next_steps": ["<li>Step 1</li>", "<li>Step 2</li>"],
        "draw_details": ["<li>Detail 1</li>"],
        "source_links": ["<li>Link 1</li>"],
        "tags": ["<a href='#'>Tag 1</a>"],
        "article_content": "<p>Test content</p>",
        "draw_config": {
            "icon": "🏥",
            "name": "Health",
            "gradient": "#dc2626 0%, #b91c1c 100%",
            "summary": "Test summary"
        },
        "impact_level": "Critical",
        "itas": 4500,
        "crs": 470,
        "draw_type": "Health",
        "date": "2025-07-25"
    }
    
    try:
        # Test template variable replacement
        content = automation.replace_template_variables(analysis)
        
        # Check if key variables were replaced
        if "{{TITLE}}" in content:
            print("❌ Template variables not replaced properly")
        else:
            print("✅ Template variable replacement working correctly")
            
    except Exception as e:
        print(f"❌ Template variable test failed: {e}")

def test_draw_types():
    """Test draw type configurations."""
    
    print("\n🎯 Testing Draw Type Configurations...")
    
    automation = DrawAutomationSystem()
    
    # Test all draw types
    test_draw_types = ["CEC", "Health", "PNP", "General", "FSTP", "FSWP"]
    
    for draw_type in test_draw_types:
        if draw_type in automation.draw_types:
            config = automation.draw_types[draw_type]
            print(f"✅ {draw_type}: {config['name']} - {config['icon']}")
        else:
            print(f"❌ {draw_type}: Not found in configurations")

def test_impact_levels():
    """Test impact level calculations."""
    
    print("\n⚡ Testing Impact Level Calculations...")
    
    automation = DrawAutomationSystem()
    
    # Test different ITA counts
    test_cases = [
        (5000, "Critical"),
        (3000, "High"),
        (1500, "Moderate"),
        (500, "Low")
    ]
    
    for itas, expected_impact in test_cases:
        test_data = {
            "invitation": itas,
            "cutoff": 500,
            "draw_type": "General",
            "date": "2025-07-25"
        }
        
        analysis = automation.analyze_draw_data(test_data)
        actual_impact = analysis["impact_level"]
        
        if actual_impact == expected_impact:
            print(f"✅ {itas} ITAs → {actual_impact}")
        else:
            print(f"❌ {itas} ITAs → Expected {expected_impact}, got {actual_impact}")

if __name__ == "__main__":
    print("🎯 Draw Automation System Test Suite")
    print("=" * 50)
    
    # Run all tests
    test_draw_types()
    test_impact_levels()
    test_template_variables()
    test_draw_automation()
    
    print("\n🏁 Test suite completed!") 