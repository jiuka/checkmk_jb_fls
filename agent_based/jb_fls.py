#!/usr/bin/python
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


import datetime
from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Result,
    Service,
    State,
)


def parse_jb_fls(string_table):
    parsed = {'connection': []}
    for line in string_table:
        if line[0] == 'connection':
            parsed['connection'].append(line[1:])
        else:
            parsed[line[0]] = line[1]
    return parsed


register.agent_section(
    name='jb_fls',
    parse_function=parse_jb_fls,
)


def discovery_jb_fls(section):
    if 'serverUID' in section:
        yield Service()


def check_jb_fls(params, section):
    Result(state=State.OK, summary='Server: %s %s' % (section.get('serverUID', 'Unknown'), section.get('url')))

    if section.get('health', 500) != '200':
        Result(state=State.WARN, summary='Not healthy %s' % section.get('health', 'Unknown'))

    Result(state=State.OK, summary='Version: %s' % section.get('currentVersion', 'Unknown'))
    if section.get('updateAvailable', 'False') != 'False' and params.get('updateAvailable', 1):
        updateAvailableStatus = State(params.get('updateAvailable', 1))
        Result(state=updateAvailableStatus, summary='update available')

    for line in section.get('connection', []):
        state = State.OK if line[1] == 'OK' else State.CRIT
        Result(state=state, notice='Connection to %s is %s' % line)

    now = datetime.datetime.now()
    lastCallHome = datetime.datetime.strptime(section['lastCallHome'], '%d %b %Y %H:%M')
    age = (now - lastCallHome).total_seconds()
    yield from check_levels(
        value=age,
        metric_name='age',
        levels_lower=params.get('lastCallHome', None),
        label='Last call home',
        render_func=render.timespan,
    )


register.check_plugin(
    name='jb_fls',
    service_name='JB FLS',
    discovery_function=discovery_jb_fls,
    check_function=check_jb_fls,
    check_ruleset_name='jb_fls',
    check_default_parameters={
        'lastCallHome': (4500, 7200),
        'updateAvailable': 'W',
    },
)
