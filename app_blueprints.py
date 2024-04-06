import logging
import azure.functions as func
import azure.durable_functions as df
import numpy as np

bp = df.Blueprint()



#THIS IS A RANDOM FUNCTION THAT IS BEING CALLED BY ORCHESTRATOR
@bp.activity_trigger(input_name="image")
def qualityMetrics(image: np.ndarray) -> dict:
    return {"quality":"metrics"}

@bp.orchestration_trigger(input_name="image")
def faceMetrics(context) -> dict:
    image = context.get_input()
    model = "MTCNN MODEL"
    embeddingmodel = "EMBEDDING MODEL"
    faces = yield context.call_activity("extractFaces", image, model)
    for x,y,w,h in faces:
        face_quality = yield context.call_activity("qualityMetrics", image[x:x+h, y:y+w])
        embedding = yield context.call_activity("getEmbedding", image[x:x+h, y:y+w], embeddingmodel)
    return {"face":"metrics"}

    
@bp.activity_trigger(input_name="image")
def extractFaces(image: np.ndarray, model) -> list:
    faces = model.detect_faces(image)

@bp.activity_trigger(input_name="image")
def getEmbedding(image: np.ndarray, embeddingmodel) -> list:
    get="embedding"

@bp.activity_trigger(input_name="cosmos")
def clusterImages(cosmos) -> None:
    #COSMOS IS A CONNECTION TO  DB
    #READ ALL DOCS FROM DB & CLUSTER THEM
    cluster = "images"