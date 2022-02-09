from config.convert_field_config import *


def convert_field_to_specify_field(data: dict, converter):
    for k, v in data.items():
        if hasattr(converter, k):
            _converter = getattr(converter, k)
            if _converter.prefix:
                data[f"{_converter.prefix}__{_converter.suffix}"] = data.pop(k)
            else:
                data[f"{k}__{_converter.suffix}"] = data.pop(k)
        
    return data


class Converter:
    def __init__(self, suffix, prefix=None):
        self.suffix = suffix
        self.prefix = prefix
    

class ProductConverter:
    star = Converter(GTE)
    min_price = Converter(GTE, "price")
    max_price = Converter(LTE, "price")
