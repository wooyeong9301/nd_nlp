# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Translation.wooy import enru


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(enru(['Settings', 'Search']))

    # f1 = open('./Data/system_messages/en_source.txt', 'r')
    # f2 = open('./Data/system_messages/ru_translated.txt', 'w')
    #
    # for line in f1.readlines():
    #     print(line)
    #     tmp = enru(line)
    #     tmp = tmp + '\n'
    #     print(tmp)
    #     f2.write(tmp)
    #
    # f2.close()
    # f1.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


