from typing import Tuple

def parsehv(region_name: str) -> Tuple[int, int]:
    h = int(region_name[1:3])
    v = int(region_name[4:6])

    return h, v
