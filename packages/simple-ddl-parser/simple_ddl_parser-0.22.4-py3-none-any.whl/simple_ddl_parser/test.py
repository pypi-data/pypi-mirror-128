from simple_ddl_parser import DDLParser

ddl =  """
        CREATE TABLE `my.data-cdh-hub-REF-CALENDAR` (
  calendar_dt DATE,
  calendar_dt_id INT
  )
OPTIONS (
    location="location"
    )
OPTIONS (
  description="Calendar table records reference list of calendar dates and related attributes used for reporting."
  )
  OPTIONS (
    name ="path"
)
OPTIONS (
    kms_two="path",
    two="two two"
)
OPTIONS (
    kms_three="path",
    three="three",
    threethree="three three"
)
OPTIONS (
    kms_four="path",
    four="four four",
    fourin="four four four",
    fourlast="four four four four"
);
        """
result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
import pprint

pprint.pprint(result)
