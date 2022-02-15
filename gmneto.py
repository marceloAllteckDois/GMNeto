from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stockfish import Stockfish
import os
from pathlib import Path

def wait_element(driver,by_type, element):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_type, element)))
            return
        finally:
            return
    
def set_engine():
       stockfish_path=Path(r'stockfish_14.1_win_x64\stockfish_14.1_win_x64.exe')
       os.chmod(stockfish_path,777)
       engine = Stockfish(path=stockfish_path, depth=32,parameters={"Threads": 2, "Minimum Thinking Time": 30,"Hash": 16,"MultiPV": 1,
       "Skill Level": 20,
       "Move Overhead": 30,
       "Minimum Thinking Time": 20,})
       engine.set_elo_rating(3200)
       return engine

def open_site(driver):
    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[13]/div[2]/a[8]').click()
    wait_element(driver,By.XPATH,'//*[@id="username"]')
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys('"seu email ou nickname"')
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys('"sua senha"')
    driver.find_element(By.XPATH,'//*[@id="login"]').click()
    wait_element(driver,By.XPATH,'//*[@id="quick-link-computer"]')
    driver.find_element(By.XPATH,'//*[@id="quick-link-computer"]').click()
    wait_element(driver,By.XPATH,'/html/body/div[2]/div[7]/div/div/button')
    driver.find_element(By.XPATH,'/html/body/div[2]/div[7]/div/div/button').click()

    bot_scroll=driver.find_element(By.CLASS_NAME, 'bot-selection-scroll')
    bot_scroll.find_element(By.XPATH,'/html/body/div[4]/div[1]/section/div/div/div[7]/div[2]/div[1]/div').click()
    driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[2]/button').click()
    driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[2]/button').click() #esse é o botão de escolher
    chess_board = driver.find_element(By.TAG_NAME,'chess-board')
    return chess_board

def player_side(chess_board):
    player_is_black = False
    if chess_board.get_attribute('class') == 'layout-board board flipped':
        print('player is black')
        player_is_black = True
    elif chess_board.get_attribute('class') == 'layout-board board':
        print('player is white')
    return player_is_black
    
def converte_coluna(lance):
    lance_convertido = lance[0]
    if  lance_convertido == '1':
        lance_convertido =  lance_convertido.replace('1','a')
    elif  lance_convertido == '2':
        lance_convertido =  lance_convertido.replace('2','b')
    elif  lance_convertido == '3':
        lance_convertido =  lance_convertido.replace('3','c')
    elif  lance_convertido =='4':
        lance_convertido =  lance_convertido.replace('4','d')
    elif  lance_convertido == '5':
        lance_convertido =  lance_convertido.replace('5','e')
    elif  lance_convertido == '6':
        lance_convertido =  lance_convertido.replace('6','f')
    elif  lance_convertido == '7':
        lance_convertido =  lance_convertido.replace('7','g')
    elif  lance_convertido == '8':
        lance_convertido =  lance_convertido.replace('8','h')
    lance_convertido = lance_convertido + lance[1]
    return lance_convertido
def number_convert(move):
    move = move.replace('a','1')
    move = move.replace('b','2')
    move = move.replace('c','3')
    move = move.replace('d','4')
    move = move.replace('e','5')
    move = move.replace('f','6')
    move = move.replace('g','7')
    move = move.replace('h','8')
    return move
def convert_lance(lance, roque=False):
    if roque:
        str_saiu = converte_coluna(lance[3][16:18])
        str_foi = converte_coluna(lance[2][16:18])
    else:
        str_saiu = converte_coluna(lance[1][16:18])
        str_foi = converte_coluna(lance[0][16:18])
    return str_saiu+str_foi

def get_oponent_move(chess_board,player_is_black):  
    lista_lances_copy = []
    lista_dif = []
    oponent_move = ''
    for lance in chess_board.find_elements(By.TAG_NAME, 'div'):
        #lista_lances_copy.append(copy.deepcopy(lance.get_attribute('class')))
        lista_lances_copy.append(lance.get_attribute('class'))
    while len(lista_dif) <= 0:
        for i in range(len(lista_lances_copy)):
            if chess_board.find_elements(By.TAG_NAME, 'div')[i].get_attribute('class') != lista_lances_copy[i]:
                lista_dif.append(chess_board.find_elements(By.TAG_NAME, 'div')[i].get_attribute('class'))
                lista_dif.append(lista_lances_copy[i])
    if len(lista_dif) > 0 :
        if player_is_black:
            if lista_dif[0][6] == 'w':
                oponent_move=convert_lance(lista_dif,roque = len(lista_dif)>2 and lista_dif[2][6] == lista_dif[3][6])
                #print(lista_dif)
        else:
            if lista_dif[0][6] == 'b':
                oponent_move=convert_lance(lista_dif,roque = len(lista_dif)>2 and lista_dif[2][6] == lista_dif[3][6])
                #print(lista_dif)
    return oponent_move
def move_to_site(driver,stockfish_move,chess_board ):
    stockfish_move = number_convert(stockfish_move)
    square_size =0
    move_from = stockfish_move[0:2]
    move_to =stockfish_move[2:4]
    for piece_position in chess_board.find_elements(By.TAG_NAME, 'div'):
        if piece_position.get_attribute('class')[16:18] == move_from:
            action=ActionChains(driver)
            square_size = int(piece_position.size['height'])
            action.drag_and_drop_by_offset(piece_position,square_size*(int(move_to[0])- int(move_from[0])),square_size*(int(move_from[1])- int(move_to[1]))).perform()
            break
if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('https://www.chess.com')
    chess_board = open_site(driver)
    side = player_side(chess_board)
    e=set_engine()
    oponent_move=''
    list_move = ['']
    while True:
        if side == False:
            stockfish_move=e.get_best_move_time(1500)
            print(stockfish_move)
            move_to_site(driver,stockfish_move,chess_board )
            list_move[0] = stockfish_move
            e.make_moves_from_current_position(list_move)
            while oponent_move == '':
                oponent_move = get_oponent_move(chess_board,side)
            print('oponent_move:'+oponent_move)
            list_move[0]=oponent_move
            e.make_moves_from_current_position(list_move)
            oponent_move=''
        else:
            while oponent_move == '':
                oponent_move = get_oponent_move(chess_board,side)
            print('oponent_move:'+oponent_move)
            list_move[0]=oponent_move
            e.make_moves_from_current_position(list_move)
            oponent_move=''
            stockfish_move=e.get_best_move_time(1500)
            print(stockfish_move)
            move_to_site(driver,stockfish_move,chess_board )
            list_move[0] = stockfish_move
            e.make_moves_from_current_position(list_move)
#novo bug, se o jogador fizer um lance muito rapido ou um pré-move o algo não lê o lance
    