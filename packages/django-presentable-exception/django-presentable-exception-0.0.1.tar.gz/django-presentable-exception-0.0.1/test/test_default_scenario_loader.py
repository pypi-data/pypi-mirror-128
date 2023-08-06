from django.test import TestCase
from presentable_exception.presentable_exception import DefaultScenarioLoader
from test.fake_resolver import FakeResolver

class TestDefaultScenarioLoader(TestCase):

    def setUp(self):
        self.resolver = FakeResolver()
        self.loader = DefaultScenarioLoader(resolver=self.resolver)

    def test_load_normal(self):
        packages = ['p1', 'p2']
        self.resolver.add('p1', [('e1', 'error1')])
        self.resolver.add('p2', [('e2', 'error2')])
        self.resolver.add('p3', [('e3', 'error3')]) # not in packages
        self.loader._load(packages)
        self.assertEqual('error1', self.loader.to_scenario('p1', 'e1').description)
        self.assertEqual('error2', self.loader.to_scenario('p2', 'e2').description)
        self.assertIsNone(self.loader.to_scenario('p3', 'e3'))

    def test_do_not_load_stuff_on_blacklists(self):
        # ensure, that the blacklists are not empty
        self.loader.blacklist.insert(0, 'entry1')
        self.loader.prefix_blacklist.insert(0, 'entry2')
        # construct names, that should be ignored
        p1 = self.loader.blacklist[0]
        p2 = self.loader.prefix_blacklist[0]+'.p2'
        # make the blacklisted findable
        self.resolver.add(p1, [('e1', 'error1')])
        self.resolver.add(p2, [('e2', 'error2')])
        # they should not be indexed
        self.assertIsNone(self.loader.to_scenario(p1, 'e1'))
        self.assertIsNone(self.loader.to_scenario(p2, 'e2'))

    def test_seperated_in_client_and_server_faults(self):
        packages = ['p1']
        self.resolver.add('p1', {
            'client': [('e1', 'error1')],
            'server': [('e2', 'error2')]
        })
        self.loader._load(packages)
        self.assertEqual('client', self.loader.to_scenario('p1', 'e1').responsible)
        self.assertEqual('server', self.loader.to_scenario('p1', 'e2').responsible)
