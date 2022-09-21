from typing import List, Tuple, Union, Dict

from data_spec_validator.spec import *
from data_spec_validator.spec import custom_spec
from data_spec_validator.spec.defines import BaseValidator

from exchange.models import ProductList, Product
from utils.convert_util import convert_field_to_sql_query

LIST_IN = "list_in"

class ListInValidator(BaseValidator):
    name = LIST_IN
    
    @staticmethod
    def validate(value, extra, data) -> Tuple[bool, Union[Exception, str]]:
        valid_data = extra.get(ListInValidator.name)
        for v in value:
            if v not in valid_data:
                return False, ValueError("Input values isn't valid values.")
        return True, ""

custom_spec.register(dict(list_in=ListInValidator()))


def extract_request_param_data(target_spec, query_params: dict, converter=None) -> Dict[str, str]:
    """
    根據target_spec指定的spec來抓取要查詢DB的欄位，並透過converter來轉換欄位格式
    :param target_spec:
    :param query_params:
    :param converter:
    :return:
    """
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
    name = Checker([STR], optional=True)
    stage_level = Checker([LIST, LIST_IN], optional=True, op=CheckerOP.ALL, extra={LIST_IN: ProductList.Stage.values})
    career = Checker([STR], optional=True)


class ProductSpec:
    star = Checker([INT], optional=True)
    is_maple = Checker([BOOL], optional=True)
    maple_capability = Checker([ONE_OF, KEY_COEXISTS], optional=True, op=CheckerOP.ALL, extra={
        ONE_OF: Product.MapleCapability.values,
        KEY_COEXISTS: ["is_maple"]
    })
    total_level = Checker([INT], optional=True)
    min_price = Checker([INT, KEY_COEXISTS], optional=True, op=CheckerOP.ALL, extra={KEY_COEXISTS: ["max_price"]})
    max_price = Checker([INT, KEY_COEXISTS], optional=True, op=CheckerOP.ALL, extra={KEY_COEXISTS: ["min_price"]})
    server_name = Checker([STR], optional=True)
    min_star = Checker([INT, KEY_COEXISTS], optional=True, op=CheckerOP.ALL, extra={KEY_COEXISTS: ["max_star"]})
    max_star = Checker([INT, KEY_COEXISTS], optional=True, op=CheckerOP.ALL, extra={KEY_COEXISTS: ["min_star"]})

