global classes
classes = ['ain', 'alf', 'baa', 'daad', 'dal', 'faa', 'gem', 'gen',
           'ha', 'haa', 'hamza', 'kaf', 'khaa', 'lam', 'lam alf',
           'lam alf hamza', 'lam alf mad', 'mem', 'non', 'qaf', 'raa', 'saad', 'shen',
           'sin', 'taa', 'tah', 'thaa', 'waw', 'yaa', 'zah', 'zal', 'zin']


# function to conver the class name to arabic character
def get_char(class_index):
    class_eq = [
        'ع', 'ا', 'ب', 'ض', 'د', 'ف', 'ج', 'غ',
        'ه', 'ح', 'ء', 'ك', 'خ', 'ل', 'لا',
        'لأ', 'لآ', 'م', 'ن', 'ق', 'ر', 'ص', 'ش',
        'س', 'ت', 'ط', 'ث', 'و', 'ي', 'ظ', 'ذ', 'ز']
    return class_eq[class_index]
