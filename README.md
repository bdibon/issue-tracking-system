# Issue tracking system

This is an API built with the [django-rest-framework](https://github.com/encode/django-rest-framework) that emulates a very sober version of JIRA.

Once a user has registered, he can create a project, add other users as contributors to the project, then every contributor can create and participate to issues, comment on them, etc.

Authentication is handled via JWT, and permissions are applied regarding the status of the user i.e whether he owns the ressource or not, and if he is part of a specific project team or not.

You can find the API documentation [here](https://documenter.getpostman.com/view/7484015/UVsHS6ye).

## Setup

Let's assume you have `pipenv` installed on your machine, then all you need to do is to clone this repository locally.

```
git clone https://github.com/bdibon/issue-tracking-system.git
```

Then from the project's directory, install the required project's dependencies.

```
> pipenv install
```

Activate the virtual environment.

```
> pipenv shell
```

Run the development server!

```
> py manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 10, 2022 - 12:12:10
Django version 4.0.3, using settings 'project_config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
