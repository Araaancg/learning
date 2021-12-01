# Proyecto pokemon, empezando con objetos

elements = ["fire","water","grass"]

class Pokemon:
    def __init__(self,name,element,HP):
        self.name = name
        self.element = element
        self.HP = HP
        self.attacks = []

    def learn(self, attack_name):
        self.attacks.append(attack_name)

    def __str__(self):
        return f"Pokemon:({self.name},{self.element},{self.HP})"
   

charmander = ["Charmander",elements[0],100.0]
print(charmander)

print(charmander.attacks)
charmander.learn("fireball")
print(charmander.attacks)
