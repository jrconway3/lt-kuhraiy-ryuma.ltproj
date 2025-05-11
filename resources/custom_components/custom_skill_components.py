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


class ReduceWeaponWeight(SkillComponent):
    nid = 'reduce_weapon_weight'
    desc = 'Reduce weapon weight '
    tag = SkillTags.CUSTOM

    expose = ComponentType.Int
    value = 1

class AdjustWeight(SkillComponent):
    nid = 'adjust_weight'
    desc = "Applies +X weight"
    tag = SkillTags.COMBAT

    expose = ComponentType.Int
    value = 2

    def modify_resist(self, unit, item):
        return self.value