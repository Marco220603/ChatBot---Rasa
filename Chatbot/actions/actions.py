from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
import requests
import json
import actions
from .feedback_rag import FeedbackRAG


# URLs de las APIs
DJANGO_TICKET_URL = "http://localhost:8000/api/crear_ticket/"
GPT_API_URL = "http://localhost:8000/api/gpt_response/" 
LOG_API = "http://localhost:8000/api/log_mensaje/"


class ActionDespedida(Action):
    def name(self) -> Text:
        return "action_despedida"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="¡Hasta luego! 😊 Que tengas un excelente día.")
        return []

class ActionObjetivosCurso(Action):
    def name(self) -> Text:
        return "action_objetivos_curso"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="El Taller de Proyecto busca que desarrolles habilidades para resolver problemas reales aplicando conocimientos de tu carrera.")
        return []
  
class ActionCompetenciasCurso(Action):
    def name(self) -> Text:
        return "action_competencias_curso"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Durante el curso desarrollarás competencias como trabajo en equipo, pensamiento crítico, solución de problemas, y comunicación efectiva.")
        return []

class ActionHorarioCurso(Action):
    def name(self) -> Text:
        return "action_horario_curso"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="El Taller de Proyecto I se dicta en sesiones semanales de 2 a 3 horas, según la sección. Verifica tu horario en el aula virtual.")
        return []

class ActionCreditosCurso(Action):
    def name(self) -> Text:
        return "action_creditos_curso"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="El Taller de Proyecto I y II tienen cada uno 3 créditos académicos.")
        return []

class ActionFechasEntrega(Action):
    def name(self) -> Text:
        return "action_fechas_entrega"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Las entregas principales son: Trabajo Parcial en semana 9, Trabajo Final en semana 16. Revisa el cronograma en Aula Virtual.")
        return []

class ActionProblemasTecnicos(Action):
    def name(self) -> Text:
        return "action_problemas_tecnicos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []

class ActionProcedimientoCambioTitulo(Action):
    def name(self) -> Text:
        return "action_procedimiento_cambio_titulo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Considera que para el procedimiento de cambio de título, se debe presentar un documento con el siguiente formato: https://upcedupe-my.sharepoint.com/:w:/g/personal/u20211c528_upc_edu_pe/EdPp5XDqB4tBglLukTZOiI8ByN7ieKGHwKu6jki03tbfeg?e=zPUpIv. Cuando complete el documento, contactarse con su profes@r metodológico para escalarlo con la PMO.")
        return []

class ActionFormatoObjetivosISI(Action):
    def name(self) -> Text:
        return "action_formato_objetivosISI"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Registra el objetivo general y objetivos específicos para ISI con la siguiente estructura: OBJ1 - Analizar \nOBJ2 - Diseñar \n OBJ3 - Validar \n OBJ4 - Elaborar el Plan de Continuidad.")
        return []

class ActionFormatoObjetivosSW(Action):
    def name(self) -> Text:
        return "action_formato_objetivosSW"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Registra el objetivo general y objetivos específicos para SW con la siguiente estructura: OBJ1 - Analizar \nOBJ2 - Diseñar \n OBJ3 - Desarrollar \n OBJ4 - Validar.")
        return []

class ActionFormatoMemoriaTesis(Action):
    def name(self) -> Text:
        return "action_formato_memoria_tesis"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Ingresa al siguiente enlace para obtener el formato de la memoria de Tesis: https://upcedupe-my.sharepoint.com/:w:/g/personal/u20211c528_upc_edu_pe/EdPp5XDqB4tBglLukTZOiI8ByN7ieKGHwKu6jki03tbfeg?e=zPUpIv")
        return []

class ActionConsultarArtefactosScrum(Action):
    def name(self) -> Text:
        return "action_consultar_artefactos_scrum"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text=( "Los principales artefactos Scrum que se usarán dentro del curso son: \n\n"
                                       "🔹 Daily Scrum - Reunión diaria de 15 minutos donde el equipo de desarrollo sincroniza actividades y planifica el trabajo del día.\n"
                                       "🔹 Sprint Retrospective - Reunión al final del Sprint para reflexionar sobre cómo se trabajó.\n"
                                       "🔹 Sprint Review - Reunión al final del Sprint donde se presenta el incremento al Product Owner y a los interesados.\n"
                                       " Ingresa al siguiente enlace https://upcedupe-my.sharepoint.com/:f:/g/personal/u20211c528_upc_edu_pe/EltM9v663Q9OlPdYcRBdhfgBvLINi6EQHXiZ_vS1yBgX9g?e=QjPvuI \n\n"
                                       ))
        return []

