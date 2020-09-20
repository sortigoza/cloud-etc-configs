import unittest

from cloud_etc_configs.logger import get_logger

logger = get_logger()


class TestLogger(unittest.TestCase):
    def test_logger(self):
        with self.assertLogs("cloud_etc_configs", level="INFO") as cm:
            logger.info("testing")
        self.assertEqual(cm.output, ["INFO:cloud_etc_configs.logger:testing"])
