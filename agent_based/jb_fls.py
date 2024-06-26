#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# jb_fls - JetBrains Floatingcheck
#
# Copyright (C) 2020-2024  Marius Rieder <marius.rieder@durchmesser.ch>
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


import datetime
from collections.abc import Mapping

from cmk.agent_based.v1 import check_levels
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    render,
    Result,
    Service,
    State,
    StringTable,
)


_Section = Mapping[str, str | tuple[str, str]]


def parse_jb_fls(string_table: StringTable) -> _Section:
    parsed = {'connection': []}
    for line in string_table:
        if line[0] == 'connection':
            parsed['connection'].append(tuple(line[1:]))
        else:
            parsed[line[0]] = line[1]
    return parsed


agent_section_jb_fls = AgentSection(
    name="jb_fls",
    parse_function=parse_jb_fls,
)


def discovery_jb_fls(section: _Section) -> DiscoveryResult:
    if 'serverUID' in section:
        yield Service()


def check_jb_fls(params, section: _Section) -> CheckResult:
    if 'serverUID' not in section:
        yield Result(state=State.UNKNOWN, summary='Server: %s not found' % (section.get('url')))
        return

    yield Result(state=State.OK, summary='Server: %s %s ' % (section.get('serverUID', 'Unknown'), section.get('url')))

    if section.get('health', 500) != '200':
        yield Result(state=State.WARN, summary='Not healthy %s' % section.get('health', 'Unknown'))

    yield Result(state=State.OK, summary='Version: %s' % section.get('currentVersion', 'Unknown'))
    if section.get('updateAvailable', 'False') != 'False' and params.get('updateAvailable', 1) is not None:
        updateAvailableStatus = State(params.get('updateAvailable', 1))
        yield Result(state=updateAvailableStatus, summary='update available to %s' % section.get('latestVersion', 'Unknown'))

    for line in section.get('connection', []):
        state = State.OK if line[1] == 'OK' else State.CRIT
        yield Result(state=state, notice='Connection to %s is %s' % line)

    now = datetime.datetime.now()
    lastCallHome = datetime.datetime.strptime(section['lastCallHome'], '%d %b %Y %H:%M')
    age = (now - lastCallHome).total_seconds()

    yield from check_levels(
        value=age,
        metric_name='age',
        levels_upper=params.get('lastCallHome', None),
        label='Last call home',
        render_func=render.timespan,
    )


check_plugin_jb_fls = CheckPlugin(
    name='jb_fls',
    service_name='JB FLS',
    discovery_function=discovery_jb_fls,
    check_function=check_jb_fls,
    check_ruleset_name='jb_fls',
    check_default_parameters={
        'lastCallHome': (4500, 7200),
        'updateAvailable': 1,
    },
)
