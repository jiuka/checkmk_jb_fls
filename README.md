# Checkmk extension for JetBrains Floating License Server

![build](https://github.com/jiuka/checkmk_jb_fls/workflows/build/badge.svg)

## Description

### Special Agent Plugin

Reports information from the [JetBrains Floating License Server](https://www.jetbrains.com/help/license_server/getting_started.html)

### Check jb_fls

Checks the status of the Floating License Server.

### Check jb_fls_licenses

Reports informations about individual licenses. One check is discoverd for each installed license.

## Development

For the best development experience use [VSCode](https://code.visualstudio.com/) with the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension. This maps your workspace into a checkmk docker container giving you access to the python environment and libraries the installed extension has.

## Directories

The following directories in this repo are getting mapped into the Checkmk site.

* `agents`, `checkman`, `checks`, `doc`, `inventory`, `notifications`, `pnp-templates`, `web` are mapped into `local/share/check_mk/`
* `agent_based` is mapped to `local/lib/check_mk/base/plugins/agent_based`
* `nagios_plugins` is mapped to `local/lib/nagios/plugins`

## Continuous integration
### Local

To build the package hit `Crtl`+`Shift`+`B` to execute the build task in VSCode.

`pytest` can be executed from the terminal or the test ui.

### Github Workflow

The provided Github Workflows run `pytest` and `flake8` in the same checkmk docker conatiner as vscode.