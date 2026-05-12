"""
Global settings for the GUI application,
such as window size, colors, fonts, and themes.
"""

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

FONT_FAMILY = "Microsoft JhengHei"

LIGHT_THEME = {
    "name": "light",
    "background_image": "background.png",

    "title": "#145A2A",
    "subtitle": "#2F5D3A",

    "green": "#1F6B36",
    "button_green": "#3A9B47",

    "panel_bg": "#FAFFFA",
    "hint_bg": "#EEF8EA",
    "text": "#163F22",
    "sub_text": "#5C6F5C",
    "border": "#D6E8D1",

    "entry_bg": "white",
    "entry_fg": "#163F22",
    "listbox_bg": "white",
    "listbox_fg": "#163F22",
}

DARK_THEME = {
    "name": "dark",
    "background_image": "background_darktheme.png",

    "title": "#D9F7C8",
    "subtitle": "#B9DFA8",

    "green": "#9BE074",
    "button_green": "#3A9B47",

    "panel_bg": "#18231D",
    "hint_bg": "#243529",
    "text": "#E6F5DD",
    "sub_text": "#B7C8B1",
    "border": "#3E5C44",

    "entry_bg": "#101914",
    "entry_fg": "#E6F5DD",
    "listbox_bg": "#101914",
    "listbox_fg": "#E6F5DD",
}

THEMES = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME,
}