import base64
import uuid
from fastapi import APIRouter, Body
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Goals import Add_Goal,Delete_Old_Image,Check_Goal,delete_Goal_data, retrieve_all_Goals, retrieve_Goal_by_id, update_Goal
from Server.Models.Goal import Goals
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Goal")
async def add_Goals_data(schema: Goals = Body(...)):
    schema = jsonable_encoder(schema)
    Goal = await Check_Goal(schema)
    if Goal==False:
        return {"code": 200, "Msg":"Goals already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Goal(schema)
    return {"code": 200, "Msg": Output}


@router.get("/", response_description="Get all Goals")
async def get_all_Goals():
    Goals = await retrieve_all_Goals()
    if Goals:
        return {"code": 200, "Data": Goals}
    return {"Data": Goals, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Goal data by id")
async def get_Goal_data(id):
    data = await retrieve_Goal_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Goal data by id")
async def delete_Goal(id: str):
    data = await delete_Goal_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Goal_data(id: str, req: Goals = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    flags=0
    if len(req["IMAGE"])!=0:
        Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_Goal = await update_Goal(id, req,flags)
    if updated_Goal:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }
