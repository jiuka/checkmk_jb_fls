#!/usr/bin/env python3
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

from typing import Optional, Sequence
import requests
import logging
from functools import cached_property

from cmk.special_agents.v0_unstable.agent_common import (
    SectionWriter,
    special_agent_main,
)
from cmk.special_agents.v0_unstable.argument_parsing import Args, create_default_argument_parser

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGING = logging.getLogger('agent_jb_fls')


class AgentJbFls:
    '''Checkmk special Agent for JetBrains Floating License Server'''

    def run(self):
        return special_agent_main(self.parse_arguments, self.main)

    def parse_arguments(self, argv: Optional[Sequence[str]]) -> Args:
        parser = create_default_argument_parser(description=self.__doc__)

        parser.add_argument('-U', '--url',
                            dest='url',
                            required=True,
                            help='URL of the FLS server. (Example http://host:1212)')
        parser.add_argument('-T', '--token',
                            dest='token',
                            required=False,
                            help='FLS reporting token.')
        parser.add_argument('-t', '--timeout',
                            dest='timeout',
                            required=False,
                            default=10,
                            help='HTTP connection timeout. (Default: 10)')

        return parser.parse_args(argv)

    def main(self, args: Args):
        self.args = args

        self.report_fls()
        if self.args.token:
            self.report_licenses()

    def report_fls(self):
        with SectionWriter('jb_fls', separator='\t') as writer:
            # URL
            writer.append(f"url\t{self.args.url}")

            # Check Health
            writer.append(f"health\t{self._health['status_code']}")
            for key, value in self._health.items():
                if key == 'status_code':
                    continue
                writer.append(f"{key}\t{value}")

            # Check Connection
            for line in self._check_connection.splitlines():
                if not line:
                    continue
                writer.append(f"connection\t{line}")

            # Check Version
            for key, value in self._check_version.items():
                if key == 'status_code':
                    continue
                writer.append(f"{key}\t{value}")

    def report_licenses(self):
        with SectionWriter('jb_fls_licenses', separator='\t') as writer:
            for license in self._licenses_report['licenses']:
                writer.append(f"{license['name']}\t{license['available']}\t{license['allocated']}")

    @cached_property
    def _check_version(self):
        return self._get('check-version')

    @cached_property
    def _health(self):
        return self._get('health')

    @cached_property
    def _check_connection(self):
        return self._get('check-connection')

    @cached_property
    def _licenses_report(self):
        return self._get(f'licenses-report.json?token={self.args.token}')

    @cached_property
    def _connection(self):
        conn = requests.Session()
        return conn

    def _get(self, url, payload=None, **kwargs) -> requests.Response:
        full_url = '%s/%s' % (self.args.url.strip('/'), url.rstrip('/'))
        LOGGING.debug(f'>> GET {full_url}')
        resp = self._connection.get(full_url, json=payload, timeout=self.args.timeout, **kwargs)
        LOGGING.debug(f'<< {resp.status_code} {resp.reason}')
        try:
            json = resp.json()
            json['status_code'] = resp.status_code
            return json
        except Exception:
            return resp.text
