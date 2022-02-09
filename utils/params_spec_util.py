from typing import List

from data_spec_validator.spec import *

from exchange.models import ProductList, Product
from utils.convert_util import convert_field_to_specify_field


def extract_request_param_data(target_spec, query_params: dict, converter=None):
    fields = extract_fields(target_spec)
    data = {k: v for k, v in query_params.items() if k in fields}
    
    if converter:
        data = convert_field_to_specify_field(data, converter)
    
    return data


def extract_fields(spec) -> List[str]:
    if not isinstance(type(spec), type):
        raise RuntimeError(f'{spec} should be just a class')
    
    return list(filter(lambda f: type(f) == str and not (f.startswith('__') and f.endswith('__')), spec.__dict__))


class ProductListSpec:
    # list(map(str, ProductList.Stage))
    category = Checker([ONE_OF], optional=True, extra={ONE_OF: [c.value for c in ProductList.Category]})
    type = Checker([STR], optional=True)
    stage_level = Checker([ONE_OF], optional=True, extra={ONE_OF: [s.value for s in ProductList.Stage]})


class ProductSpec:
    star = Checker([DIGIT_STR, INT], optional=True, op=CheckerOP.ANY)
    is_maple = Checker([DIGIT_STR, KEY_COEXISTS], optional=True, op=CheckerOP.ALL, extra={
        KEY_COEXISTS: ["maple_capability"]
    })
    maple_capability = Checker([ONE_OF, KEY_COEXISTS], optional=True, extra={
        ONE_OF: [m.value for m in Product.Maple],
        KEY_COEXISTS: ["is_maple"]
    })
    total_level = Checker([DIGIT_STR, INT], optional=True, op=CheckerOP.ANY)
    min_price = Checker([DIGIT_STR, INT], optional=True, op=CheckerOP.ANY)
    max_price = Checker([DIGIT_STR, INT], optional=True, op=CheckerOP.ANY)

