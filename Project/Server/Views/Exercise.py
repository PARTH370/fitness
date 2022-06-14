import base64
import uuid
from fastapi import APIRouter, Body
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Exercise import Add_Exercise,Delete_Old_Image,Check_Exercises, delete_exercise_data, retrieve_all_Exercises, retrieve_exercise_by_id, update_exercise
from Server.Models.Exercise import Exercise
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Exercise")
async def add_exercise_data(schema: Exercise = Body(...)):
    schema = jsonable_encoder(schema)
    Exercises= await Check_Exercises(schema)
    if Exercises==False:
        return {"code": 200, "Msg":"Exercise already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Exercise(schema)
    return {"code": 200, "Msg": Output}


@router.get("/", response_description="Get all Exercises")
async def get_all_Exercises():
    workout = await retrieve_all_Exercises()
    if workout:
        return {"code": 200, "Data": workout}
    return {"Data": workout, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Exercise data by id")
async def get_exercise_data(id):
    data = await retrieve_exercise_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Exercise data by id")
async def delete_exercise(id: str):
    data = await delete_exercise_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_exercise_data(id: str, req: Exercise = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    flags=0
    if len(req["IMAGE"])!=0:
        Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_exercise = await update_exercise(id, req,flags)
    if updated_exercise:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }
