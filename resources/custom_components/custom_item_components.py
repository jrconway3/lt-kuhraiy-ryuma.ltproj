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

class ManaUses(ItemComponent):
    nid = 'uses_mana'
    desc = "Display number of uses based on MANA."
    paired_with = ('uses_options',)
    tag = ItemTags.USES

    expose = ComponentType.Int
    value = 1

    _did_something = False

    def init(self, item):
        item.data['uses'] = self.value
        item.data['starting_uses'] = self.value

    def available(self, unit, item) -> bool:
        return item.data['uses'] > 0

    def is_broken(self, unit, item) -> bool:
        return item.data['uses'] <= 0

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        if item.uses_options.one_loss_per_combat():
            self._did_something = True
        else:
            actions.append(action.SetObjData(item, 'uses', item.data['uses'] - 1))
            actions.append(action.UpdateRecords('item_use', (unit.nid, item.nid)))

    def on_miss(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        if item.uses_options.lose_uses_on_miss():
            if item.uses_options.one_loss_per_combat():
                self._did_something = True
            else:
                actions.append(action.SetObjData(item, 'uses', item.data['uses'] - 1))
                actions.append(action.UpdateRecords('item_use', (unit.nid, item.nid)))

    def on_broken(self, unit, item):
        from app.engine.game_state import game
        if item in unit.items:
            action.do(action.RemoveItem(unit, item))
        elif item in game.party.convoy:
            action.do(action.RemoveItemFromConvoy(item))
        else:
            for other_unit in game.get_units_in_party():
                if item in other_unit.items:
                    action.do(action.RemoveItem(other_unit, item))

    def end_combat(self, playback, unit, item, target, item2, mode):
        if self._did_something and 'uses' in item.data:
            action.do(action.SetObjData(item, 'uses', item.data['uses'] - 1))
            action.do(action.UpdateRecords('item_use', (unit.nid, item.nid)))
        self._did_something = False

    def reverse_use(self, unit, item):
        if self.is_broken(unit, item):
            if item_funcs.inventory_full(unit, item):
                action.do(action.PutItemInConvoy(item))
            else:
                action.do(action.GiveItem(unit, item))
        action.do(action.SetObjData(item, 'uses', item.data['uses'] + 1))
        action.do(action.ReverseRecords('item_use', (unit.nid, item.nid)))

    def special_sort(self, unit, item):
        return item.data['uses']

class UsesMana(ItemComponent):
    nid = 'uses_mana'
    desc = "Display number of uses based on MANA."
    paired_with = ('mana',)
    tag = ItemTags.USES

    expose = ComponentType.NewMultipleOptions

    options = {
        'lose_uses_on_miss': ComponentType.Bool,
        'one_loss_per_combat': ComponentType.Bool
    }

    def __init__(self, value=None):
        self.value = {
            'lose_uses_on_miss': False,
            'one_loss_per_combat': False
        }
        if value and isinstance(value, dict):
            self.value.update(value)
        else: # value is a list from the old multiple options
            try:
                self.value['lose_uses_on_miss'] = value[0][1] == 'T'
                self.value['one_loss_per_combat'] = value[1][1] == 'T'
            except:
                pass

    def lose_uses_on_miss(self) -> bool:
        return self.value.get('lose_uses_on_miss', False)

    def one_loss_per_combat(self) -> bool:
        return self.value.get('one_loss_per_combat', False)