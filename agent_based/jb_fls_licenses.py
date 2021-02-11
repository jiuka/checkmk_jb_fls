#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# jb_fls_licenses - JetBrains Floating Licenses check
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

from .agent_based_api.v1 import (
    Metric,
    register,
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


register.agent_section(
    name='jb_fls_licenses',
    parse_function=parse_jb_fls_licenses,
)


def discovery_jb_fls_licenses(section):
    for license_type in section:
        yield Service(item=license_type)


def check_jb_fls_licenses(item, params, section):
    if item not in section:
        print(f'{item} <> {section}')
        return

    license_total, license_used = section.get(item)

    license_params = params.get('licenses', None)

    if license_params is False:
        license_warn = None
        license_crit = None
    elif not license_params:
        license_warn = int(license_total)
        license_crit = int(license_total)
    elif isinstance(license_params[0], int):
        license_warn = max(0, int(license_total) - license_params[0])
        license_crit = max(0, int(license_total) - license_params[1])
    else:
        license_warn = int(license_total) * (1 - license_params[0] / 100.0)
        license_crit = int(license_total) * (1 - license_params[1] / 100.0)

    yield Metric('licenses',
                 int(license_used),
                 levels=(license_warn, license_crit),
                 boundaries=(0, int(license_total)))

    if int(license_used) <= int(license_total):
        infotext = 'used %d out of %d licenses' % (int(license_used), int(license_total))
    else:
        infotext = 'used %d licenses, but you have only %d' % (int(license_used), int(license_total))

    if license_crit is not None and int(license_used) >= license_crit:
        status = State.CRIT
    elif license_warn is not None and int(license_used) >= license_warn:
        status = State.WARN
    else:
        status = State.OK

    if license_crit is not None:
        infotext += ' (warn/crit at %d/%d)' % (license_warn, license_crit)

    yield Result(state=status, summary=infotext)


register.check_plugin(
    name='jb_fls_licenses',
    service_name='JB Licenses %s',
    discovery_function=discovery_jb_fls_licenses,
    check_function=check_jb_fls_licenses,
    check_ruleset_name='jb_fls_licenses',
    check_default_parameters={},
)
