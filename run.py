from PCOL_lib import Agent, Colony, Rule
import fce
from fce import read_colony_from_file
import math

def main():
    file="ukazka.txt"
    col1=read_colony_from_file(file)
    res=fce.computation(col1,4)
    print(res)

    

if __name__ == "__main__":
    main()