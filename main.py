# -*- coding: utf-8 -*-

import sys
import os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher
import webbrowser

import requests


class HelloWorld(FlowLauncher):
    def query(self, query):
        categories = {}
        response = requests.get("http://127.0.0.1:5000/soundpad/query/" + query)

        # categories look like the following
        # {
        #     "23": "57324-concerning-hobbits-lord-of-the-rings",
        #     "22": "47745-top-12-hobbit-lotr-horns"
        # }

        if query == "":
            return [
                {
                    "Title": "Search for a sound",
                    "SubTitle": "This is where your subtitle goes, press enter to open Flow's url",
                    "IcoPath": "Images/soundpad.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": [
                            "https://github.com/Flow-Launcher/Flow.Launcher"
                        ],
                    },
                }
            ]

        categories = response.json()
        results = []
        for cat_id, cat_name in categories.items():
            results.append(
                {
                    "Title": cat_name,
                    "SubTitle": "SoundId: " + cat_id,
                    "IcoPath": "Images/soundpad.png",
                    "JsonRPCAction": {
                        "method": "query_set",
                        "parameters": [cat_id],
                    },
                }
            )
        return results

    def context_menu(self, data):
        return [
            {
                "Title": "Hello World Python's Context menu",
                "SubTitle": "Press enter to open Flow the plugin's repo in GitHub",
                "IcoPath": "Images/soundpad.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": [
                        "https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"
                    ],
                },
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)

    def query_set(self, cat_id):
        requests.get("http://127.0.0.1:5000/soundpad/query-set/" + cat_id)


if __name__ == "__main__":
    HelloWorld()
