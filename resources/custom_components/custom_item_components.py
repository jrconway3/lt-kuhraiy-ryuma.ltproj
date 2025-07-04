from __future__ import annotations

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.item_components import ItemComponent, ItemTags
from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system)
from app.engine.game_state import game
from app.engine.objects.unit import UnitObject
from app.utilities import utils, static_random


class DoNothing(ItemComponent):
    nid = 'do_nothing'
    desc = 'does nothing'
    tag = ItemTags.CUSTOM

    expose = ComponentType.Int
    value = 1

class ManaOptions(ItemComponent):
    nid = 'mana_options'
    desc = "Additional options for MANA uses."
    paired_with = ('mana',)
    tag = ItemTags.USES

    expose = ComponentType.NewMultipleOptions

    options = {
        'lose_mana_on_miss': ComponentType.Bool,
        'one_loss_per_combat': ComponentType.Bool
    }

    def __init__(self, value=None):
        self.value = {
            'lose_mana_on_miss': True,
            'one_loss_per_combat': False
        }
        if value and isinstance(value, dict):
            self.value.update(value)
        else: # value is a list from the old multiple options
            try:
                self.value['lose_mana_on_miss'] = value[0][1] == 'T'
                self.value['one_loss_per_combat'] = value[1][1] == 'T'
            except:
                pass

    def lose_mana_on_miss(self) -> bool:
        return self.value.get('lose_mana_on_miss', False)

    def one_loss_per_combat(self) -> bool:
        return self.value.get('one_loss_per_combat', False)