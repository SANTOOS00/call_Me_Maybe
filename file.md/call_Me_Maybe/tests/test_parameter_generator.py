from src.generator.module.parameter_generator import ParameterGenerator
from src.parser.function_definition import FunctionDefn
from src.llm_manager.manager import ManagerLLM
import unittest

class TestParameterGenerator(unittest.TestCase):

    def setUp(self):
        self.model = ManagerLLM()
        self.parameter_generator = ParameterGenerator(self.model)

    def test_generate_string_parameter(self):
        function_def = FunctionDefn(name="test_function", description="A test function", parameters={"arg1": "string"})
        prompt = "Generate a string parameter"
        result = self.parameter_generator.generate(function_def, prompt)
        self.assertIn("arg1", result)
        self.assertIsInstance(result["arg1"], str)

    def test_generate_number_parameter(self):
        function_def = FunctionDefn(name="test_function", description="A test function", parameters={"arg2": "number"})
        prompt = "Generate a number parameter"
        result = self.parameter_generator.generate(function_def, prompt)
        self.assertIn("arg2", result)
        self.assertIsInstance(result["arg2"], float)

    def test_generate_integer_parameter(self):
        function_def = FunctionDefn(name="test_function", description="A test function", parameters={"arg3": "integer"})
        prompt = "Generate an integer parameter"
        result = self.parameter_generator.generate(function_def, prompt)
        self.assertIn("arg3", result)
        self.assertIsInstance(result["arg3"], int)

    def test_generate_boolean_parameter(self):
        function_def = FunctionDefn(name="test_function", description="A test function", parameters={"arg4": "boolean"})
        prompt = "Generate a boolean parameter"
        result = self.parameter_generator.generate(function_def, prompt)
        self.assertIn("arg4", result)
        self.assertIsInstance(result["arg4"], bool)

if __name__ == '__main__':
    unittest.main()