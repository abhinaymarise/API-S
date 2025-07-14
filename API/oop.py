#===========  Class Object Creation Practice ==============

#======== Creation of Class =================

class Employee:
    def __init__(self,name,role,salary):
        self.name=name
        self.role=role
        self.salary=salary

    def read_function(self):
        return f"The name is {self.name} and the role is {self.role} and the pay is {self.salary}"
    
#=========== Creation of Object ===============

emp1=Employee("Abhinay","SDE",200000)
print(emp1.read_function())
        