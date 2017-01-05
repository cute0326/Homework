# -*- coding: utf-8 -*-
import string
import random

#定义各种全局变量
hangmanstring = ['  +---+','  |   |','      |','      |','      |','      |','=========']

DIGIT = 5
#生成随机字符串，充当单词。

# answer = 'write'
answer = ''.join(random.sample(['a','b','c','d','e','f','g','h','i','j'], DIGIT)).replace(" ","")
target_set = set(answer)

#初始化猜中后的单词状态及其他变量
puzzle_word = ['*' for i in range(DIGIT)]

#定义各种函数开始
#定义函数，格式用户输入字符,含非字符串重新输入，多余一个字符串截断。
def InputChar():
        while(True):
                input_char = input('please input the "char" you guessed,(I will just take the first "char" , and the redundant content will be cut off , ):').strip()
                if('' == input_char):
                        print('please input at least one non-blank char!')
                else:
                        for i in input_char:
                                if(True == i.isalpha()):
                                        return i.lower()  #将可能输入的大写字符改成小写，保证和asnwer中的字符一致。
                        print()
                        print('*' * 20 + ' '+ 'please input only one char, at least input a string includes a char' + ' '+ '*' * 20)
                        print()
# 猜中之后，显示单词当前状态
def ShowString(inputchar):
        for i in range(DIGIT):
                if(inputchar == answer[i]):
                        puzzle_word[i] = answer[i]

                current_word_show = ''
                for i in range(DIGIT):
                        current_word_show += puzzle_word[i]
        print('The answer current status is :\" %s \" '  %(current_word_show))

#编辑HangMan
def HangManShow(wrong_number):
        if(wrong_number > 7):
                return
        if(wrong_number == 1):
                PrintHangMan()
        elif(wrong_number == 2):
                hangmanstring[2] = '  O   |'
                PrintHangMan()
        elif(wrong_number == 3):
                hangmanstring[3] = '  |   |'
                PrintHangMan()
        elif(wrong_number == 4):
                hangmanstring[3] = ' /|   |'
                PrintHangMan()
        elif(wrong_number == 5):
                hangmanstring[3] = ' /|\  |'
                PrintHangMan()
        elif(wrong_number == 6):
                hangmanstring[4] = ' /    |'
                PrintHangMan()
        else:
                hangmanstring[4] = ' / \  |'
                PrintHangMan()

#打印HangMan
def PrintHangMan():
        for i in range(7):
                print(hangmanstring[i])

def Guess_Process(wrong_number = 0):
        guess_char = InputChar()
        #还是有点问题，连续输入正确答案，第二次输入将被忽略
        while(wrong_number < 7 and len(target_set) != 0):
                if( guess_char in target_set):
                        print('*' *  80)
                        print('You get it the char : %s' %(guess_char))
                        ShowString(guess_char)
                        target_set.discard(guess_char)
                        if(len(target_set) == 0):
                                break
                        guess_char = InputChar()
                        while(guess_char in puzzle_word):
                                print('You have already got the letter, please enter another char!')
                                guess_char = InputChar()
                else:
                        wrong_number += 1
                        print('*' *  80)
                        print('You have wrong for %d time(s): ' %(wrong_number))
                        # print('*' *  80)
                        HangManShow(wrong_number)
                        # print('*' *  80)
                        if(wrong_number == 7):
                                break
                        guess_char = InputChar()


        if(len(target_set) == 0):
                print('*'* 20 + 'Congratulations, You win the game !!' + '*'* 20 )
                print('The answer of the riddle is %s' %(answer))
        else:
                print('You have lose the game! Bad luck!!! But you can try it again!!!')

#提示用户游戏开始，可以输入字符
print('*'* 20 + 'The Hangman Guessing Games'+ '*'* 20 )
print('The answer is %s' %answer)  #帮助调试，正式发布时需要删除

Guess_Process()
