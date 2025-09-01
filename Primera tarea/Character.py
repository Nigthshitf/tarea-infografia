
import random
from typing import List, Dict

class Character:
    def _init_(self, nombre: str, hp: int, base_damage: int, parry_prob: float, crit_prob: float):
        self.nombre = nombre
        self.max_hp = hp
        self.hp = hp
        self.base_damage = base_damage
        self.parry_prob = parry_prob
        self.crit_prob = crit_prob
        self.effects: List[Dict] = []

        self.abilities: List[Dict] = []

    def is_alive(self) -> bool:
        return self.hp > 0

    def apply_effects_start_turn(self):
        """Aplica efectos que ocurren al inicio del turno (DoT, HoT, buffs con duración)."""
        to_remove = []
        for e in list(self.effects):
            if e['type'] == 'dot':
                dmg = e['value']
                self.hp -= dmg
                if self.hp < 0: self.hp = 0
                print(f"  {self.nombre} recibe {dmg} de {e.get('name','DoT')} (queda {self.hp} HP).")
            elif e['type'] == 'hot':
                heal = e['value']
                self.hp = min(self.max_hp, self.hp + heal)
                print(f"  {self.nombre} se cura {heal} por {e.get('name','HoT')} (queda {self.hp} HP).")
            e['turns'] -= 1
            if e['turns'] <= 0:
                to_remove.append(e)

        for r in to_remove:
            self.effects.remove(r)
            print(f"  Efecto {r.get('name','(efecto)')} en {self.nombre} ha terminado.")

    def current_parry(self) -> float:
        """Calcula parry actual (base + buffs)."""
        parry = self.parry_prob
        for e in self.effects:
            if e['type'] == 'buff' and e.get('what') == 'parry':
                parry += e['value']
        return min(0.95, parry)

    def current_crit(self) -> float:
        crit = self.crit_prob
        for e in self.effects:
            if e['type'] == 'buff' and e.get('what') == 'crit':
                crit += e['value']
        return min(0.95, crit)

    def attack(self, other: 'Character'):
        crit_chance = self.current_crit()
        damage = self.base_damage * 2 if random.random() <= crit_chance else self.base_damage
        print(f"{self.nombre} ataca a {other.nombre} ({'CRIT' if damage > self.base_damage else 'normal'}) -> daño {damage}")
        other.hurt(damage)

    def hurt(self, damage: int):
        if random.random() <= self.current_parry():
            print(f"  {self.nombre} realiza un PARRY y evita el daño.")
            return
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"  {self.nombre} recibe {damage} de daño, queda {self.hp} HP.")

    def add_effect(self, effect: Dict):
        """Añade un efecto (dot/hot/buff) como dict con keys: type,name,value,turns,(what)."""
        self.effects.append(effect)

    def add_ability(self, name: str, kind: str, func, uses_left: int = 1, description: str = ""):
        self.abilities.append({
            'name': name,
            'kind': kind,       
            'func': func,       
            'uses_left': uses_left,
            'description': description
        })

    def use_ability(self, idx: int, target: 'Character'):
        """Ejecuta habilidad si tiene usos disponibles. Devuelve True si tuvo efecto, False si no se pudo."""
        if idx < 0 or idx >= len(self.abilities):
            print("Índice de habilidad inválido.")
            return False

        abil = self.abilities[idx]
        # comprobar correctamente si hay usos (<=0 cubre negativos)
        if abil.get('uses_left', 0) <= 0:
            print(f"Esa habilidad ({abil['name']}) ya no tiene usos.")
            return False

        print(f"{self.nombre} usa {abil['name']} sobre {target.nombre if target else 'sí mismo'}")
        # ejecutar la función de la habilidad
        abil['func'](self, target, abil)

        # decrementar usos según tipo
        if abil['kind'] == 'single':
            abil['uses_left'] = 0
        elif abil['kind'] == 'uses':
            abil['uses_left'] = max(0, abil.get('uses_left', 1) - 1)
        return True

    def show_status(self) -> str:
        return f"{self.nombre} HP:{self.hp}/{self.max_hp} DMG:{self.base_damage} PAR:{self.current_parry():.2f} CRIT:{self.current_crit():.2f}"



