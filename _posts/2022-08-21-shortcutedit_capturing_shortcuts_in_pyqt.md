---
layout: post
title: ShortcutEdit - capturing shortcuts in PyQt
description: A simple GUI component to capture shortcuts in PyQt
categories: GUI
tags: Python
author: Sl-Alex
--- 

{% include image.html url="/assets/2022-08-21-shortcutedit_capturing_shortcuts_in_qt/example.gif" description="Here is how it looks like" %}

You need it if:

- you need to support a numpad modifier
- you need just a single shortcut, not a sequence of keys or shortcuts.
- you need a shortcut immediately after you pressed a combination of buttons
- you need an easily modifiable shortcut editor

If one of the above is what you need then this post is for you.



There are many ways to implement a custom shortcut editor, but we will use the easiest one: subclassing a QLineEdit.

QLineEdit already has everything we need. It has a nice input field that can capture the keys and it can show custom text.
So, the idea is to extend the QLineEdit by installing a custom event filter. In PyQt it is very easy to do:

```python
from PyQt5.QtWidgets import QLineEdit

class ShortcutEdit(QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress:
            # Ignore empty events, report "processed"
            if event.key() == 0 and int(event.modifiers()) == 0:
                return True

            print(f'KeyPress: Key={event.key()}, Modifier={int(event.modifiers())}')
            return True
        elif event.type() == QtCore.QEvent.KeyRelease:
            return True

        return False
```

Good thing is that we don't even need to care about all previous keys and about key releases. KeyPress event already has a last pressed key and all the modifiers. If a modifier key has been pressed then it will be in both ```event.key()``` and ```event.modifiers()```

Based on this we can write a complete component. The full code of the example in under spoiler below.

This might be not the latest version of the code. The most recent version is always on [this GitHub Gist](https://gist.github.com/Sl-Alex/20bace0271a59c8b6db446c3faacefb0)

<details>
  <summary markdown='span'>Full code</summary>

```python
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

""" Extension of QLineEdit with a possibility to catch shortcuts.
Standard QKeySequenceEdit is too slow and does not make any difference between numpad and normal keys.
"""
class ShortcutEdit(QLineEdit):

    """This signal is emitted whenever a new key or modifier is pressed
    First parameter is the key (can be zero), second is a list of modifiers
    """
    shortcutChanged = QtCore.pyqtSignal(int, list)

    keymap = {}
    modmap = {}
    modkeyslist = []

    current_modifiers = []
    current_key = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, value in vars(Qt).items():
            if isinstance(value, Qt.Key):
                self.keymap[value] = key.partition('_')[2]
                
        self.modmap = {
            Qt.ControlModifier:     'Ctrl',
            Qt.AltModifier:         'Alt',
            Qt.ShiftModifier:       'Shift',
            Qt.MetaModifier:        'Meta',
            Qt.GroupSwitchModifier: 'AltGr',
            Qt.KeypadModifier:      'Num',
            }

        self.modkeyslist = [
            Qt.Key_Control,
            Qt.Key_Alt,
            Qt.Key_Shift,
            Qt.Key_Meta,
            Qt.Key_AltGr,
            Qt.Key_NumLock,
            ]

        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress:
            # Ignore empty events, report "processed"
            if event.key() == 0 and int(event.modifiers()) == 0:
                return True

            # Reset the state
            self.current_modifiers = []
            self.current_key = 0

            # Extract event key and modifiers
            key = event.key()
            modifiers = int(event.modifiers())
            
            # Prepare a map with the current modifiers (a copy of self.modmap with only active modifiers)
            modifiers_dict = {}
            for modifier in self.modmap.keys():
                if modifiers & modifier:
                    modifiers_dict[modifier] = self.modmap[modifier]

            # Invalidate the key (it is already in the modifiers list anyway)
            if key in self.modkeyslist:
                key = 0

            text = ''
            # First, add all modifiers
            for modifier in modifiers_dict:
                if text != '':
                    text = text + '+'
                text = text + modifiers_dict[modifier]
                self.current_modifiers.append(modifier)
            # Special case for numpad keys, print them like NumMinus or Num5, without separator
            if Qt.KeypadModifier in modifiers_dict and key != 0:
                text = text + self.keymap[key]
                self.current_key = key
            # Normal keys
            elif key in self.keymap:
                if text != '':
                    text = text + '+'
                text = text + self.keymap[key]
                self.current_key = key

            # Update the text and emit a signal
            self.setText(text)
            self.shortcutChanged.emit(self.current_key, self.current_modifiers)

            return True
        elif event.type() == QtCore.QEvent.KeyRelease:
            return True

        return False
```
  
</details>
