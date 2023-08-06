

print("!! main SQL !!!!!!!!!!!")

import sys
def main(args=None):
    if args is None:
        args =  sys.argv[1:]

    print("@ SQL @!!",args)
    
    import os,__main__,site
    os.system("echo '"+str(id(__main__))+" "+str(id(site))+" '>/content/DDID_BBB.py" )

if __name__=="__main__":
    print("@ SQL @ "*20,__name__)
    main()