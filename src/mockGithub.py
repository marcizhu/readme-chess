class Issue:
    def __init__(self, title=''):
        self.__title = title

    @property
    def title(self):
        if(self.__title == ''):
            self.__title = input('Enter issue title: ')

        return self.__title

    def create_comment(self, text):
        print(f'ISSUE: New comment: \'{text}\'')

    def edit(self, state='opened', labels=[]):
        print(f'ISSUE: Edited; state=\'{state}\', labels={labels}')

    def add_to_labels(self, label):
        print(f'ISSUE: Added label: \'{label}\'')
