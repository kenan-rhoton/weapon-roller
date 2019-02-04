from UnitRoller import Weapon, Unit, Roll

# Weapons
FyresteelThrowingAxes_Unit = Weapon(attacks=1, hit=Roll(4), wound=Roll(4), damage=1)
MoltenRockbolts = Weapon(attacks=2, hit=Roll(4), wound=Roll(3), damage=1, rend=-1)


# Units
AuricHearthguard = Unit() \
    .with_weapons(FyresteelThrowingAxes_Unit, amount=5) \
    .with_weapons(MoltenRockbolts, amount=5) \
    .with_cost(100) \
    .with_save(Roll(5))

