# All imports start with an underscore, except the one we
# want to publicly export.
import inspect as _inspect
import importlib as _importlib
import sys as _sys

import pandas as _pd

from terality_serde.json_encoding import (
    instantiate_pandas_arrow_extension_types as _instantiate_pandas_arrow_extension_types,
)

from .version import __version__

# Rename all imported symbols that should not be public to start with an underscore.
# (prevent a user from doing `from terality import top_level_functions` for instance).
from ._terality.terality_structures.top_level import (
    get_dynamic_top_level_attribute as _get_dynamic_top_level_attribute,
    top_level_functions as _top_level_functions,
)
from ._terality.utils.anonymous import create_anonymous_user as _create_anonymous_user

from ._terality.terality_structures.ndarray import NDArray
from ._terality.terality_structures.dataframe import DataFrame
from ._terality.terality_structures.index import Index
from ._terality.terality_structures.index import Int64Index
from ._terality.terality_structures.index import Float64Index
from ._terality.terality_structures.index import DatetimeIndex
from ._terality.terality_structures.index import MultiIndex
from ._terality.terality_structures.series import Series


def quickstart():
    """Get started with Terality without any setup: create a temporary Terality account on this machine.

    By using this method, you agree to the terms and conditions at https://www.terality.com/terms.

    This method should only be used when evaluating Terality. For any real usage, please create a permanent
    Terality account at https://app.terality.com (it's free).

    The account created by this quickstart method has a limited duration, after which all data in this
    account will be deleted. This quickstart account also has a lower data cap than a normal account, and
    can't be upgraded.

    When the lifetime of the quickstart account is exceeded, further calls to Terality will return errors.
    """
    _create_anonymous_user()


def __getattr__(attribute: str):
    return _get_dynamic_top_level_attribute(attribute)


def __dir__():
    # Static members.
    members = set(name for name in globals() if not name.startswith("_"))
    # Dynamic members.
    members |= _top_level_functions
    return members


# Reexport all (public) pandas submodules too.
# This is required to make importing submodules ("import terality.tseries.offsets") work.
for _attribute_name in dir(_pd):
    # Don't reexport private pandas names
    if _attribute_name.startswith("_"):
        continue
    # pandas does some magic when importing these submodules, for instance:
    #     >>> import pandas
    #     >>> from pandas import pandas as pandas_2
    #     >>> pandas_2 is pandas
    #     True
    # so let's just skip them instead of trying to work around this
    if _attribute_name in ["offsets", "pandas"]:
        continue
    _pd_attribute = getattr(_pd, _attribute_name)
    if _inspect.ismodule(_pd_attribute):
        _sys.modules[f"terality.{_attribute_name}"] = _importlib.import_module(
            f".{_attribute_name}", "pandas"
        )


_instantiate_pandas_arrow_extension_types()
