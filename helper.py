

def save_information(classobj):
    for variable, value in vars(classobj).items():
        print(variable, value)