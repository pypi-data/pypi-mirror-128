from collections import defaultdict
from digitalguide.standardinteraktion.Action import readActions
from digitalguide.standardinteraktion.Interaktion import Interaktion
from digitalguide.standardinteraktion.Trigger import readTriggers


class Weg(Interaktion):
    def __init__(self, poi_name, interaktion_dict):
        self.typ = "Weg"
        self.name = poi_name

        self.action = self.generate_actions()
        self.states = self.generate_states()
        self.uebertrag_actions = []
        self.next_interaktion = ""

        self.action_requirements = []        

    def generate_states(self):
        states = defaultdict(list)
        # Trigger navigation
        if "trigger_navigation" in self.interaktion_dict.keys():
            trigger_navigation = self.interaktion_dict["trigger_navigation"]
        else:
            trigger_navigation = [("Liste", "Wohin")]
            print(
                "Info: {} hat keinen Trigger navigation - der Standardwert wird benutzt.".format(self.name))

        # Trigger weiter
        if "trigger_weiter" in self.interaktion_dict.keys():
            trigger_weiter = self.interaktion_dict["trigger_weiter"]
        else:
            trigger_weiter = [("Liste", "Weiter")]
            print(
                "Info: {} hat keinen Trigger weiter - der Standardwert wird benutzt.".format(self.name))

        states["{}_WEG".format(self.name.upper())] = readTriggers(trigger_navigation, "{}_navigation".format(self.name)) \
            + readTriggers(trigger_weiter, self.next_interaktion) \
            + [{"handler": "TypeHandler", "type": "Update",
                "action": self.tipp_action}]

        return states

    def generate_actions(self):
        # Weg
        if "Weg" in self.interaktion_dict.keys():
            self.action["{}_weg".format(self.name)] = readActions(self.interaktion_dict["Weg"]
                                                                + [("Return", "{}_WEG".format(self.name.upper()))])
        else:
            print("Error: {} hat keinen Weg.".format(self.name))

        # Navigation
        if "Navigation" in self.interaktion_dict.keys():
            self.action["{}_navigation".format(self.name)] = readActions(
                self.interaktion_dict["Navigation"])
        else:
            print("Error: {} hat keine Navigation.".format(self.name))

        # Tipp
        if "Tipp" in self.interaktion_dict.keys():
            self.action["{}_tipp".format(self.name)] = readActions(
                self.interaktion_dict["Tipp"])
            self.tipp_action = "{}_tipp".format(self.name)
        else:
            self.tipp_action = "weiter_wohin_tipp"
            self.action_requirements.append("weiter_wohin_tipp")
            print(
                "Info: {} hat keinen Tipp. - Standardwert weiter_wohin_tipp wird benutzt.".format(self.name))