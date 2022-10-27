def check_number ( text_in:str = 'Введите число: ', text_breac:str = 'Вы ввели число не правильно, введите его заново:'): 
    '''
    Проверка, явл.ется ли введённые данные числом. 
    Если нет то повторяется запрос заново.
    text_in - техт запроса в консоли
    text_breac - техт вторичного запроса, при неправильном вводе числа
    '''
    while True:
        try:
            number = float(input(text_in))
            return number
    
        except ValueError:
            print(text_breac)


def check_number_min (data_in:str, min_number:int = 0, text_breac:str = 'Вы ввели число не правильно, введите его заново:', text_min:str ='Вы ввели число меньше минимального, введите его заново: '): 
    '''
    Проверка, являются ли введённые данные числом и не меньше минимума. 
    Если нет то повторяется запрос заново.
    data_in - данные для проверки
    text_breac - техт вторичного запроса, при неправильном вводе числа
	text_min - текст запроса, если число меньше минимума
	min_number - минимальное число
    bool_error,  text_error, number

    '''
    while True:
        try:
            number = int(data_in)

            if number<min_number: # если значение меньше min_number
                return True,text_min, None 
            return False,None, number
    
        except ValueError:
            return True,text_breac, None

def check_number_min_max (data_in:str, min_number:int = 0, max_number: int =100, text_breac:str = 'Вы ввели число не правильно, введите его заново:', text_min:str ='Вы ввели число меньше минимального, введите его заново: ', text_max:str ='Вы ввели число больше максимального, введите его заново: '): 
    '''
    Проверка, являются ли введённые данные числом, и лежит ли это число в диапазоне 
    от минимума до максимума. 
    Если нет то повторяется запрос заново.
    data_in - данные для проверки
    text_breac - техт вторичного запроса, при неправильном вводе числа
	text_min - текст запроса, если число меньше минимума
	text_max - текст запроса, если число больше максимума
	min_number - минимальное число
 	max_number - максимальное число
    bool_error,  text_error, number
    '''
    while True:
        try:
            number = int(data_in)

            if number<min_number:
               return True,text_min, None 
            elif number>max_number:
                return True,text_max, None
            return False,None, number
    
        except ValueError:
            return True,text_breac, None


def imput_name(text_in:str):# Проверка правильности введения имени 
    if len(text_in)>0 and text_in[0].islower()==True:
        return True, "Введите имя с большой буквы "
    elif len(text_in)>0 and text_in[0].isdigit()==True:
        return True, "Имя должно начинаться с буквы"
    elif len(text_in)>0 and text_in.find(' ')>0:
        return True, "Имя введено с пробелами"
    elif len(text_in)==0:
       return True, "Имя не введено"
    else:
        return False, text_in