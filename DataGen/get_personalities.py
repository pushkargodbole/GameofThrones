

def get_personalities(files):
    personalities = []
    for file in files:
        f = open(file, 'r')
        if(f):
            for line in f:
                elems = line.split()
                if len(elems) == 2:
                    personality = elems[1].strip()
                    if personality not in personalities:
                        personalities.append(personality)
        f.close()
                        
    return personalities

if __name__ == "__main__":
    files = ['../Data/traits1.txt', '../Data/traits2.txt']
    personalities = get_personalities(files)
    
    for i in range(len(personalities)):
        print str(i+1)+'.', personalities[i]
