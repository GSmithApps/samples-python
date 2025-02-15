# Event Loop Canary Sample

This can help you determine if your event loop is clogged.

The idea is that you could add this canary workflow
to your worker initialization, and
it will log the delays in your event loop.

> Note: it doesn't tell you what is clogging it, but it tells you
> whether something is clogging it.

## Example

In one terminal, run:

```txt
$ poetry run python canary/your_workflows.py

# no output
```

And in another, run the following:

```txt
$ poetry run python canary/run_canary_worker.py

Your activity finished after 0.5 seconds
Your activity finished after 1.3 seconds
Your activity finished after 1.3 seconds
The canary detected 1.1774 seconds of event loop delay.
Your activity finished after 1.4 seconds
Your activity finished after 1.1 seconds
Your activity finished after 1.2 seconds
The canary detected 0.7662 seconds of event loop delay.
Your activity finished after 1.3 seconds
Your activity finished after 0.8 seconds
Your activity finished after 1.3 seconds
The canary detected 0.4724 seconds of event loop delay.
Your activity finished after 0.9 seconds
Your activity finished after 1.3 seconds
Your activity finished after 1.3 seconds
The canary detected 0.6033 seconds of event loop delay.
Your activity finished after 1.4 seconds
Your activity finished after 1.4 seconds
Your activity finished after 0.7 seconds
The canary detected 0.5424 seconds of event loop delay.
Your activity finished after 1.2 seconds
Your activity finished after 0.7 seconds
Your activity finished after 0.7 seconds
Your activity finished after 0.9 seconds
The canary detected 0.6584 seconds of event loop delay.
...
```
