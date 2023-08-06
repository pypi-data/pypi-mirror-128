from box import Box
from pyspark.sql.session import SparkSession
from databricksbundle.storage.StorageConfiguratorInterface import StorageConfiguratorInterface


class TestingConfigurator(StorageConfiguratorInterface):
    def configure(self, spark: SparkSession, config: Box):
        spark.conf.set(f"testing.storage.{config.storage_name}", f"tenant/{config.tenant_id}")
        spark.conf.set(f"testing.secrets.{config.storage_name}", f"secrets/{config.secret_scope}/{config.secret_key}")

    def get_type(self):
        return "testing"
