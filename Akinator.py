#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run with python 03_...py --qi-url="tcp://ip_robot:9559"

import qi
import requests
import time
import sys
import argparse


class AkinatorModule:
    """
    Wow, there should be some doc here too
    """
    def __init__(self, session):
        """
        """
        print ("Akinator Module init")
        self.session = session
        # Animated speech
        self.animated_speech = self.session.service("ALAnimatedSpeech")
        # Init ALMemory service
        self.memory = self.session.service("ALMemory")
        self.subscriberDialog = self.memory.subscriber("AkinatorDialog/answer")
        self.subscriberDialog.signal.connect(self.on_event_click)
        # TODO: Mettre une autre API
        self.url = "http://api.openweathermap.org/data/2.5/weather?id=6454573&APPID=49b584e311c58fa09794e5e25a19d1af&UNITS=metric"

        # Init ALDialog service
        try:
            self.ALDialog = session.service("ALDialog")
            self.ALDialog.resetAll()
            self.ALDialog.setLanguage("French")
            # Loading the topics directly as text strings
            self.topic_name = self.ALDialog.loadTopic("/home/nao/.local/share/PackageManager/apps/Akinator/topfiles/Akinator.top")

            # Activating the loaded topics
            self.ALDialog.activateTopic(self.topic_name)

            # Starting the dialog engine - we need to type an arbitrary string as the identifier
            # We subscribe only ONCE, regardless of the number of topics we have activated
            self.ALDialog.subscribe('AkinatorDialog')

        except Exception as e:
            print ("Error was: ", e)

        # Init ALTabletService.
        self.tabletService = session.service("ALTabletService")
        self.tabletService.loadApplication("Akinator")
        self.tabletService.cleanWebview()
        self.tabletService.reloadPage(1)
        self.tabletService.showWebview()


        # Connect the event callback.
        self.subscriber = self.memory.subscriber("answer")
        self.subscriber.signal.connect(self.on_event_vocal)

    def on_event_vocal(self, value):
        """
        Callback for answers in Dialog
        """
        print ("Understood: " + value)
        self.animated_speech.say("Tu as dit " + value)

    def on_event_click(self, value):
        """
        Callback for answers on click
        """
        print ("Cliques sur :", value)
        self.animated_speech.say("Tu as dit " + value)


    def get_api_info(self):
        """
        """
        info = requests.get(self.url)

        info_json = info.json()
        print ("info_json: %s" % info_json)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print ("Starting HumanGreeter")
        try:
            while True:
                fi = raw_input('H: ')
                #print fi
                self.ALDialog.forceInput(fi)
                self.ALDialog.forceOutput()
                time.sleep(1)
        except KeyboardInterrupt:
            print ("Interrupted by user, stopping HumanGreeter")

            # stopping the dialog engine
            self.ALDialog.unsubscribe('ExampleDialog')
            # Deactivating the topic
            self.ALDialog.deactivateTopic(self.topic_name)
            # now that the dialog engine is stopped and there are no more activated topics,
            # we can unload our topic and free the associated memory
            self.ALDialog.unloadTopic(self.topic_name)
            #stop
            sys.exit(0)


def main():
    """
    Init Akinator Module and registers it
    """

    app = qi.Application(url="tcp://10.50.90.103:9559")
    app.start()

    s = app.session
    my_module = AkinatorModule(s)
    s.registerService("Akinator", my_module)

    app.run()

if __name__ == "__main__":
    main()