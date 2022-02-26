import colorama
import pyttsx3
from random import choice
import speech_recognition as srgit
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import configparser
import pyaudio

class Assistans:

    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()
    # Инициализация get_default_config()
    config_dict['language'] = 'ru'
    # установка языка

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.text = ''

        self.cmds = {
            ('текущее время', 'который час', 'сейчас времени'): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'вырубайся'): self.quite,
            ('выключи комп', 'выруби компьютер'): self.shut,
            ('погода', 'какая погода', 'погода сейчас', 'какая погода на улице'): self.weather,
        }

        self.ndels = ['морган', 'морген', 'моргэн', 'морг', 'ладно', 'не могла бы ты', 'пожалуйста', 'текущее', 'сейчас']

        self.commands =[
            'текущее время', 'который час', 'сейчас времени'
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй'
            'пока', 'вырубайся'
            'выключи комп', 'выруби компьютер'
            'погода', 'какая погода', 'погода сейчас', 'какая погода на улице'
        ]

        self.num_task = 0
        self.j = 0
        self.ans = ''

    def cleaner(self, text):
        self.text = text
        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k >70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):
            self.opener(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()

        self.engine.runAndWait()
        self.engine.stop()

    def time(self):
        now = datetime.datetime.now()
        self.talk('Сейчас' + str(now.hour) + ":" + str(now.minute))

    def opener(self, task):
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com',
            ('vk', 'вк', 'в контакте', 'контакт') : 'https:vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('insta', 'instagram', 'инсту', 'инста'): 'https://www.instagram.com/',
            ('gmail', 'почта', 'почту', 'гмейл', 'гмеил', 'гмайл'): 'https://gmail.com',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', '')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            self.talk('Открываю' + double_task[i])
                            j = 1
                            break


    def cfile(self):
        try:
            cfr = Assistans.settings['SETTINGS']['fr']
            if cfr != 1:
                file = open('settings.ini', 'w', encoding='UTF-8')
                file.write('[SETTINGS]\nplace = Minsk\nfr = 1')
                file.close()
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\nplace = Minsk\nfr = 1')
            file.close()


    def quite(self):
        self.talk(choice(['До скорой встречи', 'Рада была помочь', 'пока', 'я отключаюсь']))
        self.engine.stop()
        system('cls')
        sys.exit(0)

    def shut(self):
        self.talk("Подтвердите действие!")
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, 'подтверждаю') > 60):
            self.talk('действие подтверждено')
            self.talk('да скорых встреч!')
            system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(text, 'отмена')> 60:
            self.talk('действие не подтверждено')
        else:
            self.talk('действие не подтверждено')

    def hello(self):
        self.talk(choice(['привет, чем могу помочь?', 'здравствуйте', 'приветствую']))

    def weather(self):
        place = Assistans.settings['SETTINGS']['place']
        country = Assistans.settings['SETTINGS']['country']
    # Переменная для записи страны/кода страны
        country_and_place = place + ", " + country
    # запись города строны в одну переменную через запятую
        owm = OWM('fd5321547e631b45b33d6d1cc673754f')
    # ключ с сайта open weather map
        mgr = owm.weather_manager()
    # инициализация owm.weather_manager
        observation = mgr.weather_at_place(country_and_place)
    # инициализация mgr.weather_at_place и передача в качестве параметра туда страну и город

        w = observation.weather

        status = w.detailed_status
    # узнаем статус погоды в городе и записываем в пкременную status
        w.wind()
    # узнаум скорость ветра
        humidity = w.humidity
    # узнаем влажность
        temp = w.temperature('celsius')['temp']
    # узнаем температуру в градусах по цельсию
        self.talk("В городе" + str(place) + "сейчас" + str(status) +
        "\nтемпература" + str(round(temp)) + "градусов по цельсию" +
        "\nВлажность составляет" + str(humidity) + "%" +
        "\nСкорость ветра" + str(w.wind()['speed']) + "метров в секунду")

    # выводим город и статус погоды

    def talk(self,text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print(colorama.Fore.LIGHTGREEN_EX + 'Я вас слушаю....')
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                self.text = self.r.recognize_google(audio,language="ru-Ru").lower()
            except Exception as e:
                print(e)
            return  self.text

Assistans().cfile()


while True:
    Assistans().recognizer()