class ActionExplicarPlannerTP1(Action):
    def name(self) -> Text:
        return "action_explicar_planner_tp1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text=( "📅 El calendario del TP1 se organiza en 4 sprints y una etapa inicial llamada *Inception*. Aquí algunos puntos clave:\n\n"
                                        "🔹 **Inception (S1 a S3)**: Se asignan los clientes y portafolios, y se realiza el alineamiento del proyecto con los Outcomes ABET y competencias generales.\n"
                                        "🔹 **Sprint 1 (S4 a S6)**: Se define el *Product Backlog* (historias de usuario) y los artefactos de gestión del proyecto.\n"
                                        "🔹 **Sprint 2 (S7 a S9)**: Se presenta el *Objetivo 2* (versión 100%) y luego se realizan ajustes. También se hace la sustentación parcial.\n"
                                        "🔹 **Sprint 3 (S10 a S12)**: Se trabaja el *Objetivo 3* y se entrega el *Anexo A - WASC* junto al *Capítulo 3* del documento.\n"
                                        "🔹 **Sprint 4 (S13 a S15)**: Se elabora el *Capítulo 4*, se vincula el proyecto con los Outcomes ABET y competencias generales. También se genera el paper con el listado de aprobados.\n"
                                        "🔹 **Semana 16 y 17**: Se realiza la sustentación final, entrega de notas y cierre del proyecto.\n\n"
                                        ))
        return []

class ActionExplicarPlannerTP2(Action):
    def name(self) -> Text:
        return "action_explicar_planner_tp2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text=( "📅 El calendario del TP2 se organiza desde el Sprint 5 hasta el Sprint 9. Aquí te resumo los hitos clave:\n\n"
                                        "🟢 *Semana -1 a S1*: Se realiza la **Solicitud y Asignación de RRHH**.\n"
                                        "📘 *Sprint 5 a 7 (S1 a S8)*:\n"
                                        "  - Desarrollo del **Capítulo 2: Diseño del Proyecto**.\n"
                                        "  - Avance del **Objetivo 4 al 100%** y luego ajustes.\n"
                                        "  - Reuniones de sustentación con el **Profesor Metodológico**.\n"
                                        "📘 *Sprint 7 a 8 (S9 a S11)*:\n"
                                        "  - Se presenta la **Sustentación Parcial**.\n"
                                        "  - Desarrollo del **Capítulo 3: Validación y Resultados**.\n"
                                        "📘 *Sprint 8 (S10 a S12)*:\n"
                                        "  - Elaboración del **Capítulo 4** y **Capítulo 5**.\n"
                                        "  - Entrega de **Costos y Presupuestos**, y el **Plan de Continuidad (ISI)**.\n"
                                        "📘 *Sprint 9 (S13 a S15)*:\n"
                                        "  - Redacción de **Conclusiones y Recomendaciones**.\n"
                                        "  - **Preparación y Entrega de todos los artefactos** del proyecto.\n"
                                        "  - Registro del **Paper - Listado de Aprobados**.\n"
                                        "🟢 *Semanas 15 a 17*:\n"
                                        "  - Sustentación con el **Profesor Metodológico**.\n"
                                        "  - **Sustentación Final**.\n"
                                        "  - **Entrega de Notas**.\n\n"
                                        "Recuerda seguir el cronograma y cumplir cada entregable a tiempo. Si tienes dudas técnicas, contacta a soporte@upc.edu.pe o usa el canal de Teams. ¡Ánimo con tu proyecto! 🚀"
                                        ))
        return []

class ActionContextoSprint(Action):
    def name(self) -> Text:
        return "action_contexto_sprint"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text=( " 🌀 **¿Qué es un Sprint en el TP?**\n\n"
                                        " En el contexto de los Trabajos de Proyecto de la UPC, un **Sprint** es una unidad de tiempo, normalmente de ** 3 semanas**, en la cual debes avanzar con tareas específicas del proyecto.\n\n"
                                        " 🔍 **Características clave del Sprint:**\n"
                                        " • ⏱ *Duración:* 3 semanas.\n"
                                        " • 📌 *Inicio y fin definidos*, con entregables concretos por semana.\n"
                                        " • 📚 *Ejemplo:* En el Sprint 6 puedes estar entregando el Capítulo 2 o el Objetivo 4.\n"
                                        " • 🧑‍🏫 *Sustentaciones:* Algunos Sprints incluyen revisión con el profesor metodológico.\n"
                                        " • 🔁 *Iteración:* Se avanza, se ajusta y se mejora continuamente.\n\n"
                                        " Los Sprints te ayudan a organizar el trabajo, no dejar todo para el final y cumplir con el cronograma. 📆✅"
                                        ))
        return []

