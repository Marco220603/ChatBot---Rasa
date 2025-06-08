import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import sqlite3
from .feedback_rag import FeedbackRAG
DJANGO_API_URL = "http://localhost:8000/api/feedbackgpt/" 
OLLAMA_URL = "http://localhost:11434/api/generate"  
 
class ActionFallbackToOllama(Action):
    def name(self):
        return "action_fallback_to_ollama"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_message = tracker.latest_message.get('text')
        print(f"➡️ Recibido mensaje del usuario: {user_message}")

        # Paso 1: Buscar en FAISS
        rag = FeedbackRAG()
        respuesta_guardada = rag.search(user_message)

        if respuesta_guardada:
            print("✅ Respuesta encontrada en base de datos local")
            dispatcher.utter_message(text=respuesta_guardada)
            dispatcher.utter_message(text="¿Esta respuesta resolvió tu duda? (Responde: Sí o No)")
            return [
                SlotSet("last_user_message", user_message),
                SlotSet("last_bot_response", respuesta_guardada)
            ]

        # Paso 2: Si no hay respuesta, llamar a Ollama
        print(f"➡️ Enviando mensaje a Ollama: {user_message}")
        payload = {
            "model": "llama3:8b",
            "prompt": (
                "Eres un asistente académico de la Universidad Peruana de Ciencias Aplicadas (UPC). "
                "Solo responde preguntas relacionadas con tesis, talleres de proyecto, y normativa académica de la UPC. "
                "Si la pregunta no está relacionada, indica que no puedes responder.\n"
                f"Pregunta: {user_message}\nRespuesta:"
            ),
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=15)
            response.raise_for_status()
            gpt_response = json.loads(response.text.split('\n')[0])['response']

            print(f"✅ Respuesta de Ollama: {gpt_response.strip()}")
            dispatcher.utter_message(text=gpt_response)
            dispatcher.utter_message(text="¿Esta respuesta resolvió tu duda? (Responde: Sí o No)")
            return [
                SlotSet("last_user_message", user_message),
                SlotSet("last_bot_response", gpt_response)
            ]

        except Exception as e:
            print(f"❌ Error en llamada a Ollama: {e}")
            dispatcher.utter_message(text="Lo siento, no pude obtener una respuesta en este momento. Por favor intenta más tarde.")
            return []
        
class ActionFeedbackSatisfaction(Action):
    def name(self):
        return "action_feedback_satisfaction"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        feedback = tracker.latest_message.get('text').lower()
        user_message = tracker.get_slot("last_user_message")
        bot_response = tracker.get_slot("last_bot_response")

        if not user_message or not bot_response:
            dispatcher.utter_message(text="No tengo suficientes datos para registrar tu feedback.")
            return []

        # Construir el payload para Django
        data = {
            "user_message": user_message,
            "bot_response": bot_response,
            "satisfaction": "positive" if feedback in ["si", "sí", "yes"] else "negative"
        }

        try:
            r = requests.post(DJANGO_API_URL, json=data, timeout=10)
            r.raise_for_status()

            if data["satisfaction"] == "positive":
                dispatcher.utter_message(text="¡Gracias! Me alegra haber podido ayudarte. 🎓 Puedes hacer otra consulta si deseas.")
            else:
                dispatcher.utter_message(text="Gracias por tu comentario. Seguimos aquí para resolver tus dudas. 🙌 ¿En qué más te puedo ayudar?")

        except Exception as e:
            dispatcher.utter_message(text="Hubo un error al registrar tu feedback, pero puedes seguir consultando.")
            print(f"Error al enviar feedback a Django: {e}")

        # Limpia los slots temporales para evitar confusión en siguientes preguntas
        return [
            SlotSet("last_user_message", None),
            SlotSet("last_bot_response", None)
        ]

def guardar_mensaje(sender, text, intent):
    with sqlite3.connect("intents_usuarios.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS mensajes (sender TEXT, texto TEXT, intent TEXT)''')
        c.execute("INSERT INTO mensajes (sender, texto, intent) VALUES (?, ?, ?)", (sender, text, intent))
        conn.commit()

class BaseAction(Action):
    def name(self) -> Text:
        return "base_action"

    def save_user_message(self, tracker: Tracker):
        sender_id = tracker.sender_id #identificador unico x usuario
        last_message = tracker.latest_message.get('text')
        last_intent = tracker.latest_message.get('intent', {}).get('name', 'sin_clasificar')
        guardar_mensaje(sender_id, last_message, last_intent)

class ActionDespedida(BaseAction):
    def name(self) -> Text:
        return "action_despedida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="¡Hasta luego! 😊 Que tengas un excelente día.")
        return []

class ActionObjetivosCurso(BaseAction):
    def name(self) -> Text:
        return "action_objetivos_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="El Taller de Proyecto busca que desarrolles habilidades para resolver problemas reales aplicando conocimientos de tu carrera.")
        return []

class ActionCompetenciasCurso(BaseAction):
    def name(self) -> Text:
        return "action_competencias_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Durante el curso desarrollarás competencias como trabajo en equipo, pensamiento crítico, solución de problemas, y comunicación efectiva.")
        return []

