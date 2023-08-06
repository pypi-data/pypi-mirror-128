# BitScreen CLI

## Installation
```console
pip install bitscreen-cli
```

## First steps
Before starting to interact with BitScreen, you should first log in. You can do this two ways:

### Using a private key
To obtain your private key from Metamask, you can check out [this](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key) tutorial.
```console
$ bitscreen-cli auth login
What's you Ethereum wallet address?: <your wallet address>
What's your private key?: <your private key>
```

### Using a mnemonic/seed phrase
To obtain your seed phrase from Metamask, you can check out [this](https://metamask.zendesk.com/hc/en-us/articles/360015290032-How-to-reveal-your-Secret-Recovery-Phrase) tutorial.
```console
$ bitscreen-cli auth login --from-seed
Please provide your seed phrase: <your seed phrase>
```

No matter which one of there two methods you pick, you will be asked if you want these credentials to be saved (locally) for future logins. These credentials are never leaving your machine through BitScreen CLI, they are only used to sign messages locally.

## Documentation
**Usage**:

```console
$ bitscreen-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `auth`
* `cid`
* `dashboard`
* `directory`
* `filter`
* `settings`
* `setup`

## `bitscreen-cli auth`

**Usage**:

```console
$ bitscreen-cli auth [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `login`
* `logout`
* `register`

### `bitscreen-cli auth login`

**Usage**:

```console
$ bitscreen-cli auth login [OPTIONS]
```

**Options**:

* `--fromseed / --no-fromseed`: [default: False]
* `--help`: Show this message and exit.

### `bitscreen-cli auth logout`

**Usage**:

```console
$ bitscreen-cli auth logout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli auth register`

**Usage**:

```console
$ bitscreen-cli auth register [OPTIONS] WALLET
```

**Arguments**:

* `WALLET`: [required]

**Options**:

* `--help`: Show this message and exit.

## `bitscreen-cli setup`

**Usage**:

```console
$ bitscreen-cli setup [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `install`

### `bitscreen-cli setup install`

**Usage**:

```console
$ bitscreen-cli setup install
```

## `bitscreen-cli cid`

**Usage**:

```console
$ bitscreen-cli cid [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`

### `bitscreen-cli cid list`

**Usage**:

```console
$ bitscreen-cli cid list [OPTIONS]
```

**Options**:

* `-o, --outputfile TEXT`
* `--help`: Show this message and exit.

## `bitscreen-cli dashboard`

**Usage**:

```console
$ bitscreen-cli dashboard [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `show`

### `bitscreen-cli dashboard show`

**Usage**:

```console
$ bitscreen-cli dashboard show [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `bitscreen-cli directory`

**Usage**:

```console
$ bitscreen-cli directory [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `details`
* `discard`
* `import`
* `list`

### `bitscreen-cli directory details`

**Usage**:

```console
$ bitscreen-cli directory details [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli directory discard`

**Usage**:

```console
$ bitscreen-cli directory discard [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli directory import`

**Usage**:

```console
$ bitscreen-cli directory import [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli directory list`

**Usage**:

```console
$ bitscreen-cli directory list [OPTIONS]
```

**Options**:

* `--search TEXT`: [default: ]
* `--help`: Show this message and exit.

## `bitscreen-cli filter`

**Usage**:

```console
$ bitscreen-cli filter [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`
* `add-cid`
* `delete`
* `details`
* `disable`
* `edit`
* `enable`
* `list`
* `remove-cid`

### `bitscreen-cli filter add`

**Usage**:

```console
$ bitscreen-cli filter add [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--description TEXT`: [required]
* `--visibility TEXT`: [required]
* `--override INTEGER`: [required]
* `--help`: Show this message and exit.

### `bitscreen-cli filter add-cid`

**Usage**:

```console
$ bitscreen-cli filter add-cid [OPTIONS] FILTER CID
```

**Arguments**:

* `FILTER`: [required]
* `CID`: [required]

**Options**:

* `--refurl TEXT`: [default: ]
* `--help`: Show this message and exit.

### `bitscreen-cli filter delete`

**Usage**:

```console
$ bitscreen-cli filter delete [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--confirm / --no-confirm`: [default: False]
* `--help`: Show this message and exit.

### `bitscreen-cli filter details`

**Usage**:

```console
$ bitscreen-cli filter details [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli filter disable`

**Usage**:

```console
$ bitscreen-cli filter disable [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli filter edit`

**Usage**:

```console
$ bitscreen-cli filter edit [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--name TEXT`
* `--description TEXT`
* `--override INTEGER`
* `--visibility TEXT`
* `--help`: Show this message and exit.

### `bitscreen-cli filter enable`

**Usage**:

```console
$ bitscreen-cli filter enable [OPTIONS] FILTER
```

**Arguments**:

* `FILTER`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli filter list`

**Usage**:

```console
$ bitscreen-cli filter list [OPTIONS]
```

**Options**:

* `--search TEXT`: [default: ]
* `--help`: Show this message and exit.

### `bitscreen-cli filter remove-cid`

**Usage**:

```console
$ bitscreen-cli filter remove-cid [OPTIONS] FILTER CID
```

**Arguments**:

* `FILTER`: [required]
* `CID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `bitscreen-cli settings`

**Usage**:

```console
$ bitscreen-cli settings [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `disable`
* `enable`
* `get`
* `set`

### `bitscreen-cli settings disable`

**Usage**:

```console
$ bitscreen-cli settings disable [OPTIONS] ACTION:[filtering|sharing|importing]
```

**Arguments**:

* `ACTION:[filtering|sharing|importing]`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli settings enable`

**Usage**:

```console
$ bitscreen-cli settings enable [OPTIONS] ACTION:[filtering|sharing|importing]
```

**Arguments**:

* `ACTION:[filtering|sharing|importing]`: [required]

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli settings get`

**Usage**:

```console
$ bitscreen-cli settings get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `bitscreen-cli settings set`

**Usage**:

```console
$ bitscreen-cli settings set [OPTIONS] KEY:[country|name|website|email|contact-person|address] VALUE
```

**Arguments**:

* `KEY:[country|name|website|email|contact-person|address]`: [required]
* `VALUE`: [required]

**Options**:

* `--help`: Show this message and exit.
