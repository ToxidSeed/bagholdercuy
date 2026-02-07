import importlib
import pkgutil

_INIT_REGISTRY = {}


def register_init(name):
    def _decorator(func):
        _INIT_REGISTRY[name] = func
        return func

    return _decorator


def init_all():
    for module in pkgutil.iter_modules(__path__):
        if module.name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{module.name}")

    for func in _INIT_REGISTRY.values():
        func()

__all__ = [
    "register_init",
    "init_all"
]
