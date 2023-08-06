#!/usr/bin/env python

import json
import requests
import typer
import os

from .commands import auth, filter, directory, dashboard, settings, cid, setup

app = typer.Typer()

app.add_typer(auth.app, name="auth")
app.add_typer(filter.app, name="filter")
app.add_typer(directory.app, name="directory")
app.add_typer(dashboard.app, name="dashboard")
app.add_typer(settings.app, name="settings")
app.add_typer(cid.app, name="cid")
app.add_typer(setup.app, name="setup")
