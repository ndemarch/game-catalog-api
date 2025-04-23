from app.models.items import SlotType

DEFAULT_LOADOUTS = {
    "Warrior": [
        {"name": "Longsword", "slot": SlotType.weapon, "damage": 10.0, "durability": 100.0, "defense": 0.0},
        {"name": "Metal Breastplate", "slot": SlotType.armour, "damage": 0.0, "durability": 100.0, "defense": 20.0},
    ],
    "Mage": [
        {"name": "Wand", "slot": SlotType.weapon, "damage": 5.0, "durability": 100.0, "defense": 0.0},
        {"name": "Mage Cloak", "slot": SlotType.armour, "damage": 0.0, "durability": 50.0, "defense": 5.0},
    ],
    "Rogue": [
        {"name": "Dagger", "slot": SlotType.weapon, "damage": 7.0, "durability": 100.0, "defense": 0.0},
        {"name": "Leather Armor", "slot": SlotType.armour, "damage": 0.0, "durability": 80.0, "defense": 10.0},
    ],
    "Healer": [
        {"name": "Staff", "slot": SlotType.weapon, "damage": 3.0, "durability": 100.0, "defense": 0.0},
        {"name": "Healer's Robe", "slot": SlotType.armour, "damage": 0.0, "durability": 60.0, "defense": 8.0},
    ],
    "Ranger": [
        {"name": "Bow", "slot": SlotType.weapon, "damage": 8.0, "durability": 100.0, "defense": 0.0},
        {"name": "Leather Armor", "slot": SlotType.armour, "damage": 0.0, "durability": 80.0, "defense": 10.0},
    ],
    "Archer": [
        {"name": "Crossbow", "slot": SlotType.weapon, "damage": 9.0, "durability": 100.0, "defense": 0.0},
        {"name": "Leather Armor", "slot": SlotType.armour, "damage": 0.0, "durability": 80.0, "defense": 10.0},
    ],
}
