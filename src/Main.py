from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.animation import Animation
from kivy_garden.mapview import MapView, MapMarker
from kivy_garden.mapview.downloader import Downloader
from kivy.uix.screenmanager import ScreenManager, Screen
import time
import json


# Конфигурация
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')

# Размер окна
from kivy.core.window import Window
Window.size = (480, 850)

# Данные
try:
    with open("Landmarks.json", 'r', encoding='utf-8') as file:
        LANDMARKS = json.load(file)
except Exception as error:
    print(f"Ошибка загрузки данных: {error}")
    LANDMARKS = []
    
# Ограничение FPS
Config.set('graphics', 'maxfps', 30)  

# Уменьшение логов
Config.set('kivy', 'log_level', 'warning')  

# Ограничение одновременных запросов
Downloader.concurrent_limit = 3  



# Экран заставки
class SplashScreen(Screen):
    def on_enter(self):
        # Запуск анимации через небольшой таймаут
        Clock.schedule_once(self.start_animation, 0.1)

    def start_animation(self, dt):
        anim = (
            Animation(opacity=1, duration=2)
        )
        anim.start(self.ids.logo)
        Clock.schedule_once(self.slash_animation_1, 2)

    def slash_animation_1(self, *args):
        anim = (
        Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.slash)
        Clock.schedule_once(self.slash_delete_animation, 0.5)
        
    def slash_delete_animation(self, *args):
        anim = (
            Animation(opacity=0, duration=0)
        )
        anim.start(self.ids.slash)
        Clock.schedule_once(self.slash_animation_2, 0.5)

    def slash_animation_2(self, *args):
        anim = (
        Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.slash)
        Clock.schedule_once(self.slash_delete_animation_2, 0.5)
        
    def slash_delete_animation_2(self, *args):
        anim = (
            Animation(opacity=0, duration=0)
        )
        anim.start(self.ids.slash)
        Clock.schedule_once(self.start_animation_2)
    
    def start_animation_2(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_1)
        Clock.schedule_once(self.start_animation_3, 0.05)
        
    def start_animation_3(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_2)
        Clock.schedule_once(self.start_animation_4, 0.05)    
    
    def start_animation_4(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_3)
        Clock.schedule_once(self.start_animation_5, 0.05)

    def start_animation_5(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_4)
        Clock.schedule_once(self.start_animation_6, 0.05)  

    def start_animation_6(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_5)
        Clock.schedule_once(self.start_animation_7, 0.05) 

    def start_animation_7(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_6)
        Clock.schedule_once(self.start_animation_8, 0.05)
        
    def start_animation_8(self, *args):
        anim = (
            Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.word_7)
        Clock.schedule_once(self.close_slash_animation_1, 0.1)
        
        
    def close_slash_animation_1(self, *args):
        anim = (
        Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.close_slash)
        Clock.schedule_once(self.close_slash_delete_animation, 0.5)
        
    def close_slash_delete_animation(self, *args):
        anim = (
            Animation(opacity=0, duration=0)
        )
        anim.start(self.ids.close_slash)
        Clock.schedule_once(self.close_slash_animation_2, 0.5)

    def close_slash_animation_2(self, *args):
        anim = (
        Animation(opacity=1, duration=0)
        )
        anim.start(self.ids.close_slash)
        Clock.schedule_once(self.close_slash_delete_animation_2, 0.5)
        
    def close_slash_delete_animation_2(self, *args):
        anim = (
            Animation(opacity=0, duration=0)
        )
        anim.start(self.ids.close_slash)
        Clock.schedule_once(self.switch_to_main, 1)
        

    def switch_to_main(self, dt):
        self.manager.current = 'main'




#Обновление маркеров
class FixedSizeMapMarker(MapMarker):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        self.mapview = None
        self.size_hint = (None, None)
        self.size = (30, 30)
        
        Clock.schedule_once(self.setup_binding, 0.1)
        
    def setup_binding(self, dt):
        if self.parent and self.parent.parent:
            self.mapview = self.parent.parent
            self.mapview.bind(
                zoom=self.reposition,
                on_map_relocated=self.reposition
            )
            self.reposition()

    def reposition(self):
        if not self.mapview:
            return

        bbox = self.mapview.bbox
        if (bbox[2] - bbox[0]) == 0 or (bbox[3] - bbox[1]) == 0:
            return

        x = ((self.lon - bbox[0]) / (bbox[2] - bbox[0])) * self.mapview.width
        y = ((self.lat - bbox[1]) / (bbox[3] - bbox[1])) * self.mapview.height
        
        self.pos = (x - self.width/2, y - self.height/2)

# Главный экран
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Карта
        Clock.schedule_once(self.init_map, 0.1)

        #Добовление виджетов
        Clock.schedule_once(self.init_ui, 0.1)

        
    def init_ui(self, dt):
        
        #Функция Поиска:
        self.ids.text_input.bind(text=self.on_search)  
              
        #Добавление достопримечательностей
        self.atractions_list = []    
            
        self.data = LANDMARKS.copy()
        self.atractions_list = [item["name"].lower() for item in self.data]
        
        #Сорировка достопримечательностей
        self.update_atractions_list() 
        

    def init_map(self, dt):

        self.ids.mapview.center_on(
                54.314,
                48.403
        )
        self.markers = []
        self.add_markers()
            


        #Добовление маркеров:
    def add_markers(self):        
        for landmark in LANDMARKS:  
            marker = FixedSizeMapMarker(
                lat=landmark["lat"],
                lon=landmark["lon"],
                source=landmark["mark"]
            )
            
            self.mapview.add_marker(marker)
            self.markers.append(marker)

    def focus_on_marker(self, data):
        lat = data["lat"]
        lon = data["lon"]
        self.mapview.center_on(lat, lon) 
        self.mapview.zoom = 16 
        
        #Поиск
    def on_search(self, value, instance):
        from kivy.clock import Clock
        self.update_atractions_list(value)
        
    #Отоброжение информации:
    def show_info(self, widget):
                  
        for item in self.data:
            if item["name"].lower() == widget.data["name"].lower():  
                if widget.showing_info:
                    widget.ids.label.text = item["name"]
                    widget.showing_info = False
                else:
                    widget.ids.label.text = item["info"]
                    widget.showing_info = True
                break 
            
            #Обновление и сортировка виджетов
    def update_atractions_list(self, searc_text=''):
        container = self.atraction_container
        container.clear_widgets()
        
        search_text = self.text_input.text.lower()
        
        #Сортировка:
        filtered = sorted(
        [item for item in self.data if search_text in item["name"].lower()],
        key=lambda x: x["name"]
        )
    
        #Фильтруем:
        for item in filtered: 
            attraction = Factory.AttractionItem()
            attraction.ids.label.text = item["name"]
            attraction.data = item
            container.add_widget(attraction)  
                 
# Менеджер экранов
class Manager(ScreenManager):
    pass

# Приложение
class MapApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Manager()

if __name__ == '__main__':
    MapApp().run()
