class animal:
    def details(Self):
        name="animal"
        print("name=",name)
class dog(animal):
        sound="bow bow"
        name="zimba"
        print("sound=",sound)
        print("name=",name)
        def bark(Self):
            print("woof!woof!")
c=dog()
c.bark()
c.details()
