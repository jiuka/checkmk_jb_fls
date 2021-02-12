#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# jb_fls - JetBrains Floatingcheck
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
from cmk.base.plugins.agent_based import jb_fls


@pytest.mark.parametrize('string_table, result', [
    (
        [], {'connection': []}
    ),
    (
        [['serverUID', 'foobar']],
        {'serverUID': 'foobar', 'connection': []}
    ),
    (
        [['connection', 'foo', 'bar'], ['connection', 'alice', 'bob']],
        {'connection': [('foo', 'bar'), ('alice', 'bob')]}
    ),
])
def test_parse_jb_fls(string_table, result):
    assert jb_fls.parse_jb_fls(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({'foo': 'bar'}, []),
    ({'serverUID': 'foobar'}, [Service()]),
])
def test_discovery_jb_fls(section, result):
    assert list(jb_fls.discovery_jb_fls(section)) == result


@pytest.mark.freeze_time('2021-02-11 14:55')
@pytest.mark.parametrize('params, section, result', [
    (
        {},
        {
            'serverUID': 'fooBar',
            'url': 'https://host:1212/',
            'health': '200',
            'currentVersion': '1.2.3',
            'updateAvailable': 'False',
            'connection': [
                ('https://account.jetbrains.com', 'OK')
            ],
            'lastCallHome': '11 Feb 2021 14:34'
        },
        [
            Result(state=State.OK, summary='Server: fooBar https://host:1212/ '),
            Result(state=State.OK, summary='Version: 1.2.3'),
            Result(state=State.OK, notice='Connection to https://account.jetbrains.com is OK'),
            Result(state=State.OK, summary='Last call home: 21 minutes 0 seconds'),
            Metric('age', 1260),
        ]
    ),
    (
        {},
        {
            'serverUID': 'fooBar',
            'url': 'https://host:1212/',
            'health': '200',
            'currentVersion': '1.2.3',
            'latestVersion': '1.2.4',
            'updateAvailable': 'True',
            'connection': [
                ('https://account.jetbrains.com', 'OK')
            ],
            'lastCallHome': '11 Feb 2021 14:34'
        },
        [
            Result(state=State.OK, summary='Server: fooBar https://host:1212/ '),
            Result(state=State.OK, summary='Version: 1.2.3'),
            Result(state=State.WARN, summary='update available'),
            Result(state=State.OK, notice='Connection to https://account.jetbrains.com is OK'),
            Result(state=State.OK, summary='Last call home: 21 minutes 0 seconds'),
            Metric('age', 1260),
        ]
    ),
    (
        {'updateAvailable': None},
        {
            'serverUID': 'fooBar',
            'url': 'https://host:1212/',
            'health': '200',
            'currentVersion': '1.2.3',
            'latestVersion': '1.2.4',
            'updateAvailable': 'True',
            'connection': [
                ('https://account.jetbrains.com', 'OK')
            ],
            'lastCallHome': '11 Feb 2021 14:34'
        },
        [
            Result(state=State.OK, summary='Server: fooBar https://host:1212/ '),
            Result(state=State.OK, summary='Version: 1.2.3'),
            Result(state=State.OK, notice='Connection to https://account.jetbrains.com is OK'),
            Result(state=State.OK, summary='Last call home: 21 minutes 0 seconds'),
            Metric('age', 1260),
        ]
    ),
    (
        {'lastCallHome': (1800, 900)},
        {
            'serverUID': 'fooBar',
            'url': 'https://host:1212/',
            'health': '200',
            'currentVersion': '1.2.3',
            'updateAvailable': 'False',
            'connection': [
                ('https://account.jetbrains.com', 'OK')
            ],
            'lastCallHome': '11 Feb 2021 14:34'
        },
        [
            Result(state=State.OK, summary='Server: fooBar https://host:1212/ '),
            Result(state=State.OK, summary='Version: 1.2.3'),
            Result(state=State.OK, notice='Connection to https://account.jetbrains.com is OK'),
            Result(state=State.CRIT, summary='Last call home: 21 minutes 0 seconds (warn/crit at 30 minutes 0 seconds/15 minutes 0 seconds)'),
            Metric('age', 1260, levels=(1800.0, 900.0)),
        ]
    ),
])
def test_check_jb_fls(params, section, result):
    assert list(jb_fls.check_jb_fls(params, section)) == result
