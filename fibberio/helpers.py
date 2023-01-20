import sys
from pathlib import Path
from typing import Any, Dict, Tuple


class Item:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(item: Dict[str, Any], root: Path = None) -> Tuple[str, Any]:
        # retrieve id if available
        if "id" in item:
            id = item.pop("id")
        else:
            id = None

        # class and args
        clsname = next(iter(item))
        kwargs = item[clsname]
        cl = getattr(sys.modules["fibberio"], clsname.capitalize())

        # sort relative paths
        if "path" in kwargs:
            fp = Path(kwargs["path"])
            if not fp.is_absolute():
                if root is not None:
                    fp = root.joinpath(fp)
                    kwargs["path"] = str(fp.resolve().absolute().as_posix())
                else:
                    raise ValueError("Relative paths are not allowed without a root path")

        cls = cl(**kwargs)
        return id, cls
