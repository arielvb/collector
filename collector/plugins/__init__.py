"""
Plugins
=======
This module containes the plugins definition.
"""


def get_sys_plugins():
    """Returns the system plugins"""
    from boardgamegeek import PluginBoardGameGeek
    from csvimport import PluginCsvImport
    return [PluginBoardGameGeek(), PluginCsvImport()]
