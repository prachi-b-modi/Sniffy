#!/usr/bin/env python3
"""
Comprehensive unit tests for simple_agent_dir/agent.py

Testing framework: unittest (Python standard library)
Focus: Agent initialization, configuration, and interface validation based on the provided source code
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os
import importlib.util

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSimpleAgentDirAgent(unittest.TestCase):
    """Test suite for the simple test agent without custom tools."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.expected_name = "simple_test_agent"
        self.expected_model = "gemini-2.0-flash"
        self.expected_description = "A simple test agent without custom tools"
        self.expected_instruction = "You are a helpful assistant. Just respond to user messages normally."

        # Source code from the provided file
        self.test_file_content = '''#!/usr/bin/env python3
"""
Simple test agent without custom tools
"""

from google.adk.agents import Agent

# Simple agent without tools
root_agent = Agent(
    name="simple_test_agent",
    model="gemini-2.0-flash",
    description="A simple test agent without custom tools",
    instruction="You are a helpful assistant. Just respond to user messages normally."
)'''

        # Clear any previously imported modules to ensure clean tests
        modules_to_clear = [mod for mod in sys.modules if 'simple_agent_dir' in mod or 'agent' in mod]
        for mod in modules_to_clear:
            if mod in sys.modules:
                del sys.modules[mod]

    def tearDown(self):
        """Clean up after each test method."""
        # Clean up imported modules
        modules_to_clear = [mod for mod in sys.modules if 'simple_agent_dir' in mod or 'agent' in mod]
        for mod in modules_to_clear:
            if mod in sys.modules:
                del sys.modules[mod]

    @patch('google.adk.agents.Agent')
    def test_agent_initialization_with_correct_parameters(self, mock_agent_class):
        """Test that the agent is initialized with the correct parameters."""
        # Mock the Agent class to avoid import issues
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        # Verify Agent was called with correct parameters
        mock_agent_class.assert_called_once_with(
            name=self.expected_name,
            model=self.expected_model,
            description=self.expected_description,
            instruction=self.expected_instruction
        )

    @patch('google.adk.agents.Agent')
    def test_agent_name_is_string_and_not_empty(self, mock_agent_class):
        """Test that the agent name is a non-empty string."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        agent_name = kwargs.get('name')

        self.assertIsInstance(agent_name, str, "Agent name should be a string")
        self.assertTrue(len(agent_name) > 0, "Agent name should not be empty")
        self.assertFalse(agent_name.isspace(), "Agent name should not be just whitespace")

    @patch('google.adk.agents.Agent')
    def test_agent_model_is_valid_gemini_model(self, mock_agent_class):
        """Test that the agent uses a valid Gemini model."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        model = kwargs.get('model')

        self.assertIsInstance(model, str, "Model should be a string")
        self.assertTrue(model.startswith('gemini'), "Model should be a Gemini model")
        self.assertIn('flash', model, "Model should be a Flash variant")
        self.assertEqual(model, "gemini-2.0-flash", "Model should be exactly gemini-2.0-flash")

    @patch('google.adk.agents.Agent')
    def test_agent_description_is_meaningful(self, mock_agent_class):
        """Test that the agent has a meaningful description."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        description = kwargs.get('description')

        self.assertIsInstance(description, str, "Description should be a string")
        self.assertTrue(len(description) > 10, "Description should be meaningful length")
        self.assertIn('test', description.lower(), "Description should mention it's for testing")
        self.assertIn('agent', description.lower(), "Description should mention it's an agent")
        self.assertIn('simple', description.lower(), "Description should mention it's simple")

    @patch('google.adk.agents.Agent')
    def test_agent_instruction_is_comprehensive(self, mock_agent_class):
        """Test that the agent has comprehensive instructions."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        instruction = kwargs.get('instruction')

        self.assertIsInstance(instruction, str, "Instruction should be a string")
        self.assertTrue(len(instruction) > 20, "Instruction should be comprehensive")
        self.assertIn('helpful', instruction.lower(), "Instruction should mention being helpful")
        self.assertIn('assistant', instruction.lower(), "Instruction should mention assistant role")
        self.assertIn('respond', instruction.lower(), "Instruction should mention responding")

    @patch('google.adk.agents.Agent')
    def test_agent_has_no_custom_tools(self, mock_agent_class):
        """Test that the agent is created without custom tools."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args

        # Verify no tools-related parameters are passed
        self.assertNotIn('tools', kwargs, "Agent should not have custom tools")
        self.assertNotIn('custom_tools', kwargs, "Agent should not have custom tools")
        self.assertNotIn('functions', kwargs, "Agent should not have custom functions")

    @patch('google.adk.agents.Agent')
    def test_module_creates_root_agent_variable(self, mock_agent_class):
        """Test that the module creates a root_agent variable."""
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance

        # Execute the test file content in a namespace
        namespace = {}
        exec(self.test_file_content, namespace)

        self.assertIn('root_agent', namespace, "Module should have root_agent variable")
        self.assertEqual(namespace['root_agent'], mock_agent_instance,
                        "root_agent should be the created Agent instance")

    @patch('google.adk.agents.Agent')
    def test_agent_parameters_are_not_none(self, mock_agent_class):
        """Test that all agent parameters are not None."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args

        for param_name, param_value in kwargs.items():
            self.assertIsNotNone(param_value, f"Parameter {param_name} should not be None")

    @patch('google.adk.agents.Agent')
    def test_agent_name_follows_naming_convention(self, mock_agent_class):
        """Test that the agent name follows expected naming conventions."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        agent_name = kwargs.get('name')

        # Should be lowercase with underscores
        self.assertEqual(agent_name, agent_name.lower(),
                        "Agent name should be lowercase")
        self.assertNotIn(' ', agent_name,
                        "Agent name should not contain spaces")
        self.assertNotIn('-', agent_name,
                        "Agent name should use underscores, not hyphens")
        self.assertTrue(agent_name.replace('_', '').isalnum(),
                       "Agent name should only contain alphanumeric characters and underscores")

    @patch('google.adk.agents.Agent', side_effect=Exception("Agent creation failed"))
    def test_agent_creation_failure_handling(self, mock_agent_class):
        """Test behavior when agent creation fails."""
        with self.assertRaises(Exception) as context:
            namespace = {}
            exec(self.test_file_content, namespace)

        self.assertIn("Agent creation failed", str(context.exception))

    def test_module_has_proper_docstring(self):
        """Test that the module has a proper docstring."""
        # Check if the content has a docstring
        lines = self.test_file_content.split('\n')
        docstring_lines = []
        in_docstring = False

        for line in lines:
            if '"""' in line and not in_docstring:
                in_docstring = True
                docstring_lines.append(line)
            elif '"""' in line and in_docstring:
                docstring_lines.append(line)
                break
            elif in_docstring:
                docstring_lines.append(line)

        docstring = '\n'.join(docstring_lines)
        self.assertTrue(len(docstring) > 0, "Module should have a docstring")
        self.assertIn('test', docstring.lower(),
                     "Docstring should mention this is for testing")

    def test_module_is_executable(self):
        """Test that the module has executable shebang."""
        first_line = self.test_file_content.split('\n')[0]

        self.assertTrue(first_line.startswith('#!'),
                       "Module should have executable shebang")
        self.assertIn('python', first_line.lower(),
                     "Shebang should reference Python")

    @patch('google.adk.agents.Agent')
    def test_agent_string_parameters_are_not_empty_after_strip(self, mock_agent_class):
        """Test that string parameters are not empty after stripping whitespace."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args

        string_params = ['name', 'model', 'description', 'instruction']
        for param_name in string_params:
            if param_name in kwargs:
                param_value = kwargs[param_name]
                self.assertIsInstance(param_value, str,
                                    f"{param_name} should be a string")
                self.assertTrue(len(param_value.strip()) > 0,
                              f"{param_name} should not be empty after stripping")

    @patch('google.adk.agents.Agent')
    def test_agent_description_and_instruction_are_different(self, mock_agent_class):
        """Test that description and instruction serve different purposes."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        description = kwargs.get('description', '')
        instruction = kwargs.get('instruction', '')

        self.assertNotEqual(description, instruction,
                           "Description and instruction should be different")
        self.assertTrue(len(description) > 0 and len(instruction) > 0,
                       "Both description and instruction should be provided")

    def test_agent_configuration_values_match_expected(self):
        """Test that the agent configuration matches the expected values exactly."""
        # Check that the expected values are present in the file content
        self.assertIn(self.expected_name, self.test_file_content,
                     "Expected agent name should be in file")
        self.assertIn(self.expected_model, self.test_file_content,
                     "Expected model should be in file")
        self.assertIn(self.expected_description, self.test_file_content,
                     "Expected description should be in file")
        self.assertIn(self.expected_instruction, self.test_file_content,
                     "Expected instruction should be in file")

    def test_file_has_google_adk_import(self):
        """Test that the file imports from google.adk.agents."""
        self.assertIn('from google.adk.agents import Agent', self.test_file_content,
                     "File should import Agent from google.adk.agents")

    @patch('google.adk.agents.Agent')
    def test_agent_only_has_required_parameters(self, mock_agent_class):
        """Test that the agent is created with only the expected parameters."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args
        expected_params = {'name', 'model', 'description', 'instruction'}
        actual_params = set(kwargs.keys())

        self.assertEqual(expected_params, actual_params,
                        "Agent should only have the expected parameters")

    @patch('google.adk.agents.Agent')
    def test_agent_parameter_types_are_correct(self, mock_agent_class):
        """Test that all agent parameters are strings."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        args, kwargs = mock_agent_class.call_args

        for param_name, param_value in kwargs.items():
            self.assertIsInstance(param_value, str,
                                f"Parameter {param_name} should be a string")

    def test_file_structure_and_syntax(self):
        """Test that the file has correct Python structure and syntax."""
        # Test that the content can be compiled
        try:
            compile(self.test_file_content, '<string>', 'exec')
            self.assertTrue(True, "File has valid Python syntax")
        except SyntaxError as e:
            self.fail(f"File has invalid Python syntax: {e}")

    def test_agent_variable_naming(self):
        """Test that the agent variable is named correctly."""
        self.assertIn('root_agent = Agent(', self.test_file_content,
                     "Agent should be assigned to variable named 'root_agent'")

    @patch('google.adk.agents.Agent')
    def test_agent_creation_is_immediate_not_lazy(self, mock_agent_class):
        """Test that the agent is created immediately when module is executed."""
        mock_agent_class.return_value = Mock()

        # Execute the test file content
        namespace = {}
        exec(self.test_file_content, namespace)

        # Agent should be called immediately, not lazily
        self.assertTrue(mock_agent_class.called, "Agent should be created immediately")
        self.assertEqual(mock_agent_class.call_count, 1,
                        "Agent should be created exactly once")

    def test_actual_file_exists_and_can_be_read(self):
        """Test that the actual agent file exists and is readable."""
        file_path = 'simple_agent_dir/agent.py'
        self.assertTrue(os.path.exists(file_path), f"File {file_path} should exist")

        try:
            with open(file_path, 'r') as f:
                content = f.read()
            self.assertTrue(len(content.strip()) > 0, "File should not be empty")
        except IOError as e:
            self.fail(f"Could not read file {file_path}: {e}")

    @patch('google.adk.agents.Agent')
    def test_actual_file_imports_correctly(self, mock_agent_class):
        """Test that the actual file can be imported and executed."""
        mock_agent_class.return_value = Mock()

        try:
            # Try to import the actual module
            spec = importlib.util.spec_from_file_location("simple_agent_dir.agent", "simple_agent_dir/agent.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules['simple_agent_dir.agent'] = module
                spec.loader.exec_module(module)

                # Verify the agent was created
                self.assertTrue(mock_agent_class.called, "Agent should be created when module is imported")
                self.assertTrue(hasattr(module, 'root_agent'), "Module should have root_agent attribute")
        except FileNotFoundError:
            self.skipTest("Actual agent file not found - testing with provided source code only")
        except Exception as e:
            self.fail(f"Failed to import actual agent file: {e}")

class TestSimpleAgentDirAgentIntegration(unittest.TestCase):
    """Integration tests for the simple agent module."""

    def setUp(self):
        """Set up test fixtures."""
        # Source code from the provided file
        self.test_file_content = '''#!/usr/bin/env python3
"""
Simple test agent without custom tools
"""

from google.adk.agents import Agent

# Simple agent without tools
root_agent = Agent(
    name="simple_test_agent",
    model="gemini-2.0-flash",
    description="A simple test agent without custom tools",
    instruction="You are a helpful assistant. Just respond to user messages normally."
)'''

    @patch('google.adk.agents.Agent')
    def test_module_can_be_executed_without_errors(self, mock_agent_class):
        """Test that the module can be executed without raising exceptions."""
        mock_agent_class.return_value = Mock()

        try:
            namespace = {}
            exec(self.test_file_content, namespace)
            self.assertTrue(True, "Module executed successfully")
        except ImportError as e:
            self.fail(f"Module execution failed with import error: {e}")
        except Exception as e:
            self.fail(f"Unexpected error during module execution: {e}")

    @patch('google.adk.agents.Agent')
    def test_agent_attributes_are_accessible(self, mock_agent_class):
        """Test that agent attributes can be accessed after creation."""
        # Setup mock agent with attributes
        mock_agent_instance = Mock()
        mock_agent_instance.name = "simple_test_agent"
        mock_agent_instance.model = "gemini-2.0-flash"
        mock_agent_class.return_value = mock_agent_instance

        # Execute the test file content in a namespace
        namespace = {}
        exec(self.test_file_content, namespace)

        # Test that we can access agent attributes
        self.assertEqual(namespace['root_agent'].name, "simple_test_agent")
        self.assertEqual(namespace['root_agent'].model, "gemini-2.0-flash")

    @patch('google.adk.agents.Agent')
    def test_multiple_executions_create_separate_agents(self, mock_agent_class):
        """Test that multiple executions create separate agent instances."""
        mock_agent_class.return_value = Mock()

        # Execute the content multiple times
        namespace1 = {}
        exec(self.test_file_content, namespace1)
        namespace2 = {}
        exec(self.test_file_content, namespace2)

        # Should have been called twice
        self.assertEqual(mock_agent_class.call_count, 2,
                        "Each execution should create a new agent")

    @patch('google.adk.agents.Agent')
    def test_import_from_actual_directory_structure(self, mock_agent_class):
        """Test importing from the actual simple_agent_dir directory."""
        mock_agent_class.return_value = Mock()

        try:
            # Add the simple_agent_dir to Python path
            simple_agent_dir_path = os.path.join(os.getcwd(), 'simple_agent_dir')
            if simple_agent_dir_path not in sys.path:
                sys.path.insert(0, simple_agent_dir_path)

            # Try to import the agent module
            import importlib
            if 'simple_agent_dir.agent' in sys.modules:
                del sys.modules['simple_agent_dir.agent']

            # Import the module
            spec = importlib.util.spec_from_file_location("agent", "simple_agent_dir/agent.py")
            if spec and spec.loader:
                agent_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(agent_module)

                # Verify agent was created
                self.assertTrue(mock_agent_class.called, "Agent should be created on import")

        except (ImportError, FileNotFoundError):
            self.skipTest("Could not import from simple_agent_dir - directory structure may differ")
        except Exception as e:
            self.fail(f"Unexpected error during directory import test: {e}")

class TestSimpleAgentFileValidation(unittest.TestCase):
    """Tests for validating the file content matches expected patterns."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file_content = '''#!/usr/bin/env python3
"""
Simple test agent without custom tools
"""

from google.adk.agents import Agent

# Simple agent without tools
root_agent = Agent(
    name="simple_test_agent",
    model="gemini-2.0-flash",
    description="A simple test agent without custom tools",
    instruction="You are a helpful assistant. Just respond to user messages normally."
)'''

    def test_file_contains_all_required_elements(self):
        """Test that the file contains all required code elements."""
        required_elements = [
            '#!/usr/bin/env python3',
            'from google.adk.agents import Agent',
            'root_agent = Agent(',
            'name="simple_test_agent"',
            'model="gemini-2.0-flash"',
            'description="A simple test agent without custom tools"',
            'instruction="You are a helpful assistant. Just respond to user messages normally."'
        ]

        for element in required_elements:
            self.assertIn(element, self.test_file_content,
                         f"File should contain: {element}")

    def test_file_has_proper_formatting(self):
        """Test that the file has proper Python formatting."""
        lines = self.test_file_content.split('\n')

        # Check that imports are at the top (after shebang and docstring)
        import_line_found = False
        for i, line in enumerate(lines):
            if line.startswith('from google.adk.agents'):
                import_line_found = True
                # Should not be the first line (shebang should be first)
                self.assertGreater(i, 0, "Import should not be the first line")
                break

        self.assertTrue(import_line_found, "Should contain the import statement")

    def test_agent_parameters_are_properly_quoted(self):
        """Test that all string parameters use double quotes consistently."""
        # Extract parameter lines
        param_lines = []
        in_agent_call = False

        for line in self.test_file_content.split('\n'):
            if 'root_agent = Agent(' in line:
                in_agent_call = True
            elif in_agent_call and ')' in line:
                break
            elif in_agent_call and '=' in line:
                param_lines.append(line.strip())

        # Check that string values use double quotes
        for line in param_lines:
            if '=' in line:
                value_part = line.split('=', 1)[1].strip().rstrip(',')
                if value_part.startswith('"'):
                    self.assertTrue(value_part.endswith('"'),
                                   f"String value should end with double quote: {line}")

    def test_no_trailing_whitespace(self):
        """Test that lines don't have trailing whitespace."""
        lines = self.test_file_content.split('\n')
        for i, line in enumerate(lines):
            if line.endswith(' ') or line.endswith('\t'):
                self.fail(f"Line {i+1} has trailing whitespace: '{line}'")

    def test_consistent_indentation(self):
        """Test that the file uses consistent indentation."""
        lines = self.test_file_content.split('\n')
        indented_lines = [line for line in lines if line.startswith(' ') and line.strip()]

        for line in indented_lines:
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip(' '))
            # Should be multiple of 4 (PEP 8 recommendation)
            self.assertEqual(leading_spaces % 4, 0,
                           f"Line should use 4-space indentation: '{line}'")

if __name__ == '__main__':
    # Configure test runner for verbose output
    unittest.main(verbosity=2, buffer=True)