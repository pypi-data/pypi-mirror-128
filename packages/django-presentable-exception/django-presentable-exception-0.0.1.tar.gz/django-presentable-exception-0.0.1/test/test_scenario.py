from unittest import TestCase

from presentable_exception.presentable_exception import ExceptionScenario

def build_scenario(package='package', key='key', description='description', responsible='server'):
    return ExceptionScenario(
        package=package,
        key=key,
        description=description,
        responsible=responsible
    )

class TestExceptionScenarioMessage(TestCase):

    def test_with_normal_description(self):
        scenario = build_scenario(description='A little description')
        self.assertEqual('A little description', scenario.message())

    def test_without_description(self):
        scenario = build_scenario(key='key', package='package', description=' ')
        self.assertEqual('package.key', scenario.message())

    def test_with_parameters_in_description(self):
        scenario = build_scenario(description='A little description. {name} is the name')
        data = {'name': 'Tom'}
        self.assertEqual('A little description. Tom is the name', scenario.message(data=data))

    def test_with_too_much_parameters(self):
        scenario = build_scenario(description='A little description. {name} is the name')
        data = {'name': 'Tom', 'unused': 'parameter'}
        self.assertEqual('A little description. Tom is the name', scenario.message(data))

    def test_with_too_little_parameters(self):
        scenario = build_scenario(description='A little description. {name} is the name')
        data = {}
        self.assertEqual('A little description. {name} is the name', scenario.message(data))

    def test_parameters_but_no_description(self):
        scenario = build_scenario(description='')
        data = {'name': 'Tom', 'unused': 'parameter'}
        self.assertEqual('package.key', scenario.message(data))


class TestExeptionScenarioLogEntry(TestCase):

    def test_everything_is_given(self):
        
        scenario = build_scenario(
            package='package', 
            key='key', 
            description='A little {name} description', 
            responsible='client')
        self.assertEqual(scenario.log_entry(data={'name': 'Tom'}), {
            'error': 'package.key',
            'responsible': 'client',
            'message': 'A little Tom description',
            'description': 'A little {name} description',
            'data': {'name': 'Tom'}
        })
