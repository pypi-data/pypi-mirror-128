from functools import reduce
from typing import Dict, List, Tuple

def transform_to_dict(raw_data: List[Tuple], col_names: List) -> List[Dict]:
    """
    Take a list of tuples usually output from postgres query execution and turn into
    list of dictionaires
    """
    output = []
    for record in raw_data:
        record_dict = {}
        for i, e in enumerate(record):
            record_dict[col_names[i]] = record[i]
        output.append(record_dict)
    return output