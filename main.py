from kivy.app import App
from PIL import ImageFilter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.label import Label
import os
from PIL import Image
from kivy.uix.slider import Slider
import numpy as np


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)



class Container(GridLayout):

    input_img = ObjectProperty()
    output_img = ObjectProperty()
    input_img_box = ObjectProperty()
    output_img_box = ObjectProperty()
    slider_box = ObjectProperty()
    save_button_box = ObjectProperty() 
    slider_label = ObjectProperty()
    slider = ObjectProperty()
    is_loaded = False
    k = 0

    def pix_transform(self, value):
        if value < 30:
            return 0
        elif 30 <= value < 75:
            return 51
        elif 75 <= value < 125:
            return 102
        elif 125 <= value < 180:
            return 153
        elif 180 <= value < 230:
            return 204
        else:
            return 255

    def slide(self):
        img = Image.open(r'.\Temp\Temp1.jpg')
        self.slider_label.text = f'Количество кубиков {int(self.slider.value*self.slider.value/self.k)}'
        size_lst = [int(self.slider.value), int(self.slider.value/self.k)]
        size = tuple(size_lst)
        img.resize(size).convert('L').filter(ImageFilter.EDGE_ENHANCE).save(r'.\Temp\Temp.jpg')
        for i in range(img.width):
            for x in range(img.height):
                pix = img.getpixel((i, x))
                img.putpixel((i, x), self.pix_transform(pix))
        self.output_img.source = r'.\Temp\Temp.jpg'
        self.output_img.reload()


    def convert_to_box(self):
        img = Image.open(r'.\Temp\Temp.jpg')
        new_img = Image.new(mode = "RGBA", size=(img.width*100,img.height*100))
        img_1 = Image.open(r'.\pictures\small_1.png')
        img_2 = Image.open(r'.\pictures\small_2.png')
        img_3 = Image.open(r'.\pictures\small_3.png')
        img_4 = Image.open(r'.\pictures\small_4.png')
        img_5 = Image.open(r'.\pictures\small_5.png')
        img_6 = Image.open(r'.\pictures\small_6.png')
        for i in range(img.width):
            for x in range(img.height):
                box = (i*100-100, x*100-100, i*100-1, x*100-1)
                if img.getpixel((i, x)) < 30:
                    new_img.paste(img_1, box)
                elif 30 <= img.getpixel((i, x)) < 75:
                    new_img.paste(img_2, box)
                elif 75 <= img.getpixel((i, x)) < 125:
                    new_img.paste(img_3, box)
                elif 125 <= img.getpixel((i, x)) < 180:
                    new_img.paste(img_4, box)
                elif 180 <= img.getpixel((i, x)) < 230:
                    new_img.paste(img_5, box)
                else:
                    new_img.paste(img_6, box)
        new_img.show()

                    
        

    def dismiss_popup(self):
        self._popup.dismiss()

        
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        self.input_img.source = os.path.join(path, filename[0])
        self._popup.dismiss()
        img = Image.open(os.path.join(path, filename[0]))
        self.input_img_box.opacity = 1
        self.output_img_box.opacity = 1
        self.slider_box.opacity = 1
        self.save_button_box.opacity = 1
        width = img.width
        height = img.height
        self.k = width/height
        img.convert('L').resize((100, int(100/self.k))).save(os.path.join(r'.\Temp\Temp1.jpg'))
        max_value = 100
        self.slider.max = max_value
        self.slider.value = max_value
        self.slider_label.text = f'Количество кубиков {100*int(100/self.k)}'
        self.output_img.source = r'.\Temp\Temp1.jpg'
        self.output_img.reload()



class ImgTransferApp(App):
    def build(self):
        return Container()

Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    ImgTransferApp().run()