from typing import List, Dict, Any
from pydantic import Field
from data_models.base_check_model import BaseCheckResponseModel


class BaseSodaModel(BaseCheckResponseModel):
   class Config:
      alias_generator = lambda s: s


class SodaMetricModel(BaseSodaModel):
   identity: str
   metric_name: str = Field(alias="metricName")
   value: str
   data_source_name: str = Field(alias="dataSourceName")


class SodaChecksModel(BaseSodaModel):
   identity: str
   name: str
   type: str
   definition: str
   resource_attributes: List[Any] = Field(alias="resourceAttributes")
   location: Dict[str, Any]
   data_source: str = Field(alias="dataSource")
   table: str
   filter: str | None
   column: str
   metrics: List[str]
   outcome: str
   outcome_reasons: List = Field(alias="outcomeReasons")
   archetype: str | None
   diagnostics: Dict[str, Any]


class SodaCheckResponseModel(BaseSodaModel):
   definition_name: str | None = Field(alias="definitionName")
   default_data_source: str = Field(alias="defaultDataSource")
   data_timestamp: str = Field(alias="dataTimestamp")
   scan_start_timestamp: str = Field(alias="scanStartTimestamp")
   scan_end_timestamp: str = Field(alias="scanEndTimestamp")
   has_errors: bool = Field(alias="hasErrors")
   has_warnings: bool = Field(alias="hasWarnings")
   has_failures: bool = Field(alias="hasFailures")
   metrics: List[SodaMetricModel]
   checks: List[SodaChecksModel]
   queries: List[Dict[str, Any]]
   logs: List[Dict[str, Any]]