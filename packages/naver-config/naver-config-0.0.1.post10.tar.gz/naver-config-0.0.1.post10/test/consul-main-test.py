from naver_config.consul import main
import logging


import unittest


class MainTest(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main("Consul Main"), "Consul Main")


if __name__ == '__main__':
    print("Consul Main")
    main("Consul Main")
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    logger = logging.getLogger('tcpserver')
    logger.warning('Protocol problem: %s', 'connection reset', extra=d)
