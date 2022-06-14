from fastapi import APIRouter, Body
from Server.Database import Recipes_collection
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Recipe import Add_Recipe,Delete_Old_Image,Check_Recipe, delete_Recipes_data, retrieve_all_Recipess, retrieve_Recipes_by_id, update_Recipes
from Server.Models.Recipe import Recipe
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Recipe")
async def add_recipe_data(schema:  Recipe = Body(...)):
    schema = jsonable_encoder(schema)
    Recipes=await Check_Recipe(schema)
    if Recipes==False:
        return { "code":200,"Msg":"Recipe already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Recipe(schema)
    return {"code": 200, "Msg": Output}


@router.get("/", response_description="Get all Recipe")
async def get_all_Recipe():
    Recipe = await retrieve_all_Recipess()
    if Recipe:
        return {"code": 200, "Data": Recipe}
    return {"Data": Recipe, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Recipe data by id")
async def get_recipe_data(id):
    data = await retrieve_Recipes_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Recipe data by id")
async def delete_recipe(id: str):
    data = await delete_Recipes_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Recipe_data(id: str, req: Recipe = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    flags=0
    if len(req["IMAGE"])!=0:
        Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_Recipe = await update_Recipes(id, req,flags)
    if updated_Recipe:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }


@router.post("/{id}", response_description="Change Status of Recipe")
async def Change_Recipe_Status(id: str):
    data = await Recipes_collection.find_one({"_id":ObjectId(id)})
    if data:
        if data['STATUS'] =="Active":
            await Recipes_collection.update_one({"_id":ObjectId(id)},{"$set":{"STATUS":"Inactive"}})
        else:
            await Recipes_collection.update_one({"_id":ObjectId(id)},{"$set":{"STATUS":"Active"}})
        return {"code": 404, "Data": "Something Went Wrong"}
    return {"code": 404, "Data": "Id may not exist"}