class ActionHorarioCurso(BaseAction):
    def name(self) -> Text:
        return "action_horario_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="El Taller de Proyecto I se dicta en sesiones semanales de 2 a 3 horas, según la sección. Verifica tu horario en el aula virtual.")
        return []

class ActionCreditosCurso(BaseAction):
    def name(self) -> Text:
        return "action_creditos_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="El Taller de Proyecto I y II tienen cada uno 3 créditos académicos.")
        return []

class ActionFechasEntrega(BaseAction):
    def name(self) -> Text:
        return "action_fechas_entrega"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Las entregas principales son: Trabajo Parcial en semana 9, Trabajo Final en semana 16. Revisa el cronograma en Aula Virtual.")
        return []

class ActionProblemasTecnicos(BaseAction):
    def name(self) -> Text:
        return "action_problemas_tecnicos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []

class ActionProcedimientoCambioTitulo(BaseAction):
    def name(self) -> Text:
        return "action_procedimiento_cambio_titulo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self.save_user_message(tracker)
        dispatcher.utter_message(text="Considera que para el procedimiento de cambio de título, se debe presentar un documento con el siguiente formato: https://upcedupe-my.sharepoint.com/:w:/g/personal/u20211c528_upc_edu_pe/EdPp5XDqB4tBglLukTZOiI8ByN7ieKGHwKu6jki03tbfeg?e=zPUpIv. Cuando complete el documento, contactarse con su profes@r metodológico para escalarlo con la PMO.")
        return []

class ActionFormatoObjetivosISI(BaseAction):
    def name(self) -> Text:
        return "action_formato_objetivosISI"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self.save_user_message(tracker)
        dispatcher.utter_message(text="Registra el objetivo general y objetivos específicos para ISI con la siguiente estructura: OBJ1 - Analizar \nOBJ2 - Diseñar \n OBJ3 - Validar \n OBJ4 - Elaborar el Plan de Continuidad.")
        return []

class ActionFormatoObjetivosSW(BaseAction):
    def name(self) -> Text:
        return "action_formato_objetivosSW"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self.save_user_message(tracker)
        dispatcher.utter_message(text="Registra el objetivo general y objetivos específicos para SW con la siguiente estructura: OBJ1 - Analizar \nOBJ2 - Diseñar \n OBJ3 - Desarrollar \n OBJ4 - Validar.")
        return []
    
class ActionFormatoMemoriaTesis(BaseAction):
    def name(self) -> Text:
        return "action_formato_memoria_tesis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self.save_user_message(tracker)
        dispatcher.utter_message(text="Ingresa al siguiente enlace para obtener el formato de la memoria de Tesis: https://upcedupe-my.sharepoint.com/:w:/g/personal/u20211c528_upc_edu_pe/EdPp5XDqB4tBglLukTZOiI8ByN7ieKGHwKu6jki03tbfeg?e=zPUpIv")
        return []
    
class ActionAprobacionSolicitudCambio(BaseAction):
    def name(self) -> Text:
        return "action_aprobacion_solicitud_cambio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []

class ActionConsultarArtefactosScrum(BaseAction):
    def name(self) -> Text:
        return "action_consultar_artefactos_scrum"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Los principales artefactos Scrum que se usaran dentro del curso son: \n * Daily Scrum - Reunión diaria de 15 minutos donde el equipo de desarrollo sincroniza actividades y planifica el trabajo del día.\n * Sprint Retrospective - Reunión al final del Sprint para reflexionar sobre cómo se trabajó.\n * Sprint Review - Reunión al final del Sprint donde se presenta el incremento al Product Owner y a los interesados.\n Ingresa al siguiente enlace https://upcedupe-my.sharepoint.com/:f:/g/personal/u20211c528_upc_edu_pe/EltM9v663Q9OlPdYcRBdhfgBvLINi6EQHXiZ_vS1yBgX9g?e=QjPvuI.")
        return []

class ActionExplicarPlanner(BaseAction):
    def name(self) -> Text:
        return "action_explicar_planner"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []
    
class ActionContextoSprint(BaseAction):
    def name(self) -> Text:
        return "action_contexto_sprint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []
    
class ActionAprobacionProjectCharter(BaseAction):
    def name(self) -> Text:
        return "action_aprobacion_project_charter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []
    
class ActionContactarAsesorEspecializado(BaseAction):
    def name(self) -> Text:
        return "action_contactar_asesor_especializo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []
    
class ActionFormatoActas(BaseAction):
    def name(self) -> Text:
        return "action_formato_actas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.save_user_message(tracker)
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []