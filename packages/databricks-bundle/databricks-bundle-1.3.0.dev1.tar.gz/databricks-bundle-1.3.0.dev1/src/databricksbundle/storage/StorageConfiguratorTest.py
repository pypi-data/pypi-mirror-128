import unittest
from pyfonycore.bootstrap import bootstrapped_container
from databricksbundle.storage.StorageConfigurator import StorageConfigurator
from databricksbundle.storage.testing.SparkSessionMock import SparkSessionMock


class StorageConfiguratorTest(unittest.TestCase):
    def test_azure(self):
        container = bootstrapped_container.init("test_azure")
        storage_configurator: StorageConfigurator = container.get(StorageConfigurator)

        spark_mock = SparkSessionMock()

        storage_configurator.configure(spark_mock)

        self.assertEqual("tenant/123456", spark_mock.conf.get("testing.storage.aaa"))
        self.assertEqual("secrets/some_scope1/some_key1", spark_mock.conf.get("testing.secrets.aaa"))
        self.assertEqual("tenant/987654", spark_mock.conf.get("testing.storage.bbb"))
        self.assertEqual("secrets/some_scope2/some_key2", spark_mock.conf.get("testing.secrets.bbb"))


if __name__ == "__main__":
    unittest.main()
