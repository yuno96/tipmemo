
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
- Python 3 Project : Gui Text Editor using Tkinter, File Handling
  * https://www.hackanons.com/2018/08/python-3-project-gui-text-editor-using.html
- Icons
  * https://icons8.com/
- Programming in Python 3: A Complete Introduction to the Python Language
  * refer to delete item from dbm
- Syntax Highlight: How to use Tag in Text widget
  * https://www.tutorialspoint.com/python/tk_text.htm
- Text Widget:
  * http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/text-methods.html
  * http://epydoc.sourceforge.net/stdlib/Tkinter.Text-class.html
- Mergeing overlapping intervals
  * https://codereview.stackexchange.com/questions/69242/merging-overlapping-intervals
