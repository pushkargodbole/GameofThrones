

def get_characters(file):
    f = open(file, 'r')
    if(f):
        characters = []
        endline='Retrieved from'
        for line in f:
            if len(line) > 3:
                if line[:3] == '  *':
                    elems = line.split()
                    for elem in elems:
                        if elem.find('</index.php') >= 0:
                            elem = elem.strip('</>,')
                            character = elem.split('/')[1]
                            characters.append(character)
                            break
            if line.find(endline) >= 0:
                break
                
        f.close()
        return characters
        
if __name__ == "__main__":
    file = "../Data/awoiaf_loc.txt"
    characters = get_characters(file)
    for i in range(len(characters)):
        print st+'.', characters[i]
