import sys
from typing import Any, Dict, Tuple


class Item:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(item: Dict[str, Any]) -> Tuple[str, Any]:
        # retrieve id if available
        if "id" in item:
            id = item.pop("id")
        else:
            id = None

        # class and args
        clsname = next(iter(item))
        kwargs = item[clsname]
        cl = getattr(sys.modules["fibberio"], clsname.capitalize())
        cls = cl(**kwargs)
        return id, cls
