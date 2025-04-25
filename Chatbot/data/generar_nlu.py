from django.core.management.base import BaseCommand
from autoaprendizaje.models import ConsultaUsuario
import yaml
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

class Command(BaseCommand):
    help = 'Genera un archivo nlu.yml actualizado, excluyendo fallbacks y agrupando frases'

    def handle(self, *args, **kwargs):
        # Paso 1: Cargar consultas válidas
        consultas = ConsultaUsuario.objects.exclude(intent='nlu_fallback')

        datos = {}
        for consulta in consultas:
            datos.setdefault(consulta.intent, []).append(f"- {consulta.mensaje}")

        # Paso 2: Procesar los mensajes fallidos
        fallbacks = ConsultaUsuario.objects.filter(intent='nlu_fallback')

        if fallbacks.exists():
            self.stdout.write("Agrupando frases no clasificadas...")
            mensajes_fallback = [fb.mensaje for fb in fallbacks]

            # Clustering usando embeddings
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(mensajes_fallback)
            n_clusters = min(5, len(mensajes_fallback))  # max 5 clusters o menos
            clustering = KMeans(n_clusters=n_clusters, random_state=42).fit(embeddings)

            for cluster_id in range(n_clusters):
                cluster_texts = [msg for idx, msg in enumerate(mensajes_fallback) if clustering.labels_[idx] == cluster_id]
                if cluster_texts:
                    nuevo_intent = f"nuevo_intent_cluster_{cluster_id}"
                    ejemplos = [f"- {texto}" for texto in cluster_texts]
                    datos.setdefault(nuevo_intent, []).extend(ejemplos)

        # Paso 3: Generar nlu.yml
        estructura = {"version": "3.1", "nlu": []}
        for intent, ejemplos in datos.items():
            estructura["nlu"].append({
                "intent": intent,
                "examples": "\n".join(ejemplos)
            })

        with open("data/nlu_auto.yml", "w", encoding="utf-8") as file:
            yaml.dump(estructura, file, allow_unicode=True)

        self.stdout.write(self.style.SUCCESS('Archivo nlu_auto.yml generado exitosamente.'))