class ActionFormatoActas(Action):
    def name(self) -> Text:
        return "action_formato_acta_reunion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Las reuniones con el asesor especializado y el coautor deben evidenciarse dentro del formato de Acta de Reunión. Usa la siguiente estructura https://upcedupe-my.sharepoint.com/:w:/g/personal/u20211c528_upc_edu_pe/ETMTzMQvWB5Nio1wMh-TWwUBD1Ukf8LBVb5xk74n7Mo8nA?e=bxSOJS, recuerda que este documento debe aprobarse por tu asesor/coautor a través del correo institucional.")
        return []

class ActionContactarAsesorEspecializado(Action):
    def name(self) -> Text:
        return "action_contactar_asesor_especializado"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        data = {"sender_id": sender_id, "message": user_msg}
        try:
            requests.post(LOG_API, json=data, timeout=3)
        except Exception as e:
            print(f"❌ Error al guardar log: {e}")
        
        dispatcher.utter_message(text="Si tienes problemas técnicos, contacta al soporte técnico de la UPC o escribe a soporte@upc.edu.pe. También puedes usar el canal de Teams.")
        return []

class ActionVerificarFeedback(Action):
    def name(self) -> Text:
        return "action_verificar_feedback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        feedback = tracker.latest_message.get("text", "").lower()
        last_msg = tracker.get_slot("last_user_message")
        if "no" in feedback:
            print("❌ Usuario indicó que no se resolvió su duda. Generando ticket...")
            # Crear ticket en Django
            ticket_payload = {"descripcion": last_msg, "usuario": tracker.sender_id}
            response = requests.post(DJANGO_TICKET_URL, json=ticket_payload)
            ticket = response.json()
            ticket_id = ticket.get("ticket_id")

            dispatcher.utter_message(text=f"Se ha generado un ticket para tu caso. 🧾 Número de ticket: {ticket_id}")
            return []
        else:
            dispatcher.utter_message(text="¡Genial! Me alegra haber podido ayudarte. 🙌")
            return []

class ActionConsultarEstadoTicket(Action):
    def name(self) -> Text:
        return "action_consultar_estado_ticket"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        user_id = tracker.sender_id
        estado_response = requests.get(f"http://localhost:8000/api/tickets/estado/{user_id}/")
        data = estado_response.json()

        if not data:
            dispatcher.utter_message(text="No tienes tickets abiertos actualmente.")
        else:
            msg = "📋 Estado de tus tickets:\n"
            for ticket in data:
                msg += f"Ticket #{ticket['id']}: {ticket['estado']} - {ticket['descripcion'][:50]}...\n"
            dispatcher.utter_message(text=msg)

        return []

from rasa_sdk.events import SlotSet

class ActionResponderConGPT(Action):
    def name(self) -> Text:
        return "action_fallback_con_gpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        user_message = tracker.latest_message.get("text", "")
        sender_id = tracker.sender_id
        print(f"📥 Consulta recibida de {sender_id}: {user_message}")

        # Paso 1: Verificar si GPT puede responder directamente (check_only)
        gpt_can_answer = False
        try:
            check_payload = {"query": user_message, "check_only": True}
            check_response = requests.post(GPT_API_URL, json=check_payload, timeout=5)
            check_response.raise_for_status()
            gpt_can_answer = check_response.json().get("can_answer", False)
        except Exception as e:
            print(f"❌ Error al verificar con GPT (check_only): {e}")

        # Paso 2: Obtener contexto si GPT no puede responder directamente
        contexto = ""
        if not gpt_can_answer:
            print("🔍 Consultando FAISS por contexto adicional...")
            try:
                rag = FeedbackRAG()
                contexto = rag.search(user_message) or ""
                print(f"🧠 Contexto FAISS: {contexto[:100]}...")
            except Exception as e:
                print(f"❌ Error al consultar FAISS: {e}")

        # Paso 3: Enviar a GPT
        gpt_text = "❌ GPT no respondió."
        try:
            response = requests.post(GPT_API_URL, json={
                "query": user_message,
                "context": contexto,
                "usuario_id": sender_id
            }, timeout=10)
            response.raise_for_status()
            gpt_text = response.json().get("response", gpt_text)
            print("✅ Respuesta obtenida desde Django/GPT.")
        except Exception as e:
            print(f"❌ Error al enviar consulta a Django: {e}")

        # ✅ Enviar respuesta a Django (no directamente al usuario)
        dispatcher.utter_message(json_message={"gpt_response": gpt_text})

        # ✅ Retornar SOLO EventTypes válidos (sin custom dicts sueltos)
        return [
            SlotSet("last_user_message", user_message),
            SlotSet("last_bot_response", gpt_text)
        ]
