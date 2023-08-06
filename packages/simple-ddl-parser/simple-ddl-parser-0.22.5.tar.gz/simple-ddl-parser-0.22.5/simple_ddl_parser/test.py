from simple_ddl_parser import DDLParser


ddl =   """
    CREATE TABLE IF NOT EXISTS default.salesorderdetail(
            something<2% ARRAY<structcolx:string,coly:string>
            )"""
parse_result = DDLParser(ddl).run(group_by_type=True)
import pprint
pprint.pprint(parse_result)
