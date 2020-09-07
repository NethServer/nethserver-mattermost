=====================
nethserver-mattermost
=====================

Stack:

- Mattermost
- PostgreSQL 12 listening on non-standard port 55434
- Apache as proxy server

Apache configuration derived from: https://github.com/mattermost/docs/issues/1114


First configuration
===================

Mattermost requires a dedicated virtualhost and it's accessibile only from HTTPS.

To start Mattermost, execute:

:: 

  config setprop mattermost VirtualHost mattermost.yourdomain.com status enabled
  signal-event nethserver-mattermost-update

Then, access ``https://mattermost.yourdomain.com`` and perform the first configuration.


Database
========

Properties:

- ``TCPPort``: Mattermost listen port, change only for development purpose
- ``VirtualHost``: dedicated FQDN for virtual host
- ``status``: can be ``enabled`` or ``disabled``, default to ``disabled``
- ``access``: firewall access, leave blank or at least set to ``none``

Example: ::

 mattermost=service
    TCPPort=5432
    VirtualHost=mattermost.local.neth.eu
    access=
    status=enabled

Account synchronization
=======================

The ``mattermost-bulk-user-create`` command will:

- create a default team named as the ``Company`` from ``OrganizationContact``
- read all users from local or remote Account Providers and create them inside Mattermost

Please note that:

- users disabled in the Server Manager or already existing in Mattermost will be skipped
- a random password will be generated for each user

Forcing a common default password
---------------------------------

It's possible to set a default password for each new Mattermost user, just append the default
password to command invocation.

Example: ::

  mattermost-bulk-user-create Password,1234


Cockpit API
===========

read
----

Return mattermost status and configuration.
No input required.

Output
^^^^^^

Example: ::

 {
  "status": {
    "users": "2",
    "teams": "1",
    "channels": "2",
    "posts": "2"
  },
  "configuration": {
    "props": {
      "status": "enabled",
      "access": "",
      "VirtualHost": "mattermost.nethserver.org",
      "TCPPort": "5432"
    },
    "name": "mattermost",
    "type": "service"
  }
 }


validate
--------

Constraints:

- ``VirtualHost``: must be a valid FQDN

Input
^^^^^

Example: ::

 {
  "props": {
    "status": "enabled",
    "VirtualHost": "mattermost.nethserver.org",
  },
  "name": "mattermost",
 }


update
------

Same input as validate.
