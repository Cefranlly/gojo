import ruamel.yaml
from gojo.utils.log import get_logger


logger = get_logger(__name__)


def get_ds_in_yaml_str_format(source_name: str, input_dict: dict):
   """
   i.e in Snowflake
    data_source events:
      type: snowflake
      host: ${SNOWFLAKE_HOST}
      username: ${SNOWFLAKE_USERNAME}
      password: ${SNOWFLAKE_PASSWORD}
      database: events
      schema: public
   """
   yaml_output = ruamel.yaml.dump(
      {"data_source {}".format(source_name): input_dict},
      Dumper=ruamel.yaml.RoundTripDumper,
      default_flow_style=False,
      indent=2,
      )

   return yaml_output
