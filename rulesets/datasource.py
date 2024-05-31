#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    migrate_to_password,
    Password,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _form_special_agents_jb_fls() -> Dictionary:
    return Dictionary(
        title=Title("JetBrains Floating License Server"),
        elements = {
            "url": DictElement(
                parameter_form=String(
                    title=Title("URL of the JetBrains Floating License Server, e.g. https://host:1212/"),
                    custom_validate=(
                        validators.Url(
                            [validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS],
                        ),
                    ),
                ),
                required=True,
            ),
            "token": DictElement(
                parameter_form=Password(
                    title=Title("JetBrains Floating License Report Token"),
                    migrate=migrate_to_password
                ),
                required=False,
            ),
        },
    )


rule_spec_jb_lfs_datasource = SpecialAgent(
    name="jb_fls",
    title=Title("JetBrains Floating License Server"),
    topic=Topic.APPLICATIONS,
    parameter_form=_form_special_agents_jb_fls,
)
