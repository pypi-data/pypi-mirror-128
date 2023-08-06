from unittest import TestCase
from presentable_exception.presentable_exception import ExceptionScenario, ScenarioDefinitionParser

class TestScenarioDefintionParserWithList(TestCase):

    def setUp(self):
        self.parser = ScenarioDefinitionParser()

    def test_empty_list(self):
        res = self.parser.parse_scenarios('package', [])
        self.assertEqual([], res)

    def test_list_with_one_tuple(self):
        res = self.parser.parse_scenarios('package', [('the-key', 'the description')])
        self.assertEqual(1, len(res))
        self.assertIsInstance(res[0], ExceptionScenario)
        self.assertEqual('package', res[0].package)
        self.assertEqual('the-key', res[0].key)
        self.assertEqual('the description', res[0].description)
        self.assertEqual('server', res[0].responsible)

    def test_no_description_given(self):
        res = self.parser.parse_scenarios('package', [('the-key',)])
        self.assertEqual(1, len(res))
        self.assertIsInstance(res[0], ExceptionScenario)
        self.assertEqual('package', res[0].package)
        self.assertEqual('the-key', res[0].key)
        self.assertFalse(res[0].description)

    def test_empty_tuple(self):
        res = self.parser.parse_scenarios('package', [()])
        self.assertEqual(0, len(res))

    def test_empty_key(self):
        res = self.parser.parse_scenarios('package', [('', 'd')])
        self.assertEqual(0, len(res))

    def test_lists_work_too(self):
        # note the [] arount 'the-key', 'the description'
        res = self.parser.parse_scenarios('package', [['the-key', 'the description']])
        self.assertEqual(1, len(res))
        self.assertIsInstance(res[0], ExceptionScenario)
        self.assertEqual('package', res[0].package)
        self.assertEqual('the-key', res[0].key)
        self.assertEqual('the description', res[0].description)

    def test_invalid_input(self):
        for invalid_input in [set, 1, 1.1, 'abc']:
            res = self.parser.parse_scenarios('package', invalid_input)
            self.assertEqual([], res)


class TestScenarioDefintionParserWithMap(TestCase):

    def setUp(self):
        self.parser = ScenarioDefinitionParser()

    def test_empty_map(self):
        res = self.parser.parse_scenarios('package', {})
        self.assertEqual([], res)

    def test_server_fault(self):
        res = self.parser.parse_scenarios('package', {'server': [('the-key', 'the description')]})
        self.assertEqual(1, len(res))
        self.assertIsInstance(res[0], ExceptionScenario)
        self.assertEqual('package', res[0].package)
        self.assertEqual('the-key', res[0].key)
        self.assertEqual('the description', res[0].description)
        self.assertEqual('server', res[0].responsible)

    def test_client_fault(self):
        res = self.parser.parse_scenarios('package', {'client': [('the-key', 'the description')]})
        self.assertEqual(1, len(res))
        self.assertIsInstance(res[0], ExceptionScenario)
        self.assertEqual('package', res[0].package)
        self.assertEqual('the-key', res[0].key)
        self.assertEqual('the description', res[0].description)
        self.assertEqual('client', res[0].responsible)


    # def test_list_with_one_tuple(self):
    #     res = self.parser.parse_scenarios('package', [('the-key', 'the description')])