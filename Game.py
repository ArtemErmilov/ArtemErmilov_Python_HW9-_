


from os import system
from random import randint
system ('cls')
import Check as ck


def candy_game(candies:int,total_candies:int,candies_one_step:int,uc:str, uc0:str,uc1:str):
    '''
    Игра в конфеты. Проигрывает тот , кто взял последнюю конфету.
    candies - конфеты взятые играком
    total_candies - общее количество конфет участвующее в игре 
    candies_one_step - максимальное количество конфет, которые можно взять за один ход.
    uc - играющий игрок
    uc0 - первый игрок
    uc1 - второй игрок
    total_candies, uc, game_run
    '''    
    total_candies-=candies

    if total_candies >1:
        if total_candies <= candies_one_step:
            candies_one_step = total_candies
        if uc==uc0:
            uc=uc1
        else:
            uc=uc0

        return total_candies,candies_one_step, uc, True
    elif total_candies==1 :
        return total_candies,candies_one_step, uc, False
    else:
        if uc==uc0:
            uc=uc1
        else:
            uc=uc0
        return total_candies,candies_one_step, uc, False


def bot_game_candies(candies_min,candies_max):
    """
    Бот, который в случайном порядке генерирует количество 
    конфет от candies_min до candies_max
    """

    candies = randint(candies_min,candies_max)
    return candies

def  smart_bot_game_candies(total_candies,max_candies):
    '''
    Умный бот:
    total_candies - максимальное количество конфет
    max_candies - максимальное количество конфет, которые берутся за один шаг
    '''
    number=1
    if total_candies//max_candies>1:
        if total_candies%(max_candies+2)==0:
            number = 1
        elif total_candies%(max_candies+2)==(max_candies+1):
            number = 1
        else:
            number=total_candies%(max_candies+2)
    else:
        if total_candies%(max_candies+2)==0:
            number = 1
        elif total_candies%(max_candies+2)==(max_candies+1):
            number = max_candies
        else:
            number=total_candies%(max_candies+2)-1

        return number




