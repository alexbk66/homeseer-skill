from mycroft import MycroftSkill, intent_file_handler


class Homeseer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('homeseer.intent')
    def handle_homeseer(self, message):
        self.speak_dialog('homeseer')


def create_skill():
    return Homeseer()

