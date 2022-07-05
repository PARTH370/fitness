from sys import flags
from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Subscription import Delete_Old_Image,Check_Subscriptions, Add_Subscriptions, retrieve_all_Subscriptions, retrieve_Subscriptions_by_id, delete_Subscriptions_data, update_Subscriptions
from Project.Server.Database import Subscription_collection
from Project.Server.Models.Subscription import Subscriptions
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/Add_Subscription_Data", response_description="Add Subscriptions")
async def add_Subscription_data(schema:  Subscriptions = Body(...)):
    schema = jsonable_encoder(schema)
    Subscriptions=await Check_Subscriptions(schema)
    if Subscriptions==False:
        return { "code":200,"Msg":"Subscription already exists"}
    
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Subscriptions(schema)
    return {"code": 200, "Msg": Output}

@router.get("/Get_All_Subscriptions", response_description="Get all Subscriptions")
async def get_all_Subscriptions():
    Subscriptions = await retrieve_all_Subscriptions()
    if Subscriptions:
        return {"code": 200, "Data": Subscriptions}
    return {"Data": Subscriptions, "Msg": "Empty list return"}

@router.get("/Get_Subscriptions_Data/{id}", response_description="Get Subscriptions data by id")
async def get_Subscriptions_data(id):
    data = await retrieve_Subscriptions_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}

@router.delete("/Delete/{id}", response_description="Delete Subscriptions data by id")
async def delete_Subscriptions(id: str):
    data = await delete_Subscriptions_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}

@router.put("/Update/{id}")
async def update_Subscriptions_data(id: str, req: Subscriptions = Body(...)):
    req = jsonable_encoder(req)
    flags=0
    if len(req["IMAGE"])!=0:
        # Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_Subscriptions = await update_Subscriptions(id, req,flags)
    if updated_Subscriptions:
        return {"code": 200, "Data": "Data updated Successfully"}
    return {"code": 200, "Msg": "Id may not exist"}

@router.post("/Status/{id}",response_description="Change Subscriptions status")
async def change_Subscriptions_status(id:str):
    data = await Subscription_collection.find_one({"_id": ObjectId(id)})
    if data:
        if data['STATUS']=="ACTIVE":
            await Subscription_collection.update_one({"_id": ObjectId(id)},{'$set':{"STATUS":"INACTIVE"}})
        else:
            await Subscription_collection.update_one({"_id": ObjectId(id)},{'$set':{"STATUS":"ACTIVE"}})
        return {"code": 200, "Msg": "Status changed Successfully"}
    return {"code": 200, "Msg": "Id may not exist"}