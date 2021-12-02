# Proyecto pokemon, empezando con objetos

elements = ["fire","water","grass"]

class Pokemon:
    def __init__(self,name,element,HP):
        self.name = name
        self.element = element
        self.HP = HP
        self.attacks = []

    def learn(self, attack):
        self.attacks.append(attack)

    def receive_damage(self,attack):
        self.HP -= attack.damage

    def __str__(self):
        return f"Pokemon({self.name},{self.element},{self.HP})"
   
class Attack:
    def __init__(self,name,element,damage):
        self.name = name
        self.element = element
        self.damage = damage
    
    def __repr__(self):
        return f"Attack({self.name},{self.element},{self.damage}"



charmander = Pokemon("Charmander",elements[0],100.0)
squirtle = Pokemon("Squirtle",elements[1],110.0)
bulbasur = Pokemon("Bulbasur",elements[2],95.0)

fireball = Attack("Fireball",elements[0],25.0)

charmander.learn(fireball)  # charmander aprende un ataque, definido en la calse attack
print(squirtle.HP)              
squirtle.receive_damage(charmander.attacks[0])  # squirtle recibe daño del ataque de charmander
print(squirtle.HP)




