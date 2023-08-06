
# WHATAJOKE

A python package that sends jokes to your friends!


## Precondition    

Must be installed:
- Chrome
- Python

## Installation

Install whatajoke using source code

```bash
  git clone https://github.com/joaoduartepinto/whatajoke.git
  cd whatajoke/
  python setup.py install
```

~Install whatajoke with pip~ [TBD]

```bash
  pip install whatajoke
```

## Usage

```bash
    wj <command> <flag>
```

### Flow of Use

First log into Whatapp. This will open the browser in the whatapp page to you scan the QR with your mobile Whatapp app.

```bash
    wj login
```

Then you can start to send jokes (You will need to pass the friend or group name).

```bash
    wj send --group <friend>
```
## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)


## Authors

- [@joaoduartepinto](https://www.github.com/joaoduartepinto)


