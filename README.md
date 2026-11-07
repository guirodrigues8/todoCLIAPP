# To-Do CLI

A simple to-do list app for the terminal, written in Python. Tasks are saved in a local SQLite database, so they are still there the next time you open the app.

## Features

- Add, list, complete and remove tasks from an interactive menu
- Tasks are saved automatically in a SQLite database
- Duplicate detection (ignores upper/lower case, accents and extra spaces)
- Tasks must contain text, not just numbers or symbols
- Type `0` at any prompt to cancel and go back to the menu
- Colored output (completed tasks are green and crossed out, errors are red, etc.)
- No external dependencies, only the Python standard library

## Requirements

- Python 3.8 or newer

Check your version with:

```bash
python3 --version
```

`sqlite3` is included with Python, so there is nothing to install.

## Getting started

Clone the repository and run the app:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python3 app.py
```

On Windows, use `python app.py` (or `py app.py`) instead.

## Usage

When you start the app you get this menu:

```
########################################
# TO-DO LIST
########################################
  1. Add a task
  2. Show tasks
  3. Complete a task
  4. Remove a task
  0. Exit
########################################
Choose an option:
```

| Option | What it does |
| ------ | ------------ |
| `1` | Add a new task |
| `2` | Show all tasks and how many are completed |
| `3` | Mark a task as completed (you choose it by its number) |
| `4` | Remove a task (you choose it by its number) |
| `0` | Exit the app |

## Run it from anywhere (Linux / macOS)

To start the app by typing a single command from any folder, create a link to the script:

```bash
chmod +x app.py
mkdir -p ~/.local/bin
ln -s "$(pwd)/app.py" ~/.local/bin/todoapp
```

Open a new terminal and run:

```bash
todoapp
```

> Make sure the first line of `app.py` is `#!/usr/bin/env python3` and that `~/.local/bin` is in your `PATH`. Don't move `app.py` after creating the link, or run the `ln -sf` command again with the new path.

## Where is my data stored?

Tasks are stored in a SQLite file in your home folder:

```
~/.todo.db
```

Because of this, the app shows the same tasks no matter which folder you run it from.

- **Back up your tasks:** copy the `~/.todo.db` file.
- **Start from scratch:** delete the `~/.todo.db` file. A new empty one is created on the next run.

## Colors

Colors use ANSI escape codes and work in most modern terminals, including Windows 10 and later. To turn them off, set the `NO_COLOR` environment variable:

```bash
NO_COLOR=1 python3 app.py
```

Colors are also disabled automatically when the output is not a terminal (for example, when redirected to a file).

## Project structure

```
.
├── app.py      # the whole application
└── README.md
```