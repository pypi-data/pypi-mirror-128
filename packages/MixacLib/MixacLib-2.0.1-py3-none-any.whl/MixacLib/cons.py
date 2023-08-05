from colorama import Fore
import os


def inf(information: str):
    green = Fore.GREEN
    reset = Fore.RESET
    print('[' + green + '信息' +reset + ']' + information)
    pass


def debug(debuginf: str):
    cyan = Fore.CYAN
    reset = Fore.RESET
    print('[' + cyan + '调试' + reset + ']' + debuginf)
    pass


def warn(warning):
    yellow = Fore.YELLOW
    reset = Fore.RESET
    print('[' + yellow + '警告' + reset + ']' + warning)
    pass


def error(errorinf):
    red = Fore.RED
    reset = Fore.RESET
    print('[' + red + '错误' + reset + ']' + errorinf)
    pass


def title(titlestr):
    magenta = Fore.MAGENTA
    reset = Fore.RESET
    print(magenta + titlestr + reset)

try:
    import console.utils
    def ctitle(name):
        console.utils.set_title(name)
        inf('已设置标题为 {}'.format(name))
        pass
except ImportError:
    warn('导入console失败，可能因为使用了Pyinstaller，请不要使用ctitle！')


def echo():
    inf('1145141919810')
    pass


def chenrnmsl():
    title('[陈睿]你所热爱的，就是你的生活。')
    title(' - [蒙古上单]你 妈什么时候死啊')


if __name__ == '__main__':
    chenrnmsl()
    pass
