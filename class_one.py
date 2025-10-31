class Pet():
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age


    def displayInfo(self):
        return f"My Pet {self.name} is a {self.species} species and it is {self.age} years old"
    

    def birthday(self):
        self.age += 1
        return f"Hurray {self.name} is plus one. It is {self.age} years today"



my_cat = Pet("Tiny", "gentle", 2)
print(my_cat.displayInfo())
print(my_cat.birthday())