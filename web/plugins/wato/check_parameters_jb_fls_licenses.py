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

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.check_parameters.licenses import _vs_license
from cmk.gui.valuespec import Dictionary, TextAscii
from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersApplications,
    CheckParameterRulespecWithItem,
    rulespec_registry,
)


def _vs_jb_fls_licenses():
    return Dictionary(
        title=_('JetBrains Floating License Server'),
        elements=[
            (
                'licenses',
                _vs_license()
            ),
        ],
        required_keys = ['licenses']
    )


def _item_spec_jb_fls_licenses():
    return TextAscii(
        title=_("Name of the JetBrains license, e.g. <tt>IntelliJ IDEA Ultimate 12.0</tt>"),
        allow_empty=False,
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="jb_fls_licenses",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_jb_fls_licenses,
        parameter_valuespec=_vs_jb_fls_licenses,
        title=lambda: _("Number of used JetBrains Floating licenses"),
    ))
