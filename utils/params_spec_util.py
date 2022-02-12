from typing import List

from data_spec_validator.spec import *

from exchange.models import ProductList, Product
from utils.convert_util import convert_field_to_sql_query


def extract_request_param_data(target_spec, query_params: dict, converter=None):
    fields = extract_fields(target_spec)
    data = {k: v for k, v in query_params.items() if k in fields}
    
    if converter:
        data = convert_field_to_sql_query(data, converter)
    
    return data


def extract_fields(spec) -> List[str]:
    if not isinstance(type(spec), type):
        raise RuntimeError(f'{spec} should be just a class')
    
    return list(filter(lambda f: type(f) == str and not (f.startswith('__') and f.endswith('__')), spec.__dict__))


class ProductListSpec:
    category = Checker([ONE_OF], optional=True, extra={ONE_OF: ProductList.Category.values})
    type = Checker([STR], optional=True)
    stage_level = Checker([ONE_OF], optional=True, extra={ONE_OF: ProductList.Stage.values})


class ProductSpec:
    star = Checker([INT], optional=True, op=CheckerOP.ANY)
    is_maple = Checker([BOOL, KEY_COEXISTS], optional=True, op=CheckerOP.ALL)
    maple_capability = Checker([ONE_OF, KEY_COEXISTS], optional=True, extra={
        ONE_OF: Product.MapleCapability.values,
        KEY_COEXISTS: ["is_maple"]
    })
    total_level = Checker([INT], optional=True, op=CheckerOP.ANY)
    min_price = Checker([INT], optional=True, op=CheckerOP.ANY)
    max_price = Checker([INT], optional=True, op=CheckerOP.ANY)

