import sys
import inspect
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
        attr_name = [
            s
            for s in dir(sys.modules["fibberio"])
            if s.lower() == clsname.lower() and inspect.isclass(getattr(sys.modules["fibberio"], s))
        ]
        if len(attr_name) != 1:
            raise ValueError(f"Unknown type: {clsname}")

        cl = getattr(sys.modules["fibberio"], attr_name[0])

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
