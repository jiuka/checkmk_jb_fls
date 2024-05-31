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

from cmk.rulesets.v1 import Help, Title, Label, Message
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice, CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    InputHint,
    Integer,
    LevelDirection,
    migrate_to_float_simple_levels,
    Percentage,
    ServiceState,
    SimpleLevels,
    TimeSpan,
    TimeMagnitude,
    validators,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition


def _parameter_form_jb_fls():
    return Dictionary(
        elements={
            'updateAvailable': DictElement(
                parameter_form=ServiceState(
                    title=Title('Update Available'),
                    help_text=Help('State if updates are available'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            "lastCallHome": DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Maximal time since last call home'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE]
                    ),
                    migrate=migrate_to_float_simple_levels,
                    prefill_fixed_levels=InputHint(value=(86400 * 1, 86400 * 2)),
                ),
                required=False,
            ),
        }
    )


rule_spec_jb_fls = CheckParameters(
    name='jb_fls',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_jb_fls,
    title=Title('JetBrains FLS check parameter'),
    condition=HostAndItemCondition(
        item_title=Title('UID of the JetBrains Floating License Server'),
    ),
)


def crit_lower_then_warn(value):
    if value['crit'] >= value['warn']:
        raise validators.ValidationError(Message("The critical level needs to be less or equal then the warning."))


def migrate_to_level_dict(value):
    if isinstance(value, tuple):
        return dict(warn=value[0], crit=value[1])
    return value


def _parameter_form_jb_fls_licenses():
    return Dictionary(
        title=Title('JetBrains Floating License Server'),
        elements={
            'licenses': DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Levels for Number of Licenses"),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="absolute",
                            title=Title('Absolute levels for unused licenses'),
                            parameter_form=Dictionary(
                                elements={
                                    "warn": DictElement(
                                        parameter_form=Integer(
                                            label=Label('Warning below'),
                                            unit_symbol='unused license',
                                            prefill=InputHint(5),
                                        ),
                                        required=True,
                                    ),
                                    "crit": DictElement(
                                        parameter_form=Integer(
                                            label=Label('Critical below'),
                                            unit_symbol='unused license',
                                            prefill=InputHint(0),
                                        ),
                                        required=True,
                                    )
                                },
                                custom_validate=[
                                    crit_lower_then_warn
                                ],
                                migrate=migrate_to_level_dict,
                            )
                        ),
                        CascadingSingleChoiceElement(
                            name="percentage",
                            title=Title('Percentual levels for unused licenses'),
                            parameter_form=Dictionary(
                                elements={
                                    "warn": DictElement(
                                        parameter_form=Percentage(
                                            label=Label('Warning below'),
                                            prefill=InputHint(10.0),
                                        ),
                                        required=True,
                                    ),
                                    "crit": DictElement(
                                        parameter_form=Percentage(
                                            label=Label('Critical below'),
                                            prefill=InputHint(0.0),
                                        ),
                                        required=True,
                                    )
                                },
                                custom_validate=[
                                    crit_lower_then_warn
                                ],
                                migrate=migrate_to_level_dict,
                            )
                        ),
                        CascadingSingleChoiceElement(
                            name='always_ok',
                            title=Title('Always be OK'),
                            parameter_form=FixedValue(value=False),
                        ),
                        CascadingSingleChoiceElement(
                            name='crit_on_all',
                            title=Title('Go critical if all licenses are used'),
                            parameter_form=FixedValue(value=None),
                        ),
                    ],
                    prefill='crit_on_all',
                ),
                required=True,
            ),
        }
    )


rule_spec_jb_fls_licenses = CheckParameters(
    name='jb_fls_licenses',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_jb_fls_licenses,
    title=Title('Number of used JetBrains Floating licenses'),
    condition=HostAndItemCondition(item_title=Title('Name of the JetBrains license, e.g. <tt>IntelliJ IDEA Ultimate 12.0</tt>')),
)
