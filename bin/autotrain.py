#!usr/bin/env python
import os
from glob import glob
import sys

def main():
    for root, dirs, files in os.walk(os.getcwd()):
        for dir in dirs:
            data_files = glob(os.path.join(dir, "*.tab"))
            for c in data_files:
                if os.path.getsize(c) == 0:
                    continue
                callsdata = orange.ExampleTable(os.path.join("./", c))
                for e in callsdata:
                    # if metatag tune exists:
                        # if metatag == 'fm':
                            # move file to 'fm' training folder
                            
                            
                    
if __name__ == '__main__':
    main()