# Notes for Environment Configuration


## Checklist

* prepare `.vscode` directory
  - add `extensions.json`, `settings.json`, `launch.json`
* start dev container
* create README.md
* prepare .gitignore
  - add `.DS_Store`, `.libs`, ...
* initialize git
* install extensions
* initialize pipenv and update `settings.json` with venv info
* create minimal script: https://www.python-boilerplate.com/py3+executable+gitignore+argparse+logging+pytest
* create package directory tree: https://realpython.com/python-application-layouts/
* create `tests` directory and prepare unit tests


## Settings

In the `.vscode/settings.json` add the following and change directory of venv

```
{
    "python.terminal.activateEnvironment": false,
    "python.testing.pytestArgs": [
        "tests/"
    ],
    "python.experiments.optInto": ["All"],

    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath": "/home/vscode/.local/share/virtualenvs/CBDC_scraper-YINk9gpH/bin/pytest",
    "python.pipenvPath": "/home/vscode/.local/share/virtualenvs/CBDC_scraper-YINk9gpH/bin/python",

    "python.linting.pylintPath": "/home/vscode/.local/share/virtualenvs/CBDC_scraper-YINk9gpH/bin/python",
    "python.autoComplete.extraPaths": ["/home/vscode/.local/share/virtualenvs/CBDC_scraper-YINk9gpH/bin/python"],
    "python.defaultInterpreterPath": "/home/vscode/.local/share/virtualenvs/CBDC_scraper-YINk9gpH/bin/python",
    "python.analysis.extraPaths": [
        "/home/vscode/.local/share/virtualenvs/CBDC_scraper-YINk9gpH/"
    ],
    "files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/*.pyc": true,
        "**/__pycache__": true
    }
}
```



## Extensions


List all extensions with: `code --list-extensions | xargs -L 1 echo code --install-extension`

Add these to `.vscode/extensions.json` to automatically be recommended in dev container, like such:

```
{
    "recommendations": [
        "GrapeCity.gc-excelviewer",
        "Gruntfuggly.todo-tree",
        "uctakeoff.vscode-counter"
    ]
}
```


## Python Packages

A basic `requirements.txt` file would include the following packages.  This can be obtained with: `pipenv run pip freeze > requirements.txt` if all packages are installed.  Otherwise, it is preferable to get them directly from the `Pipfile.lock`.

```
logzero
pytest
pytest-cov
```



## Testing

### VSCode

Testing can be done in VSCode using two methods: Debugger and Testing.  Debugger can be setup to run your program similar to the following:

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "scraper",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/cbdc_scraper/scraper.py",
            "args": [],
            "console": "integratedTerminal"
        },
    ]
}
```

### Commandline

Basic testing can be performed using `pytest`.

Command line testing of a specific test method can be performed using:  `pytest --trace tests/test_scraper.py -k test_get_data_atlantic`.

Use the following commands:

* n(next) – step to the next line within the same function
* s(step) – step to the next line in this function or called function
* b(break) – set up new breakpoints without changing the code
* p(print) – evaluate and print the value of an expression
* c(continue) – continue execution and only stop when a breakpoint is encountered
* unt(until) – continue execution until the line with a number greater than the current one is reached
* q(quit) – quit the debugger/execution


### Test Coverage

Run `pytest --cov=main_module --cov-report=xml tests`, where coverage is for `main_module` and `xml` is the generated `coverage.xml` report file that can be used with vscode extension `coverage gutters`.



## Binaries

Add binary packages for wrapper modules and additional functionality.

* create `.libs` directory