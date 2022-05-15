import extract


def main():
    
    source2 = 'C:\\Python\\Projects\\finalset\\dataset\\phish.csv'
    dest2 = 'C:\\Python\\Projects\\finalset\\phish.csv'
    
    content = open(source2, 'r').readlines()
    content_set = set(content)
    
    cleandata = open(dest2, 'w')
    
    for line in content_set:
        cleandata.write(line)


if __name__ == "__main__":
    main()
