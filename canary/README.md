# Canary Sample

This can help you determine if your event loop is clogged.

The idea is that you could add this canary workflow
to your code, and
if it doesn't log every second, then something long-running
is clogging the event loop.

> Note: it doesn't tell you what is clogging it, but it tells you
> whether something is clogging it.

## Example

```txt
$ run `poetry run python canary/main.py`

Your activity finished after 1.4 seconds
Your activity finished after 1.3 seconds
Your activity finished after 0.7 seconds
The canary showed the event loop took 0.4 seconds to get back after its await finished
Your activity finished after 1.0 seconds
Your activity finished after 0.6 seconds
Your activity finished after 0.7 seconds
Your activity finished after 1.3 seconds
The canary showed the event loop took 0.7 seconds to get back after its await finished
Your activity finished after 0.9 seconds
Your activity finished after 1.1 seconds
Your activity finished after 1.2 seconds
The canary showed the event loop took 0.3 seconds to get back after its await finished
Your activity finished after 1.2 seconds
Your activity finished after 1.4 seconds
Your activity finished after 0.5 seconds
The canary showed the event loop took 0.2 seconds to get back after its await finished
Your activity finished after 1.3 seconds
Your activity finished after 1.4 seconds
Your activity finished after 1.0 seconds
The canary showed the event loop took 0.9 seconds to get back after its await finished
```
