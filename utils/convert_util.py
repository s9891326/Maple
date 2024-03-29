from typing import Dict, Any

from config.convert_field_config import *


def convert_field_to_sql_query(data: dict, converter) -> Dict[str, Any]:
    """
    轉換欄位型態，讓該型態能直接進行ORM語法
    :param data:
    :param converter:
    :return:
    """
    sql_query = dict()
    for k, v in data.items():
        if hasattr(converter, k):
            _converter = getattr(converter, k)
            if _converter.prefix:
                sql_query[f"{_converter.prefix}__{_converter.suffix}"] = data[k]
            else:
                sql_query[f"{k}__{_converter.suffix}"] = data[k]
        else:
            sql_query[k] = v
    return sql_query


class Converter:
    def __init__(self, suffix, prefix=None):
        self.suffix = suffix
        self.prefix = prefix


class ProductListConverter:
    stage_level = Converter(IN)
    name = Converter(CONTAINS)
    career = Converter(IN)


class ProductConverter:
    star = Converter(GTE)
    total_level = Converter(GTE)
    min_price = Converter(GTE, "price")
    max_price = Converter(LTE, "price")
    min_star = Converter(GTE, "star")
    max_star = Converter(LTE, "star")
