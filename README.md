
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
```

## Data Management

### directory structure

```
data                     <-- root dbpath
+- 201811                <-- monthly creation
  +- 223123-filename.md  <-- Saved file 
```
### Fileformat

FileCreationTimeInSeconds-FileName.extension
```
example) 223123-filename.md 
```

## References
- Make Notepad using Tkinter
  * https://www.geeksforgeeks.org/make-notepad-using-tkinter/
