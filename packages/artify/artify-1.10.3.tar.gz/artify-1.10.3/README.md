
Upload to Nexus, Upload files to hooks, Modify version number, Syncing of GitLab/GitHub type repository, Generate template files, Create Git tags, Extract commands from Git commit messages, Create SonarQube projects, Archive file(s), Create changelog.md file

[![Downloads](https://static.pepy.tech/personalized-badge/artify?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/artify)

Installation
============
You can download and install the latest version of this software from the Python package index (PyPI) as follows::

    pip install --upgrade artify

Usage
=====
    python -m artify --help=

    python -m artify --command <command> [Options]
or

`python -m artify -c <command> [Options]`


**Params**

command &nbsp; &nbsp; &nbsp; &nbsp; nexus, syncrepo, deploy, deltav, create, extract, initialize, archive
<br>

Create CHANGELOG.md file
========================

`python -m artify -c changelog`

**Optional params**

--projectname &nbsp; &nbsp; &nbsp; &nbsp; Used to specify project when solution has more than 1 project. For .NET/NET core projects

**.Net/.Netcore example below:**

`python -m artify -c changelog --projectname Client`

<br>

Upload to Nexus
===============

    python -m artify -c nexus -f <format> -n <artifact_name> -h <nexus_repository_base_url>

**Important**

Artifact name should include artifact id and version number. E.g example-ws-1.0.0.war

**Params**

-f, --format &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Nexus upload format. Types supported: raw, npm, maven

-w, --workdirectory &nbsp; &nbsp; &nbsp; Working directory of artifact to be uploaded to Nexus repository

-n, --artifactname &nbsp; &nbsp; &nbsp; &nbsp; Artifact name

-r, --repository &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Nexus repository to upload to: e.g <repository>-snapshots

-g, --groupid &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Group ID for Maven2 type repository, Environment variable: NEXUS_GROUP_ID

-d, --directory &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Directory for RAW type repository

-u, --username &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Username of nexus user, Environment variable: NEXUS_USERNAME

-p, --password &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; Password of nexus user, Environment variable: NEXUS_PASSWORD

--proxy &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sets Http proxy

--proxysec &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sets Https proxy

**Optional Parameter(s)**

--file2  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp; Allow second file to be upload, will be uploaded as a classifier

<br>

### Environment variables (Optional if set with -u, -p, -g parameter above)

**NEXUS_GROUP_ID** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Group ID of the project e.g com.testing.testapplication


**NEXUS_USERNAME** &nbsp; &nbsp; &nbsp; &nbsp; Username of nexus user that will upload artifact


**NEXUS_PASSWORD** &nbsp; &nbsp; &nbsp; &nbsp; Password of nexus user that will upload artifact

<br>

Deploy App using custom AWX host
================================

    python -m artify -c deploy -f <manifest_file.yml> -h <awx_host>

### Environment variables need
**DEPLOY_TOKEN** &nbsp; &nbsp; &nbsp; &nbsp; Token used to deploy application

<br>

Change Package version
======================

Artify uses semantic version 2.0.

`python -m artify -c deltav -t patch -a npm`

`python -m artify -c version -t patch -a flutter`

`python -m artify -c deltav -t auto -a other --file=setup.py`

`python -m artify -c version -t minor -a gradle --file=version.properties`

**Params**

-a, --archtype &nbsp; &nbsp; &nbsp; &nbsp; npm, gradle, flutter, maven, dotnet, other

-t, --type &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; major, minor, patch, prerelease, auto

**Optional Params**

--preValue &nbsp; &nbsp; &nbsp; &nbsp; Prerelease version value e.g SNAPHOT, RELEASE, BUILD, beta, alpa
<br>

--getversion &nbsp; &nbsp; &nbsp; Get the current application version

--nocommit &nbsp; &nbsp; &nbsp;  Does not create feature branch with version change

--file &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; File name that you want to update version number. It should be relative to artify execution directory

--file2 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; An additional file that you want to update version number. It should be relative to artify execution directory

<br>

Push changes to GitLab/GitHub repository
=================================

### Recommendation: You can create a feature branch, then perform your code changes before pushing changes to remote
    python -m artify -c syncrepo -m <message> -b 


**Params**
 
 -c, --message &nbsp; &nbsp; &nbsp; &nbsp; Commit message

 -b, --branch &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Optional, by default, it will push to 'develop' branch


### Environment variables need

**PRIVATE_TOKEN**, popularly known as personal access token is needed to perform the push. This can be created by following this guide:

[Creating a personal access token: GitLab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)


[Creating a personal access token: GitHub](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

**N.B** &nbsp; A commit is performed automatically followed by a push

<br>

Creating Tags
==============

`python -m artify -c syncrepo -m tag`

**Optional Params**

--projectname &nbsp; &nbsp; &nbsp; &nbsp; Used to specify project when solution has more than 1 project. For .NET/NET core projects


`python -m artify -c syncrepo -m tag` &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Creates a git tag of repository branch that task is executed on e.g v-1.0.0-a56def9

`python -m artify -c syncrepo -m tag --projectname Client` &nbsp; Creates a git tag of repository branch for the Client project that task is executed on (**For .NET/.NET core projects**) e.g v-1.0.0.0-b56dcf9


**N.B** Please set environment variable **CI_COMMIT_SHORT_SHA** (This variable is already set in GitLab type repository)

<br>

Generate Template files
=======================

### Generate template .gitlab-ci.yml file
`python -m artify -c create -f gitlabci` 

### Geneate template manifest.yml file
`python -m artify -c create -f manifest`

**Params**
-f, --file &nbsp; &nbsp; &nbsp; &nbsp; File template to generate

**Supported files**
- .gitlab-ci.yml
- manifest.yml

<br>

Extract commands from GIT message
=================================
`python -m artify -c extract`

**N.B** If manifest.yml file is present, it will update version number in that file also.

**Parameters**

- version/deltav - specifies type of version change e.g "version": "patch", "deltav": "patch", "version": "minor", "version": "auto"



- archtype - specifies project architecture e.g "archtype": "npm", "archtype": "gradle", "archtype": "flutter", "archtype": "other"


**Environment variable(s) needed**

CI_COMMIT_MESSAGE &nbsp; &nbsp; &nbsp; This the variables that is used to extract dictionary formatted command

**N.B** For GitHub, you can set value using commands below pipeline line (*.yml):

env:

&nbsp; &nbsp;CI_COMMIT_MESSAGE: ${{ github.event.head_commit.message }}

<br>

**Optional Parameters**

- branch - speficies branch you want to push changes. If branch is not specified, it push changes to 'develop' branch by default

- nocommit - Does not create feature branch with version change


- file - File name that you want to update version number. It should be relative to artify execution directory


- file2 - An additional file that you want to update version number. It should be relative to artify execution directory

**Sample commit messages**

1. Added login functionality {"version": "patch", "archtype": "npm", "branch": "release-1.0.0" } - Updates the patch version of npm type project, and push to branch called 'release-1.0.0' branch


2. Added search functionality {"deltav": "major", "archtype": "gradle" } - Updates the major version of a java project with Gradle build tool


3. Added edit functionality {"version": "minor", "a": "flutter" } - Updates the minor version of a flutter project  

4. Add filter functionality {"version": "prerelease", "archtype": "npm", "preValue": "beta"} - Updates the prerelease value i.e Version 1.0.0 would change to 1.0.0-beta


5. Upgrade from Angular 11 to Angular 12 {"version": "auto", "archtype": "gradle", "branch": "feature/angular-12"} - Updates the pre-release integer value by 1 e.g 1.0.0-beta1 will change to 1.0.0-beta2

<br/>

Initialize SonarQube project
============================

`python -m artify -c initialize -h <SonarQube_base_url> -k <project-key> -n <project-name> -u <username> -p <password> -a <arch_type/os> -l <language>`

**Sample command**

`python -m artify -c initialize -h <SonarQube_base_url> -k <project-key> -n <project-name> -u <username> -p <password> -l java -a gradle`

`python -m artify -c initialize -h <SonarQube_base_url> -k <project-key> -n <project-name> -u <username> -p <password> -l java -a maven`

<br>

**For Windows Runner, Other (JS, TS, Go, Python, PHP, ...)**  

python -m artify -c initialize -h <SonarQube_base_url> -k <project-key> -n <project-name> -u <username> -p <password> -l other -a windows

<br>

**For Linux/macOS runner, Other (JS, TS, Go, Python, PHP, ...)**

python -m artify -c initialize -h <SonarQube_base_url> -k <project-key> -n <project-name> -u <username> -p <password> -l other -a linux

<br>

**Parameters**

-l, --language =>  Possible values: JS, TS, Go, Python, PHP, other)

-a, --archtype =>  Architecture, OS (depends on usage)

-n, --projectname => Project name.

-k, --projectkey => Project key. This should be a unique identifier for project.

-u, --username => Username for SonarQube. 

-p, --password => Password for SonarQube. The user should be able to create projects.

**N.B**. The user should have the permission to create/modify projects.

python -m artify -c initialize -h <SonarQube_base_url> -k <project-key> -n <project-name> -u <username> -p <password> -a php


<br>

Archive file(s)
========================================
Uses Shutil Python library to create archive file

`python -m artify -c archive -n <archive_name> -f <archive_format> -w <root_dir> -d base_dir>`

**Parameters**

-n, --archivename  Name for the archive file that will be created.

-f, --format       Format for the archive e.g zip, tar, gztar, bztar, xztar.

-w, --rootdir      Root directory is a directory that will be the root directory of the archive.

-d, --basedir      Base directory is the directory where we start archiving from.