def rogue_crit_burst(user: Character, target: Character, meta):
    dmg = user.base_damage * 3
    print(f"  {user.nombre} hace Crit Burst a {target.nombre} por {dmg}")
    target.hurt(dmg)

def rogue_poison(user: Character, target: Character, meta):
    target.add_effect({'type': 'dot', 'name': 'Poison', 'value': 5, 'turns': 3})
    print(f"  {target.nombre} queda envenenado por 3 turnos (5 dmg/turno).")

def tank_shield_up(user: Character, target: Character, meta):
    user.add_effect({'type': 'buff', 'name': 'Shield Up', 'what': 'parry', 'value': 0.25, 'turns': 2})
    print(f"  {user.nombre} aumenta su parry +0.25 por 2 turnos.")

def tank_crush(user: Character, target: Character, meta):
    dmg = user.base_damage * 2
    print(f"  {user.nombre} hace Crush a {target.nombre} por {dmg}")
    target.hurt(dmg)

def wizard_fireball(user: Character, target: Character, meta):
    dmg = user.base_damage * 3
    print(f"  {user.nombre} lanza Fireball a {target.nombre} por {dmg}")
    target.hurt(dmg)

def wizard_burn(user: Character, target: Character, meta):
    target.add_effect({'type': 'dot', 'name': 'Burn', 'value': 7, 'turns': 2})
    print(f"  {target.nombre} sufre Burn: 7 dmg por 2 turnos.")

def paladin_heal(user: Character, target: Character, meta):
    heal = 30
    user.hp = min(user.max_hp, user.hp + heal)
    print(f"  {user.nombre} se cura {heal}. Queda {user.hp} HP.")

def paladin_holy_guard(user: Character, target: Character, meta):
    user.add_effect({'type': 'buff', 'name': 'Holy Guard', 'what': 'parry', 'value': 0.2, 'turns': 2})
    print(f"  {user.nombre} activa Holy Guard: +0.2 parry por 2 turnos.")


# Factories

def create_rogue(nombre: str) -> Character:
    c = Character(nombre, hp=80, base_damage=25, parry_prob=0.05, crit_prob=0.25)
    c.add_ability("Crit Burst", 'single', rogue_crit_burst, uses_left=1, description="Gran daño single-use")
    c.add_ability("Poison Blade", 'uses', rogue_poison, uses_left=2, description="Aplica DoT 3 turnos")
    return c

def create_tank(nombre: str) -> Character:
    c = Character(nombre, hp=220, base_damage=12, parry_prob=0.25, crit_prob=0.05)
    c.add_ability("Shield Up", 'uses', tank_shield_up, uses_left=2, description="Aumenta parry por 2 turnos")
    c.add_ability("Crush", 'uses', tank_crush, uses_left=2, description="Daño fuerte, varios usos")
    return c

def create_wizard(nombre: str) -> Character:
    c = Character(nombre, hp=70, base_damage=18, parry_prob=0.05, crit_prob=0.18)
    c.add_ability("Fireball", 'single', wizard_fireball, uses_left=1, description="Gran daño single-use")
    c.add_ability("Burn", 'uses', wizard_burn, uses_left=2, description="DoT por 2 turnos")
    return c

def create_paladin(nombre: str) -> Character:
    c = Character(nombre, hp=150, base_damage=16, parry_prob=0.15, crit_prob=0.08)
    c.add_ability("Heal", 'uses', paladin_heal, uses_left=2, description="Cura al usuario")
    c.add_ability("Holy Guard", 'uses', paladin_holy_guard, uses_left=2, description="Aumenta parry por 2 turnos")
    return c