from __future__ import annotations

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.skill_components import SkillComponent, SkillTags
from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system)
from app.engine.game_state import game
from app.engine.objects.unit import UnitObject
from app.utilities import utils, static_random


class DoNothing(SkillComponent):
    nid = 'do_nothing'
    desc = 'does nothing'
    tag = SkillTags.CUSTOM

    expose = ComponentType.Int
    value = 1

class WeightChange(SkillComponent):
    nid = 'weight_change'
    desc = "Raise or lower current weight"
    tag = SkillTags.COMBAT

    expose = ComponentType.Int
    value = 0

    def modify_attack_speed(self, unit, item):
        return -1 * max(0, (item.weight.value + self.value) - equations.parser.constitution(unit))

    def modify_defense_speed(self, unit, item):
        return -1 * max(0, (item.weight.value + self.value) - equations.parser.constitution(unit))

    def modify_avoid(self, unit, item):
        return -2 * max(0, (item.weight.value + self.value) - equations.parser.constitution(unit))

class WeightMultiplier(SkillComponent):
    nid = 'weight_multiplier'
    desc = "Raise or lower current weight"
    tag = SkillTags.COMBAT

    expose = ComponentType.Int
    value = 0

    def modify_attack_speed(self, unit, item):
        return -1 * max(0, (item.weight.value * self.value) - equations.parser.constitution(unit))

    def modify_defense_speed(self, unit, item):
        return -1 * max(0, (item.weight.value * self.value) - equations.parser.constitution(unit))

    def modify_avoid(self, unit, item):
        return -2 * max(0, (item.weight.value * self.value) - equations.parser.constitution(unit))