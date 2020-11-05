# Google Drive Tools

### Purpose
TBD

### Set Up
Before you begin go to google api console and download your credentials file. Rename the file 
to "credentials.json". Place the "credentials.json" at the root of the project.

Install google drive dependencies. 

`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`


I use [poetry](https://python-poetry.org) to manage package installation. 

## Git setup

Initialize git

`git init`

Set the git origin

`git remote add origin git@gitlab.ops.ripple.com:ITE/Jamf_devices_gone_missing.git`

Pull in the project

` git pull git@gitlab.ops.ripple.com:ITE/Jamf_devices_gone_missing.git`

## Install dependencies.
I use [poetry](https://python-poetry.org) to manage package installation.

`poetry install`
