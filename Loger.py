from datetime import datetime

def log_data(text_log):

    folder = r'C:\Users\SBB2-Ермилов Артём\YandexDisk-artyomermiloff\GeegBrains\Programming\Python\Homework\HW9\HW9_Сandy_game\LogCalc.txt'
    #folder =r'LogCalc.txt'

    with open( folder, 'a+', encoding='UTF-8') as file:
        file.write(f'{datetime.now()}:  {text_log}\n')
        