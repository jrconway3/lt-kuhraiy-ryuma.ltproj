from __future__ import annotations

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.item_components import ItemComponent, ItemTags
from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system)
from app.engine.game_state import game
from app.engine.objects.unit import UnitObject
from app.utilities import utils, static_random

from app.engine.fonts import NORMAL_FONT_COLORS, FONT
from app.engine.game_menus.icon_options import UsesDisplayConfig


class DoNothing(ItemComponent):
    nid = 'do_nothing'
    desc = 'does nothing'
    tag = ItemTags.CUSTOM

    expose = ComponentType.Int
    value = 1

class CustomUsesColor(ItemComponent):
    nid = 'custom_uses_color'
    desc = "Override the default color of the uses text. Do not Combine with ManaCostAsUses or RemainingManaUses."
    tag = ItemTags.USES
    value = 'white'

    expose = (ComponentType.MultipleChoice, ['white', 'blue', 'green', 'red', 'orange', 'grey', 'yellow', 'brown', 'purple', 'navy'])

    def _font_color(self, unit, item):
        color = self.value
        if not item_funcs.available(unit, item):
            color = 'grey'
        if 'text-' + color in FONT:
            return color
        return None

    def item_uses_display(self, unit, item) -> UsesDisplayConfig:
        return UsesDisplayConfig(None, None, None, self._font_color, unit, item)