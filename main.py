# -*- coding: utf-8 -*-

import sys
import os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
for folder in ["", "lib", "plugin"]:
    sys.path.append(os.path.join(parent_folder_path, folder))

from flowlauncher import FlowLauncher
import webbrowser

import requests


class SoundpadSearch(FlowLauncher):
    def query(self, query):
        if not query:
            return [
                {
                    "Title": "Search for a sound",
                    "SubTitle": "",
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": [
                            "https://github.com/Flow-Launcher/Flow.Launcher"
                        ],
                    },
                }
            ]

        try:
            response = requests.get(f"http://127.0.0.1:5000/soundpad/query/{query}")
            response.raise_for_status()
        except requests.RequestException:
            return [{
                "Title": "Unable to fetch sounds",
                "SubTitle": "Network issue or server unavailable",
                "IcoPath": "Images/app.png"
            }]

        categories = response.json()
        results = []
        for cat_id, cat_name in categories.items():
            results.append(
                {
                    "Title": cat_name,
                    "SubTitle": "SoundId: " + cat_id,
                    "IcoPath": "Images/app.png",
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
                "IcoPath": "Images/app.png",
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
    SoundpadSearch()
