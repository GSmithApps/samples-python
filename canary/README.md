# Probing Sample

This can help you determine if your event loop is clogged.

The idea is that you could add this probing workflow
to your code, and
if it doesn't log every second, then something long-running
is clogging the event loop.

> It doesn't tell you what is clogging it, but it tells you
> whether something is clogging it.

run `poetry run python probing/main.py`
