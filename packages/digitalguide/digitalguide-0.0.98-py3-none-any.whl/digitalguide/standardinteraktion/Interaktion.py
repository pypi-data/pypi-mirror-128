
from collections import defaultdict
from digitalguide.standardinteraktion.Action import readActions
from digitalguide.standardinteraktion.Trigger import readTriggers


class Interaktion:
    def __init__(self, name, typ, states, actions, uebertrag_actions, next_interaktion, action_requirements):
        self.name = name
        self.typ = typ
        self.states = states
        self.actions = actions
        self.uebertrag_actions = uebertrag_actions
        self.next_interaktion = next_interaktion

        self.action_requirements = action_requirements

    @classmethod
    def from_excel_dict(cls, excel_dict_item):
        actions = defaultdict(list)
        states = defaultdict(list)
        action_requirements = []

        poi_interaction, interaktion_dict = excel_dict_item
        poi_name, interaction_typ = poi_interaction

        if "Next" in interaktion_dict.keys():
            weiter_dict = dict((x, y) for x, y in interaktion_dict["Next"])
            next_interaktion = "{}_{}".format(
                weiter_dict["POI"], weiter_dict["Aktion"])
            action_requirements.append(next_interaktion)

        else:
            next_interaktion = None

        if interaction_typ == "Aktion":
            print(interaktion_dict)
            actions["{}".format(poi_name)] = readActions(
                interaktion_dict["Aktion"])

        elif interaction_typ == "Datenabfrage":
            actions["{}_frage".format(poi_name)] = readActions(interaktion_dict["Frage"]
                                                               + [("Return", "{}_FRAGE".format(poi_name.upper()))])
            actions["{}_tipp".format(poi_name)] = readActions(
                interaktion_dict["Tipp"])

            states["{}_FRAGE".format(poi_name.upper())] = readTriggers(interaktion_dict["Typ"], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update",
                    "action": "{}_tipp".format(poi_name)}]

        elif interaction_typ == "Weg":
            # Weg
            if "Weg" in interaktion_dict.keys():
                actions["{}_weg".format(poi_name)] = readActions(interaktion_dict["Weg"]
                                                                 + [("Return", "{}_WEG".format(poi_name.upper()))])
            else:
                print("Error: {} hat keinen Weg.".format(poi_name))

            # Navigation
            if "Navigation" in interaktion_dict.keys():
                actions["{}_navigation".format(poi_name)] = readActions(
                    interaktion_dict["Navigation"])
            else:
                print("Error: {} hat keine Navigation.".format(poi_name))

            # Tipp
            if "Tipp" in interaktion_dict.keys():
                actions["{}_tipp".format(poi_name)] = readActions(
                    interaktion_dict["Tipp"])
                tipp_action = "{}_tipp".format(poi_name)
            else:
                tipp_action = "weiter_wohin_tipp"
                action_requirements.append("weiter_wohin_tipp")
                print(
                    "Info: {} hat keinen Tipp. - Standardwert weiter_wohin_tipp wird benutzt.".format(poi_name))

            # Trigger navigation
            if "trigger_navigation" in interaktion_dict.keys():
                trigger_navigation = interaktion_dict["trigger_navigation"]
            else:
                trigger_navigation = [("Liste", "Wohin")]
                print(
                    "Info: {} hat keinen Trigger navigation - der Standardwert wird benutzt.".format(poi_name))

            # Trigger weiter
            if "trigger_weiter" in interaktion_dict.keys():
                trigger_weiter = interaktion_dict["trigger_weiter"]
            else:
                trigger_weiter = [("Liste", "Weiter")]
                print(
                    "Info: {} hat keinen Trigger weiter - der Standardwert wird benutzt.".format(poi_name))

            states["{}_WEG".format(poi_name.upper())] = readTriggers(trigger_navigation, "{}_navigation".format(poi_name)) \
                + readTriggers(trigger_weiter, next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update",
                    "action": tipp_action}]

        elif interaction_typ == "Quizfrage":
            actions["{}_frage".format(poi_name)] = readActions(
                interaktion_dict["Frage"] + [("Return", "{}_FRAGE".format(poi_name.upper()))])

            actions["{}_tipp".format(poi_name)] = readActions(
                interaktion_dict["Tipp"])

            for aktion, aktion_list in interaktion_dict.items():
                if aktion.startswith("antwort_"):
                    actions["{}_{}".format(poi_name, aktion)] = readActions(aktion_list) \
                        + readActions(interaktion_dict["Aufloesung"]) \
                        + readActions([("Return", "{}_AUFLOESUNG".format(poi_name.upper()))])

                elif aktion.startswith("trigger_"):
                    states["{}_FRAGE".format(poi_name.upper())] += readTriggers(
                        aktion_list, "{}_{}".format(poi_name, aktion.replace("trigger_", "antwort_")))

            states["{}_AUFLOESUNG".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction_typ == "Schätzfrage":
            actions["{}_frage".format(poi_name)] = readActions(
                interaktion_dict["Frage"] + [("Return", "{}_FRAGE".format(poi_name.upper()))])

            actions["{}_aufloesung".format(poi_name)] = readActions(interaktion_dict["Aufloesung"]) \
                + readActions([("Return", "{}_AUFLOESUNG".format(poi_name.upper()))])

            actions["{}_tipp".format(poi_name)] = readActions(
                interaktion_dict["Tipp"])

            if interaktion_dict["Typ"][0][0] == "Jahreszahl":
                states["{}_FRAGE".format(poi_name.upper())] = (readTriggers([("Regex", "^(\d{1,4})$")], "{}_aufloesung".format(poi_name))) \
                    + [{"handler": "TypeHandler", "type": "Update",
                        "action": "{}_tipp".format(poi_name)}]

            elif interaktion_dict["Typ"][0][0] == "Prozentzahl":
                states["{}_FRAGE".format(poi_name.upper())] = (readTriggers([("Regex", "(\d{1,2}),? ?(\d{,2})")], "{}_aufloesung".format(poi_name))) \
                    + [{"handler": "TypeHandler", "type": "Update",
                        "action": "{}_tipp".format(poi_name)}]

            elif interaktion_dict["Typ"][0][0] == "Römische Jahreszahl":
                states["{}_FRAGE".format(poi_name.upper())] = (readTriggers([("Regex", "^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")], "{}_aufloesung".format(poi_name))) \
                    + [{"handler": "TypeHandler", "type": "Update",
                        "action": "{}_tipp".format(poi_name)}]

            else:
                print("Der Schätzfragentyp {} ist nicht bekannt!".format(
                    interaktion_dict["Typ"][0][0]))

            states["{}_AUFLOESUNG".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction_typ == "Listenfrage":
            actions["{}_frage".format(poi_name)] = readActions(
                interaktion_dict["Frage"] + [("Return", "{}_FRAGE".format(poi_name.upper()))])

            answer_id_name_list = []
            for aktion, aktion_list in interaktion_dict.items():
                if aktion.startswith("antwort_"):
                    actions["{}_{}".format(poi_name, aktion)] = readActions([("Formel", "function: check_in_context\nkey: {}\nvalue: {}\ndoppelte_antwort: {}\n".format(poi_name, aktion.replace("antwort_", ""), interaktion_dict["doppelte Antwort"][0][1]))])\
                        + readActions([("Formel", "function: append_to_context\nkey: {}\nvalue: {}".format(poi_name, aktion.replace("antwort_", "")))])\
                        + readActions(aktion_list) \
                        + readActions(interaktion_dict["richtig Antwort"])

                elif aktion.startswith("trigger_"):
                    states["{}_FRAGE".format(poi_name.upper())] += readTriggers(
                        aktion_list, "{}_{}".format(poi_name, aktion.replace("trigger_", "antwort_")))

                elif aktion.startswith("name_"):
                    answer_id_name_list.append(
                        [aktion.replace("name_", ""), aktion_list[0][1]])

            actions["{}_aufloesung".format(poi_name)] = [{"type": "function", "func": "eval_list", "answer_id_name_list": answer_id_name_list, "poi": poi_name, "response_text": interaktion_dict["response_text"][0][1]}]\
                + readActions(interaktion_dict["Aufloesung"]) \
                + readActions([("Return", "{}_AUFLOESUNG".format(poi_name.upper()))])

            actions["{}_falsche_antwort".format(poi_name)] = readActions(
                interaktion_dict["falsch Antwort"])

            states["{}_FRAGE".format(poi_name.upper())] += readTriggers([("Liste", "Weiter")], "{}_aufloesung".format(poi_name))\
                + [{"handler": "TypeHandler", "type": "Update",
                    "action": "{}_falsche_antwort".format(poi_name)}]

            states["{}_AUFLOESUNG".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]
        elif interaction_typ == "Beteiligungsfrage":
            actions["{}_frage".format(poi_name)] = readActions(
                interaktion_dict["Frage"] + [("Return", "{}_FRAGE".format(poi_name.upper()))])
            actions["{}_tipp".format(poi_name)] = readActions(
                interaktion_dict["Tipp"])

            actions["{}_aufloesung".format(poi_name)] = readActions(
                interaktion_dict["Aufloesung"] + [("Return", "{}_AUFLOESUNG".format(poi_name.upper()))])

            states["{}_FRAGE".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + readTriggers([("Liste", "Nein")], next_interaktion) \
                + readTriggers(interaktion_dict["Typ"], "{}_aufloesung".format(poi_name)) \
                + [{"handler": "TypeHandler", "type": "Update",
                    "action": "{}_tipp".format(poi_name)}]

            states["{}_AUFLOESUNG".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction_typ == "GIF Generator":
            actions["{}_frage".format(poi_name)] = readActions(
                interaktion_dict["Frage"] + [("Return", "{}_FRAGE".format(poi_name.upper()))])

            actions["{}_tipp".format(poi_name)] = readActions(
                interaktion_dict["Tipp"])

            actions["{}_aufloesung".format(poi_name)] = readActions(
                interaktion_dict["Aufloesung"])

            states["{}_FRAGE".format(poi_name.upper())] = readTriggers([("Foto", "")], "{}_aufloesung".format(poi_name)) \
                + readTriggers([("Liste", "Weiter")], next_interaktion) \
                + readTriggers([("Liste", "Nein")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update",
                    "action": "{}_tipp".format(poi_name)}]

        elif interaction_typ == "Infostrecke":
            actions["{}_info".format(poi_name)] = readActions(
                interaktion_dict["Info"] + [("Return", "{}_INFO".format(poi_name.upper()))])

            states["{}_INFO".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction_typ == "Assoziationskette":
            actions["{}_frage".format(poi_name)] = readActions(
                interaktion_dict["Frage"] + [("Return", "{}_FRAGE".format(poi_name.upper()))])
            actions["{}_loop".format(poi_name)] = readActions(
                interaktion_dict["Loop"])
            states["{}_FRAGE".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], "{}_aufloesung".format(poi_name)) \
                + readTriggers([("Freitext", "")], "{}_loop".format(poi_name)) \
                + [{"handler": "TypeHandler", "type": "Update",
                    "action": "{}_tipp".format(poi_name)}]
            actions["{}_tipp".format(poi_name)] = readActions(
                interaktion_dict["Tipp"])
            actions["{}_aufloesung".format(poi_name)] = readActions(
                interaktion_dict["Aufloesung"] + [("Return", "{}_AUFLOESUNG".format(poi_name.upper()))])

            states["{}_AUFLOESUNG".format(poi_name.upper())] = readTriggers([("Liste", "Weiter")], next_interaktion) \
                + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        else:
            print("Der Interaktionstyp {} ist nicht bekannt!".format(interaction_typ))

        return cls(poi_name, interaction_typ, states, actions, [], next_interaktion, action_requirements)
