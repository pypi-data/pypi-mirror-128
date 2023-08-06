#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = """

TODO: NOT DONE

Collection of first-party plugins.

This module exists to isolate munin.program from the potentially
heavyweight build dependencies for first-party plugins.
This way people doing custom builds of Munin have the option to only pay for the
dependencies they want.

This module also grants the flexibility to those doing custom builds, to
automatically inherit the centrally-maintained list of standard plugins,
for less repetition.

Created on 27/04/2019

@author: cnheider
"""

import logging

import pkg_resources

from tensorboard.backend import experimental_plugin
from tensorboard.plugins.audio import audio_plugin
from tensorboard.plugins.core import core_plugin
from tensorboard.plugins.custom_scalar import custom_scalars_plugin
from tensorboard.plugins.debugger_v2 import debugger_v2_plugin
from tensorboard.plugins.distribution import distributions_plugin
from tensorboard.plugins.graph import graphs_plugin
from tensorboard.plugins.histogram import histograms_plugin
from tensorboard.plugins.hparams import hparams_plugin
from tensorboard.plugins.image import images_plugin
from tensorboard.plugins.pr_curve import pr_curves_plugin
from tensorboard.plugins.profile_redirect import profile_redirect_plugin
from tensorboard.plugins.scalar import scalars_plugin
from tensorboard.plugins.text import text_plugin
from tensorboard.plugins.text_v2 import text_v2_plugin
from tensorboard.plugins.mesh import mesh_plugin

logger = logging.getLogger(__name__)


class ExperimentalTextV2Plugin(text_v2_plugin.TextV2Plugin, experimental_plugin.ExperimentalPlugin):
    """Angular Text Plugin marked as experimental."""

    pass


# Ordering matters. The order in which these lines appear determines the
# ordering of tabs in TensorBoard's GUI.
_PLUGINS = [
    core_plugin.CorePluginLoader,
    scalars_plugin.ScalarsPlugin,
    custom_scalars_plugin.CustomScalarsPlugin,
    images_plugin.ImagesPlugin,
    audio_plugin.AudioPlugin,
    debugger_v2_plugin.DebuggerV2Plugin,
    graphs_plugin.GraphsPlugin,
    distributions_plugin.DistributionsPlugin,
    histograms_plugin.HistogramsPlugin,
    text_plugin.TextPlugin,
    pr_curves_plugin.PrCurvesPlugin,
    profile_redirect_plugin.ProfileRedirectPluginLoader,
    hparams_plugin.HParamsPlugin,
    mesh_plugin.MeshPlugin,
    ExperimentalTextV2Plugin,
]


def get_plugins():
    """Returns a list specifying all known TensorBoard plugins.

    This includes both first-party, statically bundled plugins and
    dynamic plugins.

    This list can be passed to the `tensorboard.program.TensorBoard` API.

    Returns:
      The list of default first-party plugins.
    """
    return get_static_plugins() + get_dynamic_plugins()


def get_static_plugins():
    """Returns a list specifying TensorBoard's default first-party plugins.

    Plugins are specified in this list either via a TBLoader instance to load the
    plugin, or the TBPlugin class itself which will be loaded using a BasicLoader.

    This list can be passed to the `tensorboard.program.TensorBoard` API.

    Returns:
      The list of default first-party plugins.

    :rtype: list[Type[base_plugin.TBLoader] | Type[base_plugin.TBPlugin]]
    """

    return _PLUGINS[:]


def get_dynamic_plugins():
    """Returns a list specifying TensorBoard's dynamically loaded plugins.

    A dynamic TensorBoard plugin is specified using entry_points [1] and it is
    the robust way to integrate plugins into TensorBoard.

    This list can be passed to the `tensorboard.program.TensorBoard` API.

    Returns:
      The list of dynamic plugins.

    :rtype: list[Type[base_plugin.TBLoader] | Type[base_plugin.TBPlugin]]

    [1]: https://packaging.python.org/specifications/entry-points/
    """

    # .load() method to import and load that entry point (module or object).
    # from importlib import metadata # new method!
    # return [      entry_point.load()      for entry_point in metadata.entry_points()["munin_plugins"]      ]
    return [entry_point.load() for entry_point in pkg_resources.iter_entry_points("munin_plugins")]


if __name__ == "__main__":
    print(get_plugins())
