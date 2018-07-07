# -*- coding: utf-8 -*-
from chatterbot import ChatBot

# Create a new chat bot named Charlie

class Meseek(ChatBot):
    DIALOG = [
                 "Salut",
                 "Salut mec !",
                 "Ca va ?",
                 "OKLM"
                 ]


    def __init__(self, userId):
        super().__init__(userId, trainer='chatterbot.trainers.ListTrainer')
        super().train(self.DIALOG)

