# Django LDP editor

## Context

The goal of this repository is to make available to all of our models a editor feature, covering the editor action, diseditor action, and count of both use cases.

The editor Model will be related to an IDURLField targetting users/ so that we will be able to relate the users and their editors in a distributed world.

Would ideally be implemented in a way which makes it compatible with the [ActivityPub editor Activity](https://www.w3.org/TR/activitypub/#editor-activity-outbox) 

Add your package in settings.py of the app. Now, you can test if your package is imported propefully by doing a
`python manage.py shell` then
from djangoldp_myawesomepackage.models import ExampleModel

If, no error, it's working.

## Planning

1. Make it work:

Being able to post a editor, a diseditor.
Being able to retrieve the count of editors and diseditors for a given resource
Being able to do that on the federation instance bearing the current user identity

2. Make it clean

Test it in the context of the federation
Ensure we stay compliant with the activityPub specification

## CICD
When you're ready to publish your app :
1. Add the `sib-deploy` user as a `maintainer` to the project (`Settings > Members`)

2. Configure `pipeline strategy` to `clone` (`Settings > CI/CD > Pipelines`)

3. Protect the `master` branch allowing only `maintainers` to push (`Settings > Repository > Protected branches`)

4. Configure CI/CD variables to authenticate on pypi.org:

Variable        | Value              | Protection
----------------|--------------------|-----------
`GL_TOKEN`      | `sib-deploy-token` | protected
`PYPI_PASSWORD` | `pypi-password`    | protected
`PYPI_USERNAME` | startinblox        | protected

5. Replace the "do_not_publish" by "master" in the .gitlab-ci.yml

### Factories
If you dont need factory, you can remove the mock_example command, the factories files and the extras_require section in setup.cfg

Provide a factory is a good pratice in order to simplify the mocking of data on a server / in a test pipeline.

## Contribute !

As the Startin'Blox project is evolving a lot and quickly, we're going to need to update this demo regularly! 
For any suggestion, you can open an issue or contact the last person who updated it: 

alice@startinblox.com

Thanks!