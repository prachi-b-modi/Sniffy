#!/usr/bin/env python3
"""
Unit tests for the Website Overlay Generation Agent

Testing Framework: unittest (Python standard library)
Testing approach: Comprehensive unit tests covering all functionality paths
"""

import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to sys.path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module under test
from overlay_agent_dir.overlay_agent import generate_website_overlay_js, root_agent


class TestGenerateWebsiteOverlayJS(unittest.TestCase):
    """Test cases for the generate_website_overlay_js function"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.maxDiff = None  # Allow full diff output for long strings

    def test_red_background_generation(self):
        """Test generation of red background JavaScript code"""
        prompt = "change the background to red"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("js_code", result)
        self.assertIn("description", result)
        self.assertIn("document.body.style.backgroundColor = 'red'", result["js_code"])
        self.assertIn("Background changed to red", result["js_code"])
        self.assertIn("change the background to red", result["description"])

    def test_red_background_case_insensitive(self):
        """Test red background detection is case insensitive"""
        prompts = [
            "Change the BACKGROUND to RED",
            "background RED please",
            "make Background Red"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("document.body.style.backgroundColor = 'red'", result["js_code"])

    def test_blue_background_generation(self):
        """Test generation of blue background JavaScript code"""
        prompt = "change the background to blue"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("document.body.style.backgroundColor = 'blue'", result["js_code"])
        self.assertIn("Background changed to blue", result["js_code"])

    def test_green_background_generation(self):
        """Test generation of green background JavaScript code"""
        prompt = "set background to green"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("document.body.style.backgroundColor = 'green'", result["js_code"])
        self.assertIn("Background changed to green", result["js_code"])

    def test_yellow_background_generation(self):
        """Test generation of yellow background JavaScript code"""
        prompt = "make background yellow"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("document.body.style.backgroundColor = 'yellow'", result["js_code"])
        self.assertIn("Background changed to yellow", result["js_code"])

    def test_purple_background_generation(self):
        """Test generation of purple background JavaScript code"""
        prompt = "purple background please"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("document.body.style.backgroundColor = 'purple'", result["js_code"])
        self.assertIn("Background changed to purple", result["js_code"])

    def test_default_background_color(self):
        """Test default color when background is mentioned without specific color"""
        prompt = "change the background"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("document.body.style.backgroundColor = 'lightblue'", result["js_code"])
        self.assertIn("Background changed to lightblue", result["js_code"])

    def test_overlay_generation(self):
        """Test generation of Apple-style glass overlay"""
        prompt = "create an overlay"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("glass-overlay", result["js_code"])
        self.assertIn("backdrop-filter: blur(10px)", result["js_code"])
        self.assertIn("Glass Overlay", result["js_code"])
        self.assertIn("Apple-style glass overlay", result["js_code"])
        self.assertIn("overlay.remove()", result["js_code"])

    def test_overlay_case_insensitive(self):
        """Test overlay detection is case insensitive"""
        prompts = [
            "create an OVERLAY",
            "make an Overlay",
            "OVERLAY please"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("glass-overlay", result["js_code"])

    def test_note_overlay_generation(self):
        """Test generation of floating note overlay"""
        prompt = "show a note"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("floating note", result["js_code"])
        self.assertIn("📝 Note", result["js_code"])
        self.assertIn("slideIn", result["js_code"])
        self.assertIn("Dismiss", result["js_code"])

    def test_message_overlay_generation(self):
        """Test generation of message overlay (same as note)"""
        prompt = "display a message"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("floating note", result["js_code"])
        self.assertIn("📝 Note", result["js_code"])

    def test_note_case_insensitive(self):
        """Test note detection is case insensitive"""
        prompts = [
            "show a NOTE",
            "display Message",
            "create a note"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("📝 Note", result["js_code"])

    def test_generic_modification_generation(self):
        """Test generation of generic website modification"""
        prompt = "do something cool"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("Generic website modification", result["js_code"])
        self.assertIn("Website modified:", result["js_code"])
        self.assertIn("do something cool", result["js_code"])
        self.assertIn("setTimeout", result["js_code"])

    def test_long_prompt_truncation(self):
        """Test that long prompts are properly truncated in generic modification"""
        long_prompt = "a" * 100
        result = generate_website_overlay_js(long_prompt)
        
        self.assertEqual(result["status"], "success")
        # Check that the prompt is truncated to 50 characters in the notification
        self.assertIn("a" * 50 + "...", result["js_code"])
        # Check that description is truncated to 100 characters
        self.assertIn("a" * 100 + "...", result["description"])

    def test_empty_prompt(self):
        """Test handling of empty prompt"""
        result = generate_website_overlay_js("")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("Generic website modification", result["js_code"])

    def test_none_prompt(self):
        """Test handling of None prompt"""
        with self.assertRaises(AttributeError):
            generate_website_overlay_js(None)

    def test_special_characters_in_prompt(self):
        """Test handling of special characters in prompt"""
        prompt = "create overlay with <script>alert('test')</script>"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        # Should still work and include the special characters
        self.assertIn("<script>alert('test')</script>", result["js_code"])

    def test_unicode_characters_in_prompt(self):
        """Test handling of unicode characters in prompt"""
        prompt = "créer une superposition avec émojis 🚀 ✨"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("émojis 🚀 ✨", result["js_code"])

    def test_multiple_keywords_red_background_priority(self):
        """Test that red background has priority when multiple background colors mentioned"""
        prompt = "change background to red and blue"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("document.body.style.backgroundColor = 'red'", result["js_code"])

    def test_multiple_keywords_overlay_and_background(self):
        """Test precedence when both overlay and background keywords present"""
        prompt = "create overlay with red background"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        # Red background should take precedence
        self.assertIn("document.body.style.backgroundColor = 'red'", result["js_code"])

    def test_multiple_keywords_overlay_and_note(self):
        """Test precedence when both overlay and note keywords present"""
        prompt = "create overlay note"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        # Overlay should take precedence (first elif condition)
        self.assertIn("glass-overlay", result["js_code"])

    def test_javascript_code_validity(self):
        """Test that generated JavaScript code has valid syntax structure"""
        prompts = [
            "change background to red",
            "create an overlay",
            "show a note",
            "do something"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                js_code = result["js_code"]
                
                # Check for proper IIFE structure
                self.assertIn("(function()", js_code)
                self.assertIn("})();", js_code)
                
                # Check for proper console.log statements
                self.assertIn("console.log(", js_code)

    def test_css_styling_completeness(self):
        """Test that CSS styling in overlays is complete and valid"""
        prompt = "create an overlay"
        result = generate_website_overlay_js(prompt)
        js_code = result["js_code"]
        
        # Check for essential CSS properties
        essential_properties = [
            "position: fixed",
            "z-index:",
            "background:",
            "border-radius:",
            "backdrop-filter:"
        ]
        
        for prop in essential_properties:
            self.assertIn(prop, js_code)

    def test_error_handling_exception(self):
        """Test error handling when an exception occurs"""
        # Mock the function to raise an exception
        with patch('builtins.str', side_effect=Exception("Test error")):
            result = generate_website_overlay_js("test prompt")
            
            self.assertEqual(result["status"], "error")
            self.assertIn("error_message", result)
            self.assertIn("Failed to generate JavaScript code", result["error_message"])

    def test_return_structure_success(self):
        """Test that successful returns have correct structure"""
        result = generate_website_overlay_js("test")
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("js_code", result)
        self.assertIn("description", result)
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["js_code"], str)
        self.assertIsInstance(result["description"], str)

    def test_return_structure_error(self):
        """Test that error returns have correct structure"""
        with patch('builtins.str', side_effect=Exception("Test error")):
            result = generate_website_overlay_js("test")
            
            self.assertIsInstance(result, dict)
            self.assertIn("status", result)
            self.assertIn("error_message", result)
            self.assertEqual(result["status"], "error")
            self.assertIsInstance(result["error_message"], str)

    def test_js_code_stripped(self):
        """Test that JavaScript code is properly stripped of leading/trailing whitespace"""
        result = generate_website_overlay_js("test")
        
        js_code = result["js_code"]
        self.assertEqual(js_code, js_code.strip())

    def test_description_content(self):
        """Test that description contains relevant information"""
        prompt = "create something amazing"
        result = generate_website_overlay_js(prompt)
        
        description = result["description"]
        self.assertIn("Generated JavaScript code for:", description)
        self.assertIn("create something amazing", description)

    def test_very_long_description_truncation(self):
        """Test description truncation for very long prompts"""
        long_prompt = "x" * 200
        result = generate_website_overlay_js(long_prompt)
        
        description = result["description"]
        # Should be truncated to 100 characters plus "..."
        self.assertTrue(len(description) < len(f"Generated JavaScript code for: {long_prompt}..."))
        self.assertIn("x" * 100 + "...", description)


class TestRootAgent(unittest.TestCase):
    """Test cases for the root agent configuration"""

    def test_agent_initialization(self):
        """Test that the root agent is properly initialized"""
        self.assertEqual(root_agent.name, "overlay_agent_dir")
        self.assertEqual(root_agent.model, "gemini-1.5-flash")
        self.assertIsInstance(root_agent.description, str)
        self.assertIsInstance(root_agent.instruction, str)
        self.assertEqual(len(root_agent.tools), 1)

    def test_agent_description(self):
        """Test agent description content"""
        description = root_agent.description
        self.assertIn("JavaScript", description)
        self.assertIn("overlay", description)
        self.assertIn("Apple-style", description)

    def test_agent_instruction(self):
        """Test agent instruction content"""
        instruction = root_agent.instruction
        self.assertIn("generate_website_overlay_js", instruction)
        self.assertIn("MUST use", instruction)
        self.assertIn("raw JavaScript code", instruction)

    def test_agent_tool_configuration(self):
        """Test that the agent has the correct tool configured"""
        self.assertEqual(len(root_agent.tools), 1)
        tool = root_agent.tools[0]
        self.assertEqual(tool.function, generate_website_overlay_js)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def test_whitespace_only_prompt(self):
        """Test handling of whitespace-only prompt"""
        result = generate_website_overlay_js("   ")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("Generic website modification", result["js_code"])

    def test_numeric_prompt(self):
        """Test handling of numeric prompt"""
        result = generate_website_overlay_js("12345")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("12345", result["js_code"])

    def test_boolean_prompt_conversion(self):
        """Test handling when prompt is converted from boolean"""
        # This tests the str() conversion in the f-string
        with patch('builtins.len', return_value=10):  # Mock to avoid actual boolean
            result = generate_website_overlay_js("true")
            self.assertEqual(result["status"], "success")

    def test_prompt_with_quotes(self):
        """Test handling of prompts containing quotes"""
        prompt = 'create "fancy" overlay with \'single\' quotes'
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("create an overlay", result["js_code"].lower())

    def test_prompt_with_newlines(self):
        """Test handling of prompts with newline characters"""
        prompt = "create\noverlay\nwith\nnewlines"
        result = generate_website_overlay_js(prompt)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("glass-overlay", result["js_code"])

    def test_mixed_case_keywords(self):
        """Test mixed case keyword detection"""
        test_cases = [
            ("BaCkGrOuNd ReD", "red"),
            ("OvErLaY", "glass-overlay"),
            ("NoTe", "📝 Note")
        ]
        
        for prompt, expected in test_cases:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn(expected, result["js_code"])


class TestJavaScriptCodeQuality(unittest.TestCase):
    """Test the quality and completeness of generated JavaScript code"""

    def test_overlay_removal_functionality(self):
        """Test that overlay includes proper removal functionality"""
        result = generate_website_overlay_js("create overlay")
        js_code = result["js_code"]
        
        # Should include code to remove existing overlay
        self.assertIn("getElementById('glass-overlay')", js_code)
        self.assertIn("existingOverlay.remove()", js_code)
        
        # Should include close button functionality
        self.assertIn("this.parentElement.remove()", js_code)

    def test_note_animation_styles(self):
        """Test that note overlay includes proper animation"""
        result = generate_website_overlay_js("show note")
        js_code = result["js_code"]
        
        self.assertIn("@keyframes slideIn", js_code)
        self.assertIn("animation: slideIn", js_code)
        self.assertIn("transform: translateX", js_code)

    def test_accessibility_considerations(self):
        """Test that generated code includes accessibility considerations"""
        result = generate_website_overlay_js("create overlay")
        js_code = result["js_code"]
        
        # Should include proper font family
        self.assertIn("-apple-system, BlinkMacSystemFont", js_code)
        
        # Should include proper color contrast
        self.assertIn("color: #333", js_code)

    def test_responsive_design_elements(self):
        """Test that overlays include responsive design considerations"""
        result = generate_website_overlay_js("create overlay")
        js_code = result["js_code"]
        
        # Should use relative units and flexible sizing
        self.assertIn("max-width:", js_code)
        self.assertIn("transform: translate(-50%, -50%)", js_code)

    def test_cross_browser_compatibility(self):
        """Test that generated code uses cross-browser compatible features"""
        result = generate_website_overlay_js("create overlay")
        js_code = result["js_code"]
        
        # Should use standard DOM methods
        self.assertIn("document.createElement", js_code)
        self.assertIn("document.body.appendChild", js_code)
        self.assertIn("document.getElementById", js_code)


class TestPromptKeywordPrecedence(unittest.TestCase):
    """Test keyword precedence and priority in prompt processing"""

    def test_background_red_first_priority(self):
        """Test that red background takes absolute first priority"""
        prompts_with_red = [
            "create overlay with red background and note",
            "show message with red background",
            "red background overlay note"
        ]
        
        for prompt in prompts_with_red:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("document.body.style.backgroundColor = 'red'", result["js_code"])

    def test_background_colors_second_priority(self):
        """Test that other background colors take second priority over overlays and notes"""
        test_cases = [
            ("create overlay with blue background", "blue"),
            ("show note with green background", "green"),
            ("yellow background overlay", "yellow"),
            ("purple background note", "purple")
        ]
        
        for prompt, color in test_cases:
            with self.subTest(prompt=prompt, color=color):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn(f"document.body.style.backgroundColor = '{color}'", result["js_code"])

    def test_overlay_third_priority(self):
        """Test that overlay takes third priority when no background is specified"""
        prompts = [
            "create overlay note",
            "overlay message",
            "note overlay"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("glass-overlay", result["js_code"])
                self.assertNotIn("background", result["js_code"].lower().split("//")[0])  # No background in main code

    def test_note_fourth_priority(self):
        """Test that note/message takes fourth priority"""
        prompts = [
            "show note",
            "display message",
            "create note message"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("📝 Note", result["js_code"])
                self.assertNotIn("glass-overlay", result["js_code"])

    def test_generic_fallback(self):
        """Test that unrecognized prompts fall back to generic modification"""
        prompts = [
            "do something random",
            "modify the website",
            "change things around",
            "make it better"
        ]
        
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = generate_website_overlay_js(prompt)
                self.assertEqual(result["status"], "success")
                self.assertIn("Generic website modification", result["js_code"])


class TestFunctionToolIntegration(unittest.TestCase):
    """Test integration with the FunctionTool and Agent framework"""

    def test_function_tool_import(self):
        """Test that FunctionTool is properly imported and used"""
        from google.adk.tools import FunctionTool
        
        # Verify the tool is a FunctionTool instance
        tool = root_agent.tools[0]
        self.assertIsInstance(tool, FunctionTool)

    def test_agent_import(self):
        """Test that Agent is properly imported and used"""
        from google.adk.agents import Agent
        
        # Verify the root_agent is an Agent instance
        self.assertIsInstance(root_agent, Agent)

    def test_function_signature_matches_tool(self):
        """Test that the function signature matches what's expected by the tool"""
        import inspect
        
        # Get the function signature
        sig = inspect.signature(generate_website_overlay_js)
        params = list(sig.parameters.keys())
        
        # Should have exactly one parameter: prompt
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], "prompt")
        
        # Parameter should have string type annotation
        prompt_param = sig.parameters["prompt"]
        self.assertEqual(prompt_param.annotation, str)

    def test_return_type_annotation(self):
        """Test that function has proper return type annotation"""
        import inspect
        
        sig = inspect.signature(generate_website_overlay_js)
        self.assertEqual(sig.return_annotation, dict)


class TestDocstrings(unittest.TestCase):
    """Test function and module docstrings"""

    def test_function_docstring_exists(self):
        """Test that the main function has a comprehensive docstring"""
        docstring = generate_website_overlay_js.__doc__
        self.assertIsNotNone(docstring)
        self.assertIn("Generate JavaScript code", docstring)
        self.assertIn("Args:", docstring)
        self.assertIn("Returns:", docstring)

    def test_docstring_contains_usage_examples(self):
        """Test that docstring explains when to use the function"""
        docstring = generate_website_overlay_js.__doc__
        self.assertIn("overlay", docstring)
        self.assertIn("modify a website", docstring)
        self.assertIn("background", docstring)

    def test_docstring_return_format(self):
        """Test that docstring explains return format"""
        docstring = generate_website_overlay_js.__doc__
        self.assertIn("status", docstring)
        self.assertIn("js_code", docstring)
        self.assertIn("error_message", docstring)


if __name__ == '__main__':
    # Create a test suite with all test cases
    unittest.main(verbosity=2)