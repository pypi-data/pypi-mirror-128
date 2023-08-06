import json
import requests
import typer
import os
from .auth import host, getConfigFromFile, BearerAuth
from dashing import *

app = typer.Typer()

state = {
    'accessToken': None,
    'providerId': None
}

@app.command()
def show():
    textColor = 2
    borderColor = 3
    ui = VSplit(
        HSplit(
            Text("Currently Filtering CIDs\n8", color=textColor, border_color=borderColor),
            Text("List subscriberss\n8", color=textColor, border_color=borderColor),
            Text("Deals declined\n8", color=textColor, border_color=borderColor),
        ),
        HSplit(
            Text("Active lists\n8", color=textColor, border_color=borderColor),
            Text("Inactive lists\n8", color=textColor, border_color=borderColor),
            Text("Imported lists\n8", color=textColor, border_color=borderColor),
            Text("Private lists\n8", color=textColor, border_color=borderColor),
            Text("Public lists\n8", color=textColor, border_color=borderColor),
        ),
        HSplit(),
        HSplit()
    )

    ui.display()

@app.callback()
def getAuthData():
    state['accessToken'] = getConfigFromFile('access_token')
    state['providerId'] = getConfigFromFile('provider_id')

    if state['accessToken'] is None or state['providerId'] is None:
        raise typer.Exit("Not logged in.")

if __name__ == "__main__":
    app()
