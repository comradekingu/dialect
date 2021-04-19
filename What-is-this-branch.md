# What is this branch?

It's an experimental port of Dialect to GTK4. It's not meant to be usable. It's meant to be a useful resource when the actual port happens.

What works perfectly:

- About dialog
- Keyboard shortcuts dialog

Everything else either doesn't work or has issues. In the current state:

- Launches.
- Translation works, including Enter or Ctrl+Enter to search.
- Audio, pronunciations and mistakes work.
- Preferences dialog launches. But a few things are broken:
  - Backend selection works, but the backend labels don't work.
  - Crash when typing invalid backend due to GtkPopover behavior changes.
- Language switcher works but is full of bugs.
- A lot of other weird issues.
