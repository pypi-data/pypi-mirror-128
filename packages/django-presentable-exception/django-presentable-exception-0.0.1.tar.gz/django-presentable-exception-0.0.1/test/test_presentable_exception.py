from unittest import TestCase
from unittest.suite import TestSuite

from presentable_exception.presentable_exception import PresentableClientException, PresentableException, PresentableServerException
from test.fake_scenario import FakeScenario, FakeScenarioLoader


class TestPresentableException(TestCase):

    def setUp(self):
        self.loader = FakeScenarioLoader()
        self.scenario = FakeScenario('package', 'key', 'this is a message', {'a': 'log'})
        self.loader.register_scenario(self.scenario)

    def test_passes_through_message(self):
        exception = PresentableException.of('package', 'key', scenario_loader=self.loader)
        self.assertEqual('this is a message', exception.message)

    def test_passes_through_log(self):
        exception = PresentableException.of('package', 'key', scenario_loader=self.loader)
        self.assertEqual({'a': 'log'}, exception.log_entry)

    def test_scenario_not_found(self):
        exception = PresentableException.of('unknown', 'unknown', scenario_loader=self.loader)
        self.assertTrue(exception.message)
        self.assertTrue(exception.log_entry)
        self.assertIsInstance(exception, PresentableServerException)

    def test_server_exception(self):
        self.scenario.responsible = 'server'
        exception = PresentableException.of('package', 'key', scenario_loader=self.loader)
        self.assertIsInstance(exception, PresentableServerException)

    def test_clien_exception(self):
        self.scenario.responsible = 'client'
        exception = PresentableException.of('package', 'key', scenario_loader=self.loader)
        self.assertIsInstance(exception, PresentableClientException)
