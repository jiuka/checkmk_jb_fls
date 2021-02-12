#!/usr/bin/env python3
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

import pytest  # type: ignore[import]
import requests  # noqa: F401

from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

spec = spec_from_loader("agent_jb_fls", SourceFileLoader("agent_jb_fls", "agents/special/agent_jb_fls"))
agent_jb_fls = module_from_spec(spec)
spec.loader.exec_module(agent_jb_fls)


@pytest.fixture
def fls_mock(requests_mock):
    requests_mock.register_uri('GET', 'http://jbfls:1212/check-version', text='{"currentVersion":"123","latestVersion":"124","updateAvailable":true}')
    requests_mock.register_uri('GET', 'http://jbfls:1212/health', text='{"serverUID":"1a2b3c4d5f","lastCallHome":"12 Feb 2021 07:34"}')
    requests_mock.register_uri('GET', 'http://jbfls:1212/check-connection', text='''
https://account.jetbrains.com	OK
https://www.jetbrains.com	OK
''')
    requests_mock.register_uri('GET', 'http://jbfls:1212/licenses-report.json?token=foo', text='''
{
    "licenses": [
        {
            "name": "IntelliJ IDEA Ultimate 12.0",
            "available": 1,
            "allocated": 0,
            "allocatedDetails": "/tickets/II?version=12000&trueUp=false"
        },
        {
            "name": "IntelliJ IDEA Ultimate 2016.2",
            "available": 1,
            "allocated": 0,
            "allocatedDetails": "/tickets/II?version=2016200&trueUp=false"
        }
    ]
}
''')


class Args:
    url = 'http://jbfls:1212/'
    token = None
    debug = True
    timeout = 10


def test_AgentJbFls_main(capsys, fls_mock):
    agent = agent_jb_fls.AgentJbFls()
    agent.main(Args())

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.splitlines() == [
        '<<<check_mk>>>',
        'AgentOS: JetBrains FLS',
        'Version: 123',
        '<<<jb_fls:sep(9)>>>',
        'url\thttp://jbfls:1212/',
        'health\t200',
        'serverUID\t1a2b3c4d5f',
        'lastCallHome\t12 Feb 2021 07:34',
        'connection\thttps://account.jetbrains.com\tOK',
        'connection\thttps://www.jetbrains.com\tOK',
        'currentVersion\t123',
        'latestVersion\t124',
        'updateAvailable\tTrue',
    ]


def test_AgentJbFls_main_w_token(capsys, fls_mock):
    agent = agent_jb_fls.AgentJbFls()
    args = Args()
    args.token = 'foo'
    agent.main(args)

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.splitlines() == [
        '<<<check_mk>>>',
        'AgentOS: JetBrains FLS',
        'Version: 123',
        '<<<jb_fls:sep(9)>>>',
        'url\thttp://jbfls:1212/',
        'health\t200',
        'serverUID\t1a2b3c4d5f',
        'lastCallHome\t12 Feb 2021 07:34',
        'connection\thttps://account.jetbrains.com\tOK',
        'connection\thttps://www.jetbrains.com\tOK',
        'currentVersion\t123',
        'latestVersion\t124',
        'updateAvailable\tTrue',
        '<<<jb_fls_licenses:sep(9)>>>',
        'IntelliJ IDEA Ultimate 12.0\t1\t0',
        'IntelliJ IDEA Ultimate 2016.2\t1\t0',
    ]
