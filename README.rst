Crowd Auth Backend for Sentry
=============================

A Crowd authentication backend for Sentry.

Tested with Sentry 8.12.0.


Install
-------

.. code-block:: console

    $ pip install https://github.com/robbi5/sentry-auth-crowd/archive/master.zip


Setup
-----

In Atlassian Crowd create an application for Sentry we will need the
application name and password for the Sentry configuration.

Make sure the remote addresses are set correct to avoid authentication failures.

The following settings should be set in ``sentry.conf.py``:

.. code-block:: python

    # Url of the Crowd server
    CROWD_URL = ""
    # The application name of Sentry in Crowd
    CROWD_APP_NAME = ""
    # The application password of Sentry in Crowd
    CROWD_APP_PASSWORD = ""
    # The team slugs a new user should automatically be member of.
    CROWD_DEFAULT_TEAM_SLUGS = []


SSO Support
-----------

This fork of sentry-auth-crowd supports the SSO authproviders from Sentry.

After first signin a screen appears that a new user is going to be created.
Unfortunately you have to enter your crowd credentials here again, because we don't store the password in the session.
