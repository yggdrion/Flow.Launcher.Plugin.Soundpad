# -*- coding: utf-8 -*-

import json
import sys
import os


parent_folder_path = os.path.abspath(os.path.dirname(__file__))
for folder in ["", "lib", "plugin"]:
    sys.path.append(os.path.join(parent_folder_path, folder))

from flowlauncher import FlowLauncher  # noqa: E402
import webbrowser  # noqa: E402
import requests  # noqa: E402

from soundpadrc import Soundpad
sp = Soundpad()


class SoundpadSearch(FlowLauncher):
    def query(self, query): # type: ignore
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
            response = sp.query_sounds(query)
        except requests.RequestException:
            return [
                {
                    "Title": "Unable to fetch sounds",
                    "SubTitle": "Network issue or server unavailable",
                    "IcoPath": "Images/app.png",
                }
            ]
        categories = response
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
        sp.query_id_set(cat_id)


if __name__ == "__main__":
    SoundpadSearch()
