import json
import requests
import typer
import os
from .auth import host, getConfigFromFile, BearerAuth
from typing import Optional

state = {
    'accessToken': None,
    'providerId': None
}

app = typer.Typer()

def getCids(download = False):
    query = {
        download: download
    }

    response = requests.get(host + '/cid/blocked', params=query, auth=BearerAuth(state['accessToken']))

    if download:
        return response.content

    cids = response.json()

    return cids

@app.command()
def list(
    outputFile: str = typer.Option(None, "--outputfile", "-o")
):
    if outputFile:
        cids = getCids(True)
        open(outputFile, 'wb').write(cids)
        raise typer.Exit("CID list written at: " + outputFile)

    cids = getCids(False)

    print("Found " + str(len(cids)) + " blocked CIDs:")

    for cid in cids:
        typer.secho(cid)

@app.callback()
def getAuthData():
    state['accessToken'] = getConfigFromFile('access_token')
    state['providerId'] = getConfigFromFile('provider_id')

    if state['accessToken'] is None or state['providerId'] is None:
        raise typer.Exit("Not logged in.")

if __name__ == "__main__":
    app()
