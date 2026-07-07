class student:
    def __init__(self,name,rollno):
        self.name=name
        self.rollno=rollno
    def details(self):
        
        print("roolno=",self.rollno)
        print("name=",self.name)
c=student("john",101)
c.details()
