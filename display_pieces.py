from tkinter import *

class Displays():
    def __init__(self):
        self.log_text = -1
        self.log_text_window = -1

        self.objects = []

        self.port_give_text = StringVar()
        self.port_get_text = StringVar()

        self.wood_discard = StringVar()
        self.brick_discard = StringVar()
        self.sheep_discard = StringVar()
        self.wheat_discard = StringVar()
        self.stone_discard = StringVar()

        self.total_text = -1


    def add_object(self,obj):
        self.objects.append(obj)

    def destroy_objects(self):
        for obj in self.objects:
            obj.destroy()
        self.objects = []

    def get_wood_discard(self):
        try:
            value = int(self.wood_discard.get())
        except:
            value = 0
        return value

    def get_brick_discard(self):
        try:
            value = int(self.brick_discard.get())
        except:
            value = 0
        return value

    def get_sheep_discard(self):
        try:
            value = int(self.sheep_discard.get())
        except:
            value = 0
        return value

    def get_wheat_discard(self):
        try:
            value = int(self.wheat_discard.get())
        except:
            value = 0
        return value

    def get_stone_discard(self):
        try:
            value = int(self.stone_discard.get())
        except:
            value = 0
        return value
