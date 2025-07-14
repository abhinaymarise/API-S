def read(first_name,last_name):
    return first_name+" "+last_name

fname="abhinay"
a=read(fname.capitalize(),"marise")
print(a)


def read_1(first_name:list,last_name:str):
    return first_name[0].capitalize()+" "+last_name.capitalize()

fname_1=["abhinay"]
b=read_1(fname_1,"marise")
print(b)