#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# jb_fls_licenses - JetBrains Floatingcheck
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

import pytest  # type: ignore[import]
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import jb_fls_licenses


@pytest.mark.parametrize('string_table, result', [
    (
        [], {}
    ),
    (
        [
            ['All Products Pack Toolbox', '21', '21'],
            ['CLion Toolbox', '23', '0']
        ],
        {
            'All Products Pack Toolbox': (42, 21),
            'CLion Toolbox': (23, 0)
        }
    ),
])
def test_parse_jb_fls_licenses(string_table, result):
    assert jb_fls_licenses.parse_jb_fls_licenses(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({}, []),
    (
        {
            'All Products Pack Toolbox': (42, 21),
            'CLion Toolbox': (23, 0)
        },
        [
            Service(item='All Products Pack Toolbox'),
            Service(item='CLion Toolbox')
        ]
    ),
])
def test_discovery_jb_fls_licenses(section, result):
    assert list(jb_fls_licenses.discovery_jb_fls_licenses(section)) == result


JB_FLS_LICENSES_SECTION = {
    'All Products Pack Toolbox': (42, 21),
    'CLion Toolbox': (23, 23)
}


@pytest.mark.parametrize('item, params, section, result', [
    (
        'Foo', {},
        JB_FLS_LICENSES_SECTION,
        []
    ),
    (
        'All Products Pack Toolbox', {},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 21.0, levels=(42.0, 42.0), boundaries=(0.0, 42.0)),
            Result(state=State.OK, summary='used 21 out of 42 licenses (warn/crit at 42/42)')
        ]
    ),
    (
        'All Products Pack Toolbox', {'licenses': (5, 0)},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 21.0, levels=(37.0, 42.0), boundaries=(0.0, 42.0)),
            Result(state=State.OK, summary='used 21 out of 42 licenses (warn/crit at 37/42)')
        ]
    ),
    (
        'All Products Pack Toolbox', {'licenses': (30, 0)},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 21.0, levels=(12.0, 42.0), boundaries=(0.0, 42.0)),
            Result(state=State.WARN, summary='used 21 out of 42 licenses (warn/crit at 12/42)')
        ]
    ),
    (
        'All Products Pack Toolbox', {'licenses': (30, 25)},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 21.0, levels=(12.0, 17.0), boundaries=(0.0, 42.0)),
            Result(state=State.CRIT, summary='used 21 out of 42 licenses (warn/crit at 12/17)')
        ]
    ),
    (
        'CLion Toolbox', {},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 23.0, levels=(23.0, 23.0), boundaries=(0.0, 23.0)),
            Result(state=State.CRIT, summary='used 23 out of 23 licenses (warn/crit at 23/23)')
        ]
    ),
    (
        'CLion Toolbox', {'auto-migration-wrapper-key': False},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 23.0, levels=(23.0, 23.0), boundaries=(0.0, 23.0)),
            Result(state=State.CRIT, summary='used 23 out of 23 licenses (warn/crit at 23/23)')
        ]
    ),
    (
        'CLion Toolbox', {'licenses': False},
        JB_FLS_LICENSES_SECTION,
        [
            Metric('licenses', 23.0, boundaries=(0.0, 23.0)),
            Result(state=State.OK, summary='used 23 out of 23 licenses')
        ]
    ),
])
def test_check_jb_fls_licenses(item, params, section, result):
    assert list(jb_fls_licenses.check_jb_fls_licenses(item, params, section)) == result
