import extract


def main():
    source = 'C:\\Python\\Projects\\finalset\\dataset\\phish.csv'
    dest = 'C:\\Python\\Projects\\finalset\\dataset\\features_dataset.csv'
    extract.main(source, dest)
    print('''
#######################################
#   Dataset generated successfully!   #
#######################################
            ''')


if __name__ == "__main__":
    main()
