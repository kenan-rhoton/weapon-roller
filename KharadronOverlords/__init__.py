from UnitRoller import Weapon, Unit, Roll

# Weapons
PrivateerPistol = Weapon(attacks=2, hit=Roll(4), wound=Roll(4), damage=1)
AethermaticVolleyGun = Weapon(attacks=6, hit=Roll(5), wound=Roll(4), damage=1, rend=-1)
LightSkyhook = Weapon(attacks=1, hit=Roll(4), wound=Roll(3), damage=2, rend=-2)

# Units
ArkanautCompany_WithVolleyGuns = Unit() \
    .with_weapons(PrivateerPistol, amount=7) \
    .with_weapons(AethermaticVolleyGun, amount=3) \
    .with_cost(120) \
    .with_save(Roll(5))

ArkanautCompany_WithSkyhooks = Unit() \
    .with_weapons(PrivateerPistol, amount=7) \
    .with_weapons(LightSkyhook, amount=3) \
    .with_cost(120) \
    .with_save(Roll(5))

