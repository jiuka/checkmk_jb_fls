#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# jb_fls_licenses - JetBrains Floating Licenses check
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


from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    Result,
    Service,
    State,
)


def parse_jb_fls_licenses(string_table):
    parsed = {}
    for line in string_table:
        available = int(line[1])
        allocated = int(line[2])
        parsed[line[0]] = (available + allocated, allocated)
    return parsed


agent_section_jb_fls_licenses = AgentSection(
    name="jb_fls_licenses",
    parse_function=parse_jb_fls_licenses,
)


def discovery_jb_fls_licenses(section):
    for license_type in section:
        yield Service(item=license_type)


def check_jb_fls_licenses(item, params, section):
    if item not in section:
        return

    license_total, license_used = section.get(item)

    match params.get('licenses'):
        case ('crit_on_all', _):
            levels = ('fixed', (license_total, license_total))
        case ('absolute', {'warn': warn, 'crit': crit}):
            levels = ('fixed', (license_total - warn, license_total - crit))
        case ('percentage', {'warn': warn, 'crit': crit}):
            levels = ('fixed', (int(license_total * (100 - warn) / 100), int(license_total * (100 - crit) / 100)))
        case _:
            levels = ('no_levels', None)

    yield Result(state=State.OK, summary=f"Licenses available: {license_total}")
    yield from check_levels(license_used,
                            label="used",
                            render_func=lambda v: f"{v:d}",
                            levels_upper=levels,
                            metric_name='licenses',
                            boundaries=(0, int(license_total)))


check_plugin_jb_fls = CheckPlugin(
    name='jb_fls_licenses',
    service_name='JB Licenses %s',
    discovery_function=discovery_jb_fls_licenses,
    check_function=check_jb_fls_licenses,
    check_ruleset_name='jb_fls_licenses',
    check_default_parameters={'licenses': ('crit_on_all', True)},
)
