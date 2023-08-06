import json
import requests
import typer
import os
from tabulate import tabulate
from .auth import host, getConfigFromFile, BearerAuth
from .filter import getReadableVisibility

app = typer.Typer()

state = {
    'accessToken': None,
    'providerId': None
}

def getPublicFilters(params = {}):
    params['providerId'] = state['providerId'];

    response = requests.get(host + '/filter/public', params=params, auth=BearerAuth(state['accessToken']))
    filters = response.json()

    return filters['data']

def getPublicFilterDetails(filterId, params = {}):
    params['providerId'] = state['providerId'];

    response = requests.get(host + '/filter/public/details/' + filterId, params=params, auth=BearerAuth(state['accessToken']))

    if response.status_code == 200:
        data = response.json()
        data['filter']['isImported'] = data['isImported']
        data['filter']['provider'] = data['provider']
        return data['filter']

    raise typer.Exit("Filter not found.")

def getStatusFromFilter(filter):
    status = typer.style("Not imported", fg=typer.colors.WHITE, bg=typer.colors.RED)
    if filter['isImported']:
        status = typer.style("Imported", fg=typer.colors.GREEN, bold=True)
    elif filter['provider']['id'] == state['providerId']:
        status = typer.style("Owned", fg=typer.colors.GREEN)

    return status

def printPublicFilterLists(filterList: list):
    headers = ["ID", "Name", "Visibility", "Status", "Subscribers", "CIDs", "Override", "Provider", "Description"]
    rows = [];
    for filter in filterList:
        status = getStatusFromFilter(filter)

        rows.append([
            filter['shareId'],
            filter['name'],
            getReadableVisibility(filter['visibility']),
            status,
            filter['subs'],
            filter['cids'],
            'Yes' if filter['override'] else 'No',
            filter['provider']['businessName'],
            filter['description']
        ])
    print(tabulate(rows, headers, tablefmt="fancy_grid"))

def printPublicFilterDetails(filter):
    typer.echo(getStatusFromFilter(filter))
    typer.secho(f"Filter name:  {filter['name']}")
    typer.secho(f"Description: {filter['description']}")
    typer.secho(f"ID: {filter['shareId']}")
    typer.secho(f"Subscribers: {len(filter['provider_Filters'])}")
    typer.secho(f"Override: {('Yes' if filter['override'] else 'No')}")
    typer.secho(f"CID count: {len(filter['cids'])}")
    typer.secho(f"Business name: {filter['provider']['businessName']}")
    typer.secho(f"Contact person: {filter['provider']['contactPerson']}")
    typer.secho(f"Website: {filter['provider']['website']}")
    typer.secho(f"Email: {filter['provider']['businessName']}")
    typer.secho(f"Address: {filter['provider']['businessName']}")
    typer.secho(f"City & Country: {filter['provider']['businessName']}")

@app.command()
def list(search: str = ""):
    params = {};
    if len(search) > 0:
        params['q'] = search
    filters = getPublicFilters(params)

    typer.secho(f"Found {len(filters)} filters.")
    printPublicFilterLists(filters)

@app.command()
def details(filter: str):
    filter = getPublicFilterDetails(filter)

    printPublicFilterDetails(filter)

@app.command(name="import")
def importFilter(filter: str):
    filter = getPublicFilterDetails(filter)
    if filter['isImported']:
        raise typer.Exit("Filter already imported.")

    if filter['provider']['id'] == state['providerId']:
        raise typer.Exit("Cannot import your own filter.")

    if filter['visibility'] == 1:
        raise typer.Exit("Filter is not public or shareable.")

    providerFilter = {
        'active': True,
        'filterId': filter['id'],
        'providerId': state['providerId']
    }
    response = requests.post(f"{host}/provider-filter", json=providerFilter, auth=BearerAuth(state['accessToken']))
    if response.status_code == 200:
        typer.secho("Imported.", bg=typer.colors.GREEN, fg=typer.colors.BLACK)
    else:
        typer.secho("Error: ", bg=typer.colors.RED)
        typer.secho(response.json())

@app.command(name="discard")
def discardFilter(filter: str):
    filter = getPublicFilterDetails(filter)

    if not filter['isImported']:
        raise typer.Exit("This filter is not imported.")

    response = requests.delete(f"{host}/provider-filter/{state['providerId']}/{filter['id']}", auth=BearerAuth(state['accessToken']))
    if response.status_code == 200:
        typer.secho("Discarded.", bg=typer.colors.GREEN, fg=typer.colors.BLACK)
    else:
        typer.secho("Error: ", bg=typer.colors.RED)
        typer.secho(response.json())

@app.callback()
def getAuthData():
    state['accessToken'] = getConfigFromFile('access_token')
    state['providerId'] = getConfigFromFile('provider_id')

    if state['accessToken'] is None or state['providerId'] is None:
        raise typer.Exit("Not logged in.")

if __name__ == "__main__":
    app()
