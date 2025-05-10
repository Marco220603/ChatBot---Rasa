# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBienvenida(Action):
    def name(self) -> Text:
        return "action_bienvenida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="¡Hola! 👋 Bienvenido al asistente académico. ¿En qué puedo ayudarte hoy?")
        return []

class ActionMostrarMenu(Action):
    def name(self) -> Text:
        return "action_mostrar_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        menu = (
            "📚 Estas son algunas cosas que puedo responder:\n"
            "1️⃣ Objetivos del curso\n"
            "2️⃣ Competencias del curso\n"
            "3️⃣ Horarios\n"
            "4️⃣ Créditos\n"
            "5️⃣ Fechas de entrega\n"
            "6️⃣ Problemas técnicos\n"
            "Puedes preguntarme lo que necesites."
        )
        dispatcher.utter_message(text=menu)
        return []

class ActionDespedida(Action):
    def name(self) -> Text:
        return "action_despedida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="¡Hasta luego! 😊 Que tengas un excelente día.")
        return []

class ActionObjetivosCurso(Action):
    def name(self) -> Text:
        return "action_objetivos_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="El Taller de Proyecto busca que desarrolles habilidades para resolver problemas reales aplicando conocimientos de tu carrera.")
        return []

class ActionCompetenciasCurso(Action):
    def name(self) -> Text:
        return "action_competencias_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Durante el curso desarrollarás competencias como trabajo en equipo, pensamiento crítico, solución de problemas, y comunicación efectiva.")
        return []

class ActionHorarioCurso(Action):
    def name(self) -> Text:
        return "action_horario_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="El Taller de Proyecto I se dicta en sesiones semanales de 2 a 3 horas, según la sección. Verifica tu horario en el aula virtual.")
        return []

class ActionCreditosCurso(Action):
    def name(self) -> Text:
        return "action_creditos_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="El Taller de Proyecto I y II tienen cada uno 3 créditos académicos.")
        return []

class ActionFechasEntrega(Action):
    def name(self) -> Text:
        return "action_fechas_entrega"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Las entregas principales son: Trabajo Parcial en semana 9, Trabajo Final en semana 16. Revisa el cronograma en Aula Virtual.")
        return []

class ActionProblemasTecnicos(Action):
    def name(self) -> Text:
        return "action_problemas_tecnicos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []

