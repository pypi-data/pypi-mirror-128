"""."""

class ActionRow:
    def __init__(self, components):
        self.base = {"type": 1, "components": components}

    def build(self):
        return self.base

class SelectMenu:
    def __init__(self, custom_id, options):
        self.base = {"type": 3, "custom_id": custom_id, "options": [op.build() for op in options if isinstance(op, SelectMenuOption)]}

    def build(self):
        return self.base

class SelectMenuOption:
    def __init__(self, label: str, description: str, value: str, emoji: dict = {}):
        self.base = {"label": label, "description": description, "value": value, "emoji": emoji}

    def build(self):
        return self.base

class ButtonStyle:
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5

class Button:
    def __init__(self, custom_id,  style: int = ButtonStyle.PRIMARY, label: str = '', url: str = None, emoji: dict = None, disabled: bool = False, timeout: float = 0.0, single_use: bool = False):
        self.timeout = timeout
        self.single_use = single_use
        self.base = {"type": 2, "style": style, "label": label, "custom_id": custom_id, "disabled": disabled}

        if emoji is not None:
            self.base["emoji"] = emoji
        if style == ButtonStyle.LINK and url is not None:
            self.base["url"] = url

    def build(self):
        return self.base

    def __raw__(self):
        f = self.base
        f["timeout"] = self.timeout
        f['single_use'] = self.single_use
        return f
