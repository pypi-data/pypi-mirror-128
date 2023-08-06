# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Helpers.
"""

import logging


def _flatten_object(obj):
    """

    """
    logging.debug("obj: %s", obj)

    fields = list(filter(lambda s: not s.startswith('_'), dir(obj.fields)))
    flattened = {'id': obj.id}
    for k in fields:
        try:
            flattened[k] = obj.attributes[k]
        except:
            pass
    logging.debug("flattened: %s", flattened)

    return flattened
