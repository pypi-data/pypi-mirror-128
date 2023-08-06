from unittest import TestCase as UnitTestCase
from presentable_exception.presentable_exception import Locator
from test.fake_resolver import FakeResolver

class TestLocator(UnitTestCase):
    
    def setUp(self):
        self.resolver = FakeResolver()

    def test_locate_all_empty(self):
        self.assertEqual({}, Locator().locate([]))

    def test_locate_one_found(self):
        content = [('error key', 'error description')]
        self.resolver.add('my_package', content)
        locator = Locator(resolver=self.resolver)
        res = locator.locate(['my_package', 'some_other_package'])
        self.assertEqual({'my_package': content}, res)

    def test_on_prefix_blacklist_ignored(self):
        content = [('error key', 'error description')]
        self.resolver.add('my_package', content)
        prefix_blacklist = ['my_']
        locator = Locator(resolver=self.resolver, prefix_blacklist=prefix_blacklist)
        res = locator.locate(['my_package'])
        self.assertEqual({}, res)

    def test_on_blacklist_ignored(self):
        content = [('error key', 'error description')]
        self.resolver.add('my_package', content)
        blacklist = ['my_package']
        locator = Locator(resolver=self.resolver, blacklist=blacklist)
        res = locator.locate(['my_package'])
        self.assertEqual({}, res)

    def test_empty_content_gets_ignored(self):
        content = [] # note, that the content is empty
        self.resolver.add('my_package', content)
        locator = Locator(resolver=self.resolver)
        res = locator.locate(['my_package'])
        self.assertEqual({}, res)

    def test_passes_along_raw_content(self):
        content = 'there can be anything in here'
        self.resolver.add('my_package', content)
        locator = Locator(resolver=self.resolver)
        res = locator.locate(['my_package'])
        self.assertEqual({'my_package': 'there can be anything in here'}, res)

    def test_different_valid_inputs(self):
        content = [('error key', 'error description')]
        self.resolver.add('my_package', content)
        locator = Locator(resolver=self.resolver)
        for valid_input in ['my_package', ['my_package'], ('my_package')]:
            res = locator.locate(valid_input)
            self.assertEqual({'my_package': content}, res)

    def test_invalid_input(self):
        content = [('error key', 'error description')]
        self.resolver.add('my_package', content)
        locator = Locator(resolver=self.resolver)
        for invalid_input in [set, 1, 1.1]:
            res = locator.locate(invalid_input)
            self.assertEqual({}, res)
        
