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


register_rule("datasource_programs",
    "special_agents:jb_fls",
     Dictionary(
        title = _("Check state of a JetBrains Floating License Server"),
        help = _("This rule selects the JetBrains Floating License agent"),
        elements = [
            ( "url",
              HTTPUrl(
                  title = _("URL of the JetBrains Floating License Server, e.g. https://host:1212/"),
                  allow_empty = False,
              )
            ),
            ( "token",
              TextAscii(
                  title = _("Report Token"),
                  allow_empty = True,
              )
            ),
        ],
        optional_keys = [ 'token' ],
    ),
    factory_default = watolib.Rulespec.FACTORY_DEFAULT_UNUSED, # No default, do not use setting if no rule matches
    match = 'first')
