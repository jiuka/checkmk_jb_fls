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
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    DropdownChoice,
    TextAscii,
    Tuple,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _vs_jb_fls():
    return Dictionary(
        title=_('JetBrains Floating License Server'),
        elements=[
            (
                'updateAvailable',
                DropdownChoice(
                    title=_('Update Available'),
                    choices=[
                        (2, _('CRIT')),
                        (1, _('WARN')),
                        (0, _('OK')),
                        (None, _('IGNORE')),
                    ],
                    default_value='1',
                )
            ),
            (
                'lastCallHome',
                Tuple(
                    title=_('Maximal time since last call home'),
                    elements=[
                        Age(title=_('Warning if older than')),
                        Age(title=_('Critical if older than')),
                    ],
                )
            ),
        ]
    )


def _item_spec_jb_fls():
    return TextAscii(
        title=_('UID of the JetBrains Floating License Server'),
        allow_empty=False,
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='jb_fls',
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_jb_fls,
        parameter_valuespec=_vs_jb_fls,
        title=lambda: _('JetBrains FLS check parameter'),
    )
)
