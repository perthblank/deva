class DGSD_Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    print(DGSD_Colors.HEADER + 'header' + DGSD_Colors.ENDC)
    role = """
 o
""" +DGSD_Colors.HEADER +  '-+-' +DGSD_Colors.ENDC + """
 ^
"""
    print(role)
