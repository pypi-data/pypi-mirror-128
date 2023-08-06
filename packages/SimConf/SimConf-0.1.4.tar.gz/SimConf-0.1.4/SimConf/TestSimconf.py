import unittest
import collections

from simconf import SimConf


class TestSimconfDict(unittest.TestCase):

    def setUp(self):
        self.defaultAtr = {"atr0": 0}
        self.conf = SimConf(default_atr=self.defaultAtr, load_conf=False)

    def test_init(self):
        self.assertEqual(self.conf.filename, "config")
        self.assertEqual(self.conf.default_atr, self.defaultAtr)
        self.assertEqual(self.conf.data, self.defaultAtr)
        self.assertEqual(self.conf.ensure_ascii, True)
        self.assertEqual(self.conf.load_conf, False)

    def test_setitem(self):
        self.assertEqual(self.conf.__setitem__("atr1",1), None)
        self.assertEqual(self.conf.__setitem__(1,1), None)
        self.assertEqual(self.conf.__setitem__(1,[1,2]), None)
        self.assertEqual(self.conf.append("atr2", 2), None)
        with self.assertRaises(TypeError):
            self.conf.__setitem__(1,1,1)
        with self.assertRaises(TypeError):
            self.conf.__setitem__([1],1)
        with self.assertRaises(AttributeError):
            self.conf.append(2)

    def test_getitem(self):
        self.assertEqual(self.conf["atr0"], 0)
        with self.assertRaises(KeyError):
            self.conf["0"]
        with self.assertRaises(KeyError):
            self.conf[0]
        with self.assertRaises(KeyError):
            self.conf[0,2]

    def test_len(self):
        self.assertEqual(len(self.conf), 1)

    def test_iter(self):
        self.assertIsInstance(self.conf.__iter__(), collections.abc.Iterable)
        self.assertEqual(list(self.conf.keys()), ["atr0"])
        self.assertEqual(list(self.conf.values()), [0])
        self.assertEqual(list(self.conf.items()), [("atr0", 0)])

    def test_save(self):
        self.assertEqual(self.conf.save(), None)

    def test_load(self):
        self.assertEqual(self.conf.load(), self.defaultAtr)

    def test_getDefault(self):
        self.assertEqual(self.conf.get_default(), self.defaultAtr)

    def test_setDefault(self):
        self.conf["1"] = 1
        self.assertEqual(self.conf.set_default(), None)
        self.assertEqual(self.conf.get_default(), self.defaultAtr)

    def test_print(self):
        self.assertEqual(self.conf.print_all(), None)


class TestSimconfList(unittest.TestCase):

    def setUp(self):
        self.defaultAtr = [1]
        self.conf = SimConf(default_atr=self.defaultAtr, load_conf=False)

    def test_init(self):
        self.assertEqual(self.conf.filename, "config")
        self.assertEqual(self.conf.default_atr, self.defaultAtr)
        self.assertEqual(self.conf.data, self.defaultAtr)
        self.assertEqual(self.conf.ensure_ascii, True)
        self.assertEqual(self.conf.load_conf, False)

    def test_setitem(self):
        self.assertEqual(self.conf.append(2), None)
        self.assertEqual(self.conf.append([2,3]), None)
        self.assertEqual(self.conf.__setitem__(1,[1,2]), None)
        self.assertEqual(self.conf.__setitem__(1,1), None)
        with self.assertRaises(TypeError):
            self.conf.__setitem__("atr1",1)
        with self.assertRaises(TypeError):
            self.conf.__setitem__(1,1,1)
        with self.assertRaises(TypeError):
            self.conf.__setitem__([1],1)
        with self.assertRaises(AttributeError):
            self.conf.append("atr2", 2)

    def test_getitem(self):
        self.assertEqual(self.conf[0], 1)
        self.assertEqual(self.conf[0:2], [1])
        with self.assertRaises(TypeError):
            self.conf["0"]
        with self.assertRaises(TypeError):
            self.conf[0,2]

    def test_len(self):
        self.assertEqual(len(self.conf), 1)

    def test_iter(self):
        self.assertIsInstance(self.conf.__iter__(), collections.abc.Iterable)
        self.assertEqual(list(self.conf.keys()), [0])
        self.assertEqual(list(self.conf.values()), [1])
        self.assertEqual(list(self.conf.items()), [(0, 1)])

    def test_save(self):
        self.assertEqual(self.conf.save(), None)

    def test_load(self):
        self.assertEqual(self.conf.load(), self.defaultAtr)

    def test_getDefault(self):
        self.assertEqual(self.conf.get_default(), self.defaultAtr)

    def test_setDefault(self):
        self.conf.append(1)
        self.assertEqual(self.conf.set_default(), None)
        self.assertEqual(self.conf.get_default(), self.defaultAtr)

    def test_print(self):
        self.assertEqual(self.conf.print_all(), None)


class TestSimconfList(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(TypeError):
            self.conf = SimConf(load_conf=12)
        with self.assertRaises(TypeError):
            self.conf = SimConf(filename=12)
        with self.assertRaises(TypeError):
            self.conf = SimConf(default_atr=12)
        with self.assertRaises(TypeError):
            self.conf = SimConf(default_atr=())
        with self.assertRaises(TypeError):
            self.conf = SimConf(ensure_ascii=12)


if __name__ == '__main__':
    unittest.main()
