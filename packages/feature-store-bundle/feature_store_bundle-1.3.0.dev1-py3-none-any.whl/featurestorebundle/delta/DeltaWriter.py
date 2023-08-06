from pyspark.sql import DataFrame
from featurestorebundle.db.TableNames import TableNames
from featurestorebundle.delta.DeltaDataHandler import DeltaDataHandler
from featurestorebundle.delta.DeltaMergeConfigGenerator import DeltaMergeConfigGenerator
from featurestorebundle.feature.FeaturesStorage import FeaturesStorage
from featurestorebundle.feature.TablePreparer import TablePreparer
from featurestorebundle.metadata.MetadataTablePreparer import MetadataTablePreparer
from featurestorebundle.feature.FeaturesPreparer import FeaturesPreparer
from featurestorebundle.feature.FeaturesValidator import FeaturesValidator
from featurestorebundle.feature.writer.FeaturesWriterInterface import FeaturesWriterInterface


class DeltaWriter(FeaturesWriterInterface):
    def __init__(
        self,
        delta_data_handler: DeltaDataHandler,
        delta_merge_config_generator: DeltaMergeConfigGenerator,
        table_preparer: TablePreparer,
        metadata_table_preparer: MetadataTablePreparer,
        features_preparer: FeaturesPreparer,
        features_validator: FeaturesValidator,
        table_names: TableNames,
    ):
        self.__delta_data_handler = delta_data_handler
        self.__delta_merge_config_generator = delta_merge_config_generator
        self.__table_preparer = table_preparer
        self.__metadata_table_preparer = metadata_table_preparer
        self.__features_preparer = features_preparer
        self.__features_validator = features_validator
        self.__table_names = table_names

    def write_latest(self, features_storage: FeaturesStorage, archive=False):
        entity = features_storage.entity
        feature_list = features_storage.feature_list
        features_data = self.prepare_features(features_storage)

        self.__features_validator.validate(entity, features_data, feature_list)

        full_table_name = self.__table_names.get_latest_full_table_name(entity.name)
        metadata_full_table_name = self.__table_names.get_latest_metadata_full_table_name(entity.name)
        data_path = self.__table_names.get_latest_path(entity.name)
        metadata_path = self.__table_names.get_latest_metadata_path(entity.name)
        pk_columns = [entity.id_column]

        if archive:
            self.__delta_data_handler.archive(entity)

        self.__table_preparer.prepare(full_table_name, data_path, entity, feature_list)
        self.__metadata_table_preparer.prepare(metadata_full_table_name, metadata_path, entity)

        config = self.__delta_merge_config_generator.generate(
            entity,
            features_data,
            pk_columns,
        )

        self.__delta_data_handler.write(full_table_name, metadata_full_table_name, config, feature_list)

    def write_historized(self, features_storage: FeaturesStorage):
        entity = features_storage.entity
        feature_list = features_storage.feature_list
        features_data = self.prepare_features(features_storage)

        self.__features_validator.validate(entity, features_data, feature_list)

        full_table_name = self.__table_names.get_historized_full_table_name(entity.name)
        metadata_full_table_name = self.__table_names.get_historized_metadata_full_table_name(entity.name)
        data_path = self.__table_names.get_historized_path(entity.name)
        metadata_path = self.__table_names.get_historized_metadata_path(entity.name)
        pk_columns = [entity.id_column, entity.time_column]

        self.__table_preparer.prepare(full_table_name, data_path, entity, feature_list)
        self.__metadata_table_preparer.prepare(metadata_full_table_name, metadata_path, entity)

        config = self.__delta_merge_config_generator.generate(
            entity,
            features_data,
            pk_columns,
        )

        self.__delta_data_handler.write(full_table_name, metadata_full_table_name, config, feature_list)

    def prepare_features(self, features_storage: FeaturesStorage) -> DataFrame:
        return self.__features_preparer.prepare(features_storage.entity, features_storage.results)
