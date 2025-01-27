# `Patched()` function Deep Dive

This tutorial has two associated python files and
[a YouTube playlist](https://www.youtube.com/playlist?list=PLytZkHFJwKUdfxFQnuo0Fson0QM0VL9hL).

The pastable snippets are here:

## Not Replaying

- if not replaying, and the execution hits a call to patched,
  it first checks the event history, and:
  - if the patch ID is not in the event history,
    it will add a marker to the
    event history and upsert a search attribute
    (you can think of this like the first block of patching with
    a given patch ID)
  - if the patch ID is in the event history,
    it won't modify the history
    (you can think of this like the second
    block of patching of a given patch ID)
- In either case, it will return true

> there is a caveat to the above in Python and Dotnet, and
> we will discuss that below

## Replaying With Marker Before-Or-At Current Location

- if replaying,
  - if the code has a call to patched, and if the event history
    has a marker from a call to patched in the same place (which means it
    will match the original event history), then
    write a marker to the replay event history and return true.
    *This is similar to the behavior of the non-replay case, and
    just like in that one, you can think of this like the first block of patching with
    a given patch ID*
  - if the code has a call to patched, and the event history
    has a marker with that Patch ID earlier in the history,
    then it will simply return true and not modify the
    replay event history.
    *This is similar to the behavior of the non-replay case, and just
    like in that case, you can think of this like the second
    block of patching of a given patch ID*

## Replaying With Marker After Current Location or No Marker at All

We have covered what happens when replaying and the code
hits a call to patched and there's a marker in the event
history on or before that spot in the execution. What remains
is what happens if (1) the marker is after that spot in the
execution or (2) if there is no marker at all for that patch.

In these situations, the TypeScript SDK behaves in one way,
and the Python and Dotnet SDKs behave in another.

### (1) There is a marker after that spot in the execution

#### (1) TypeScript With Later Marker

Returns False.

#### (1) Python and Dotnet With Later Marker

if the event is after where we currently are
in the event history, then, in other words,
our patch is before the
event, then our patch is too early. it will
attempt to write the marker to the replay event
history, but it will throw a non-deterministic
exception because the replay and original event
histories don't match

### (2) There is no marker for that Patch ID

#### (2) TypeScript With No Marker

Returns False.

#### (2) Python and Dotnet With No Marker

it will return false and not add anything to
the event history. Furthermore, ***and this is the
caveat mentioned in the very first section***, it will make all future calls to patched
with that ID false -- even after it is done replaying
and is running new code.

Why is this a caveat?

in the first video, we said that ***if not replaying,
the patched function will always return true***, and if
the marker doesn't exist, it will add it, and if
the marker already exists, it won't re-add it.

But what this
is saying is that this doesn't hold if there was already
a call to patched with that ID in the replay code, but not
in the event history. In this situation, it won't return
true.

### A Summary of the Two Potentially Unexpected Behaviors

(neither of these apply to typescript, but they both apply
to python and dotnet)

1. When Replaying, in the scenario of ***it hits a call to
   patched, but that patch ID isn't before/on that point in
   the event history***, you may not expect that
   the event history *after* where you currently
   are matters. Because:
   1. If that patch ID exists later, you get an NDE [(see Python and Dotnet Later Marker above)](#1-python-and-dotnet-with-later-marker).
   2. If it doesn't exist later, you don't get an NDE, and
      it returns false
      [(see Python and Dotnet No Marker above)](#2-python-and-dotnet-with-no-marker).

   (In TypeScript, both of these just return false with no NDE)
2. When Replaying, if you hit a call to patched with an ID that
   doesn't exist in the history, then not only will it return
   false in that occurence, but it will also return false if
   the execution surpasses the Replay threshold and is running new code.
   [(see Python and Dotnet No Marker above)](#2-python-and-dotnet-with-no-marker).

   (This doesn't happen in TS -- it will
   return false in that occurence, but this doesn't modify the behavior
   of future calls).
