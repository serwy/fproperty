import unittest

from fproperty.api import fproperty, property

class Thing:
    def __init__(self):
        self._get_only = '_get_only'
        self._set_only = '_set_only'
        self._del_only = '_del_only'
        self._full = True

    @fproperty
    def get_only():
        def g(self):
            return self._get_only
        return (g,)

    @fproperty
    def set_only():
        def s(self, value):
            self._set_only = value
        return (None, s)

    @fproperty
    def del_only():
        def d(self):
            del self._del_only
        return (None, None, d)

    @fproperty.apply
    def doc_only():
        return (None, None, None, 'doc_only')

    @property.apply
    def full():
        def g(self): return self._full
        def s(self, v): self._full = v
        def d(self): del self._full
        return (g, s, d, 'full')


class TestMain(unittest.TestCase):

    def test_get(self):
        t = Thing()
        self.assertEqual(t.get_only, '_get_only')

        with self.assertRaises(AttributeError):
            t.get_only = False

        with self.assertRaises(AttributeError):
            del t.get_only

    def test_set(self):
        t = Thing()
        self.assertEqual(t._set_only, '_set_only')
        t.set_only = 123
        self.assertEqual(t._set_only, 123)

        with self.assertRaises(AttributeError):
            x = t.set_only

        with self.assertRaises(AttributeError):
            del t.set_only

    def test_del(self):
        t = Thing()
        self.assertEqual(t._del_only, '_del_only')

        with self.assertRaises(AttributeError):
            x = t.del_only

        with self.assertRaises(AttributeError):
            t.del_only = True

        del t.del_only
        self.assertFalse(hasattr(t, '_del_only'))

    def test_doc(self):
        t = Thing()
        self.assertEqual(
            Thing.doc_only.__doc__,
            'doc_only'
        )

        with self.assertRaises(AttributeError):
            x = t.doc_only

        with self.assertRaises(AttributeError):
            t.doc_only = False

        with self.assertRaises(AttributeError):
            del t.doc_only

    def test_full(self):
        t = Thing()
        t.full = 123
        self.assertEqual(t.full, 123)

        del t.full

        with self.assertRaises(AttributeError):
            x = t.full

if __name__ == '__main__':
    unittest.main(verbosity=2)
