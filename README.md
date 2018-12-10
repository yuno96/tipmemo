
# tipmemo

## Intro.
Easy to record and search a tons of tips working on the cross-platform

## Layout

```
+---------------------------+
| panel_menu                |
+------------_--------------+
| panel_search              |
+------------+--------------+
| panel_head | panel_body   |
|            |              |
+------------+--------------+
| panel_status              |
+---------------------------+
```

## Data Management

### directory structure

```
data            <-- root dbpath
+- cache        <-- database(dbm)
+- 112312414-0  <-- Saved file which means time in seconds
+- 112312413-0
+- 112312412-0
```
### Database format
```
filename,title
```

### Fileformat

```
title\n
contents
```

## References
- Make Notepad using Tkinter
  * https://www.geeksforgeeks.org/make-notepad-using-tkinter/
