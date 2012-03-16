 Rice CAS Backend
=================

This is a simple backend designed to work with the django-cas package, providing integration with Rice's LDAP server to retrieve name and email data for logged-in users.

Usage
-----
In settings.py, instead of including `'django_cas.backends.CASBackend'` in your `AUTHENTICATION_BACKENDS`, include `'rice_cas_backend.backends.RiceCASBackend'` instead. 