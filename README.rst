=====================
nethserver-mattermost
=====================

Stack:

- Mattermost
- PostgreSQL 9.4 listening on non-standard port 55432
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
