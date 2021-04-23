# What is this branch?

It's an experimental port of Dialect to GTK4. It's not meant to be usable. It's meant to be a useful resource when the actual port happens.

Most things somewhat work. Everything else either doesn't work or has issues. In the current state:

- Launches.
- Translation works, including Enter or Ctrl+Enter to search.
- Live translation, Audio, pronunciations and mistakes work.
- Preferences dialog launches. But a few things are broken:
  - Backend selection works, but the backend labels don't work.
  - Crash when typing invalid backend due to GtkPopover behavior changes.
- Language switcher works but when searching, items are not properly filtered. They are instead hidden in a weird manner.
- Setting window size with set_default_size or through UI file seems to set with a 52px offset. (X11-only bug)
- When repeatedly maximizing and unmaximizing the window, the width might increase suddenly if it was less than 690 before maximizing. (X11-only bug)
- Possibly many others.
