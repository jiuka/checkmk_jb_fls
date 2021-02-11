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

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    IndividualOrStoredPassword,
    rulespec_registry,
)
from cmk.gui.valuespec import (
    Dictionary,
    HTTPUrl,
)
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourceProgramsApps


def _valuespec_special_agents_jb_fls():
    return Dictionary(
        title=_("JetBrains Floating License Server"),
        help = _("This rule selects the JetBrains Floating License agent"),
        elements = [
            (
                'url',
                HTTPUrl(
                    title = _("URL of the JetBrains Floating License Server, e.g. https://host:1212/"),
                    allow_empty = False,
                )
            ),
            (
                'token',
                IndividualOrStoredPassword(
                    title = _("JetBrains Floating License Report Token"),
                    allow_empty = True,
                )
            ),
        ],
        optional_keys = ['token'],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsApps,
        name='special_agents:jb_fls',
        valuespec=_valuespec_special_agents_jb_fls,
    ))
