# What is this?
`pooetry` is a python wrapper utility with a very narrow use case.  If you don't know what it does you probably don't need it 🙃

# What does it do?
This utility automagically fixes issues caused by these factors combined:
* `poetry 0.12.*`
* `pip 19.*`
* Use a private package repo which requires authentication
* Have special characters in your credentials for this private repo
    * _commonly caused by having an email as a username (the '@' is not URL legal)_

If you are stuck in this situation you'll find yourself changing the credentials between quoted and non-quoted as _some_ `poetry` commands only work with quoted creds while _others_ only work with non-quoted creds.

# How do I use it?
1. Install `poetry`
    * Best to follow the [install procedure on the official `poetry` repo](https://github.com/sdispater/poetry#installation)
2. Install `pooetry`
    * You can use the package manager of your choice for this, `pip install pooetry` for example
3. When you want to run `poetry` simply use `pooetry` instead.  All the commands and options will be passed through.