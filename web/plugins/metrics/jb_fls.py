#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2020  Marius Rieder <marius.rieder@durchmesser.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


from cmk.gui.plugins.metrics import (
    check_metrics,
    metric_info,
    graph_info,
)


check_metrics['check_mk-jb_fls_licenses'] = {
    'licenses': {
        'name': 'jb_licenses'
    },
}

metric_info["jb_licenses"] = {
    "title": _("Used licenses"),
    "unit": "count",
    "color": "#ff6234",
}

graph_info["jb_fls_licenses"] = {
    "title": _("JetBrains licenses"),
    "metrics": [
        ("jb_licenses", "area"),
    ],
    "scalars": [
        "jb_licenses:warn",
        "jb_licenses:crit",
        ("jb_licenses:max#000000", "Installed licenses"),
    ],
    "range": (0, "jb_licenses:max"),
}
