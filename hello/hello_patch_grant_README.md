# Hello Patch Tutorial

This tutorial has two associated python files and
[a YouTube playlist](https://www.youtube.com/playlist?list=PLytZkHFJwKUdfxFQnuo0Fson0QM0VL9hL).

The pastable snippets are here:

```python
        await asyncio.sleep(10)
        print(f"v1val: {workflow.patched("v1")}")
```

## Video Explanations

Each video had some explanation text at the top --
that is pasted below:

### Video 1: Not Replaying

In this video, we'll begin to discuss the behavior
of the patched function. We'll start by
showing what it does when not replaying, and
in another video, we'll show what happens when replaying.

- if not replaying, and the execution hits a call to patched,
  it first checks the event history, and:
  - if the patch ID is not in the event history,
    it will add a marker to the
    event history and upsert a search attribute
  - if the patch ID is in the event history,
    it won't modify the history
- In either case, it will return true

> there is a caveat to the above, and
> we will get to that in a later video

### Video 2: Replaying with Patch ID in the history

In this video, we'll continue our discussion of the behavior
of the patched function. We'll
show what it does when replaying.

- if replaying, and the code has a call to patched,
  - if the patch ID is somewhere in the event history
    - if the event is after where we currently are
      in the event history, then, in other words,
      our patch is before the
      event, then our patch is too early. it will
      attempt to write the marker to the replay event
      history, but it will throw a non-deterministic
      exception because the replay and original event
      histories don't match
    - if the event is before where we currently are
      in the execution, and there hasn't been a call to patched
      with that id yet, then it won't even get to this call
      because an NDE would have already been thrown
    - if the event is where we currently are in the
      event history, it will return true and add a
      marker to the replay event history (which means it
      will match the original event history) and it will
      continue.
      *This is similar to the behavior of the non-replay case*
    - if the event is before where we currently are
      in the execution, meaning the replay already has seen
      a call to patched with this ID,
      it will return true and not
      do anything to the replay event history
      *This is similar to the behavior of the non-replay case*
  - if the patch ID is not anywhere in the event history
    - we will discuss in the next video

### Video 3: Replaying with Patch ID not in the history

In this video, we'll finish our discussion of the behavior
of the patched function. We'll
show what it does when replaying, and the patch ID
is nowhere in the event history.

- if replaying, and the code has a call to patched,
  - if the patch ID is somewhere in the event history
    - ...
  - if the patch ID is not anywhere in the event history
    - it will return false and not add anything to
      the event history. Furthermore, and this is the
      caveat, it will make all future calls to patched
      with that ID false -- even after it is done replaying
      and is running normal code.

Why is this a caveat?

- in the first video, we said that if not replaying,
  the patched function will always return true, and if
  the marker doesn't exist, it will add it, and if
  the marker already exists, it won't re-add it.

  But what this
  is saying is that this doesn't hold if there was already
  a call to patched with that ID in the replay code, but not
  in the event history.
