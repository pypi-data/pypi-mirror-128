# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Michał Góral.

"""
Functions passed to jinja templates
"""

import logging
from dateutil.parser import parse as parse_dt

from stag.utils import date_sorting_key as _date_sorting

from slugify import slugify

log = logging.getLogger(__name__)


def _is_date(val):
    return isinstance(val, date)


def strftime(val, format):
    if not val:
        return ""

    try:
        if isinstance(val, (int, float, str)):
            dt = parse_dt(val)
        else:
            dt = val
        return dt.strftime(format)
    except ValueError:
        return val


def isoformat(val):
    if isinstance(val, str):
        dt = parse_dt(val)
    else:
        dt = val
    return dt.isoformat()


def rfc822format(config):
    def flt(val):
        if isinstance(val, str):
            dt = parse_dt(val)
        else:
            dt = val
        return dt.strftime(f"%a, %d %b %Y %H:%M:%S {config.timezone}")

    return flt


def sorted_pages(pages, key=None, reverse=False):
    if key in {"date", "lastmod"}:
        return sorted(pages, key=_date_sorting(key), reverse=reverse)
    return sorted(pages, reverse=reverse)


def pagetype(pages, *filetypes):
    for page in pages:
        if page.output and any(page.output.type == ft for ft in filetypes):
            yield page


def update_env(env, config):
    globals = {"sorted_pages": sorted_pages, "slugify": slugify}
    filters = {
        "slugify": slugify,
        "strftime": strftime,
        "isoformat": isoformat,
        "rfc822format": rfc822format(config),
        "pagetype": pagetype,
    }

    env.globals.update(globals)
    env.filters.update(filters)
