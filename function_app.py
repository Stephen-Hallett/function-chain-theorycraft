import azure.functions as func
import azure.durable_functions as df
from app_blueprints import bp
import logging

app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_functions(bp)

def blob2img(blob):
    hi = "there"
    # CONERT BLOB TO AN IMAGE AND RETURN NP ARRAY

def upload2cosmos(data):
    hi = "there"
    #UPSERT THE DATA TO THE DATABASE

#THIS IS WHAT IS ACTUALLY TRIGGERED BY THE USER
@app.blob_trigger(arg_name="myblob", path="durabletest",
                               connection="BlobStorageConnectionString") 
@app.durable_client_input(client_name="client")
async def blob_orchestrator(myblob: func.InputStream, client):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}")
    instance_id = await client.start_new("orchestrator", client_input=myblob)

@app.orchestration_trigger(context_name="context")
def orchestrator(context):
    myblob = context.get_input()
    path = myblob.name
    cosmos_data = {"id": path}
    image = blob2img(myblob.read())
    quality_metrics = yield context.call_activity("qualityMetrics", image)
    face_metrics = yield context.call_sub_orchestrator("faceMetrics", image)
    cosmos_data["quality_metrics"] = quality_metrics
    cosmos_data["face_metrics"] = face_metrics # THIS WILL CALL QUALITY METRICS FOR EACH FACE & GET EMBEDDING
    upload2cosmos(cosmos_data)
    all_img_in_container_in_db = True
    if all_img_in_container_in_db:
        _ = yield context.call_activity("clusterImages", None)

    return "Complete!"