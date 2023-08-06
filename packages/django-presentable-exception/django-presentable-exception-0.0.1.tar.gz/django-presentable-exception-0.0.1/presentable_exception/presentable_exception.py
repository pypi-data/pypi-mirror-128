from unittest.case import TestCase
from django.conf import settings
from find_class import find_class
from collections.abc import Iterable
from safe import safe


class PresentableException(Exception):
    """
    A kind of exception, that different components can raise and a special
    API view captures and converts to a proper response, such that the client
    can show it to the user directly. They are not intended to be caught.
    """

    not_found_message = 'Internal Error: Error not found'

    @staticmethod
    def of(package, key, data=None, scenario_loader=None):
        data = data or {}
        scenario_loader = scenario_loader or DefaultScenarioLoader.instance()
        scenario = scenario_loader.to_scenario(package, key)

        if not scenario:
            return PresentableExceptionNotFound(package, key, data)

        if scenario.responsible == 'client':
            return PresentableClientException(scenario, data)

        return PresentableServerException(scenario, data)

    @staticmethod
    def from_scenario(scenario, data):
        pass
    
    def __init__(self, scenario, data=None):
        self.scenario = scenario
        self.data = data or {}
    
    @property
    def message(self):
        return self.scenario.message(self.data)

    @property
    def log_entry(self):
        return self.scenario.log_entry(self.data)

    def __str__(self):
        return self.key

    def __repr__(self):
        return self.key
    
class PresentableServerException(PresentableException):
    pass

class PresentableClientException(PresentableException):
    pass

class PresentableExceptionNotFound(PresentableServerException):
    
    def __init__(self, package, key, data=None):
        self.package = package
        self.key = key
        self.data = data or {}

    property
    def message(self):
        return 'Internal Error: Error not found'

    @property
    def log_entry(self):
        return {
            'package': 'presentable_exception',
            'key': 'error_not_found',
            'message': 'Error not found',
            'data': {
                'package': self.package,
                'key': self.key, 
                'data': self.data
            }
        }


class Locator:
    """
    This class locates the presentable_exceptions.py in the given packages
    and loads them into a map with {"package": [presentable_excpetions]}
    """

    def __init__(self, prefix_blacklist=[], blacklist=[], resolver=find_class):
        self.prefix_blacklist = prefix_blacklist
        self.blacklist = blacklist
        self.resolver = resolver

    def locate(self, packages):
        if isinstance(packages, str):
            packages = [packages]
        if not isinstance(packages, Iterable):
            return {}

        res = {}
        for package in packages:
            package, entries = self._locate_one(package)
            if package and entries:
                res[package] = entries
        return res

    def _locate_one(self, package):
        if self._is_on_blacklist(package):
            return None, []
        candidate = package + '.presentable_exceptions.presentable_exceptions'
        candidate = self.resolver(candidate)
        return package, self._load_candidate(candidate)

    def _load_candidate(self, candidate):
        if not candidate:
            return []
        return candidate

    def _is_on_blacklist(self, package_name):
        if package_name in self.blacklist:
            return True
        for entry in self.prefix_blacklist:
            if package_name.startswith(entry):
                return True
        return False

class ScenarioDefinitionParser:

    def __int__(self):
        pass

    def parse_scenarios(self, package, scenario_defs):
        if not isinstance(scenario_defs, Iterable):
            return []

        if isinstance(scenario_defs, str):
            return []

        # if not speratet, everything is our fault
        if not isinstance(scenario_defs, dict):
            return self._parse_scenarios_list(package, scenario_defs, 'server')

        # it is a dict
        res = []
        res += self._parse_scenarios_list(package, scenario_defs.get('client', []), 'client')
        res += self._parse_scenarios_list(package, scenario_defs.get('server', []), 'server')
        return res

    def _parse_scenarios_list(self, package, scenario_defs, responsible):
        res = []
        for scenario_def in scenario_defs:
            key = safe(lambda: scenario_def[0])
            if not key:
                continue
            res += [ExceptionScenario(
                package=package,
                key=key, 
                description=safe(lambda: scenario_def[1]),
                responsible=responsible
            )]

        return res


class DefaultScenarioLoader:
    """
    Locates sources of ExceptionScenarios, and load them. After that, the 
    PrentableException can query them via key
    """

    prefix_blacklist=['django.', 'rest_framework.']
    blacklist=['rest_framework']

    _instance = None
    @staticmethod
    def instance():
        if DefaultScenarioLoader._instance:
            return DefaultScenarioLoader._instance
        instance = DefaultScenarioLoader(
            resolver=find_class
        )
        instance._load(settings.INSTALLED_APPS)
        DefaultScenarioLoader._instance = instance
        return instance

    def __init__(self, resolver):
        self.resolver = resolver
        self.locator = Locator(
            prefix_blacklist=self.prefix_blacklist,
            blacklist=self.blacklist,
            resolver=self.resolver
        )
        self.parser = ScenarioDefinitionParser()
        self.scenario_lut = {}

    def to_scenario(self, package, key):
        return self.scenario_lut.get(package + '.' + key)

    ### 

    def _load(self, packages):
        res = self.locator.locate(packages)
        scenarios = self._parse_scenarios(res)
        self._register_scenarios(scenarios)

    def _parse_scenarios(self, collected_raw_material):
        res = []
        for package in collected_raw_material.keys():
            scenarios = self.parser.parse_scenarios(package, collected_raw_material[package])
            res += scenarios
        return res

    def _register_scenarios(self, scenarios):
        for scenario in scenarios:
            self.scenario_lut[scenario.package + '.' + scenario.key] = scenario



class ExceptionScenario:
    """
    The programmers can create scenarios in different formats. They 
    are parsed and converted to ExceptionScenarios and loaded by the 
    Scenario Loder and used by the PresentableException.
    """
    
    def __init__(self, package, key, description, responsible):
        self.package = package
        self.key = key
        self.description = description.strip() if description else ''
        self.responsible = responsible

    def message(self, data=None):
        description = self.description
        if not description:
            return f'{self.package}.{self.key}'
        if not data:
            return description
        return description.format(**data)

    def log_entry(self, data=None):
        return {
            'error': f'{self.package}.{self.key}',
            'responsible': self.responsible,
            'message': self.message(data),
            'description': self.description,
            'data': data
        }

    def __str__(self):
        return self.key