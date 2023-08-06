# 🎈 `st` - a friendly Streamlit CLI

`st` is a CLI that helps you kick-off a new Streamlit project from the command line

## How it works

✨ Simple as:

```bash
$ st .
```

https://user-images.githubusercontent.com/7164864/142880682-e2ac5e67-400e-4eec-bef8-22db7408c9f4.mov


## 🚀 Usage

### Prerequisites

This is a working setup for anyone using Microsoft VS Code.
Has been tested solely on Mac OSX.

#### Manually

1. Install requirements:

```
pip install -r requirements.txt
```

2. Make sure to enable your CLI to access VS Code. See [this link](https://stackoverflow.com/a/40129135/6159698).

3. Add the alias to your `~/.bashrc`:
```
# Alias for st
alias st='python ~/your/path/to/st/st.py -p'
```

4. Source it:
```
source ~/.bash_profile
```

### Getting started

Run:

```
$ st {directory}
```

### Documentation


### Troubleshooting

- If you get `xcrun: error: invalid active developer path`... error:  
Visit https://apple.stackexchange.com/a/254381 or run:
```
xcode-select --install
```
