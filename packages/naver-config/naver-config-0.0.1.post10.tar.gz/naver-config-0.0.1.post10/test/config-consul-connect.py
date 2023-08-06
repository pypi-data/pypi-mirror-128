from naver_config.consul import ConsulClient 
import unittest


class MainTest(unittest.TestCase):
    # def test_getValue(self):
    #     c = ConsulClient()
    #     self.assertIsNotNone(c.getValue("data"))

    # def test_setValue(self):
    #     c = ConsulClient()
    #     self.assertIsNotNone(c.setValue("data2", "test"))
 
    def test_deleteValue(self):
        c = ConsulClient()
        self.assertIsNotNone(c.deleteValue("data2"))

    # def test_createNode(self):
    #     c = ConsulClient()
    #     self.assertIsNotNone(c.createNode("testnode"))

    def test_deleteNode(self):
        c = ConsulClient()
        self.assertIsNotNone(c.deleteNode("node1"))

    # def test_registerService(self):
    #     c = ConsulClient()
    #     self.assertIsNotNone(c.registerService("testservice"))

    def test_deregisterService(self):
        c = ConsulClient()
        self.assertIsNotNone(c.deregisterService("testservice"))
    pass