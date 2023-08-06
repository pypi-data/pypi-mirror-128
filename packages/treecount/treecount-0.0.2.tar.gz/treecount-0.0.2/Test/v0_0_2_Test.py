# Importing Module(s)
from src.treecount import display_tree


# Main Method
if __name__ == '__main__':

    # 1. Test for String Representation [True]
    stringRepresentation = display_tree(string_rep = True)
    print(stringRepresentation)

    # 2. Test for Console-Print [False]
    display_tree()


