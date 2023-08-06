import json
import requests
import typer
import os
import subprocess
import re

from .auth import host, getConfigFromFile

app = typer.Typer()

@app.command()
def install():
    typer.secho("Installing BitScreen Plugin.")
    try:
        subprocess.call(["go", "install", "github.com/Murmuration-Labs/bitscreen/cmd/bitscreen@latest"], stdout=subprocess.DEVNULL)
    except OSError as e:
        print(e);
        return;

    typer.secho("Installing BitScreen Updater.")
    try:
        subprocess.call(["pip", "install", "bitscreen-updater"], stdout=subprocess.DEVNULL)
    except OSError as e:
        print(e);
        return;

    privateKey = None
    seedPhrase = None
    autoAuth = typer.confirm("Would you like to authenticate the BitScreen Updater with your CLI credentials?")
    if autoAuth:
        privateKey = getConfigFromFile("eth_private_key")
        if not privateKey:
            typer.secho("Private key not found. Maybe you didn't choose to save it.")
    if not privateKey:
        typer.secho("Proceeding with manual authentication.")
        authMethod = typer.prompt("How would you like to authenticate? [0] -> Private Key [1] -> Seed Phrase")
        if authMethod == "0":
            privateKey = typer.prompt("Please insert your private key: ")
        if authMethod == "1":
            seedPhrase = typer.prompt("Please insert your seed phrase: ")

        if not privateKey and not seedPhrase:
            raise typer.Exit("Invalid option selected")

    typer.secho("Writing environment init script.")
    typer.secho("You can find it at ~/.murmuration/updater_config.sh and execute it before using BitScreen Updater");
    typer.secho("Example: source ~/.murmuration/updater_config.sh")

    fullPath = os.path.expanduser("~/.murmuration/updater_config.sh")
    configDir = os.path.dirname(fullPath)
    if not os.path.exists(configDir):
        os.makedirs(configDir)

    with open(fullPath, "w") as f:
        f.write("export BITSCREEN_SOCKET_PORT=5555\n");
        f.write("export BITSCREEN_BACKEND_HOST=https://bxn.mml.keyko.rocks\n");
        f.write("export BITSCREEN_CIDS_FILE=~/.murmuration/bitscreen\n");
        if privateKey:
            f.write(f"export BITSCREEN_PROVIDER_KEY={privateKey}\n");
        if seedPhrase:
            f.write(f"export BITSCREEN_PROVIDER_SEED_PHRASE={seedPhrase}\n");

    typer.secho("Configuring Lotus Miner to use BitScreen Filter.")
    minerConfigPath = os.getenv('LOTUS_MINER_PATH')
    if len(minerConfigPath) == 0:
        raise typer.Exit("LOTUS_MINER_PATH environment variable not found. Could not configure BitScreen for the Lotus Miner")

    goPath = subprocess.check_output(["go", "env", "GOPATH"]).decode().strip()
    if len(goPath) == 0:
        raise typer.Exit("GOPATH environment variable not found. Could not configure BitScreen for the Lotus Miner")
    goPath += "/bin/bitscreen"

    with open(minerConfigPath + "/config.toml", "r+") as f1:
         contents = f1.read()
         contents = re.sub(r"\s\sFilter\s=\s\".*\"", f"  Filter = \"{goPath}\"", contents)
         contents = re.sub(r"\s\sRetrievalFilter\s=\s\".*\"", f"  RetrievalFilter = \"{goPath}\"", contents)

         f1.seek(0)
         f1.truncate()
         f1.write(contents)

     typer.secho("Done.")

if __name__ == "__main__":
    app()
