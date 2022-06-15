from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Recipes_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": str(data["TITLE"]),
        "CATEGORY": data["CATEGORY"],
        "PRICE": data["PRICE"],
        'SERVINGS': data["SERVINGS"],
        "TOTAL_TIME": data["TOTAL_TIME"],
        "FEATURED": data["FEATURED"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }

def Single_Recipes_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": str(data["TITLE"]),
        'DESCRIPTION': data["DESCRIPTION"],
        'INGREDIENTS': data["INGREDIENTS"],
        'DIRECTIONS': data["DIRECTIONS"],
        'CATEGORY': data["CATEGORY"],
        'PRICE': data["PRICE"],
        'CALORIES':data["CALORIES"] ,
        'CARBS': data["CARBS"],
        'PROTEIN': data["PROTEIN"],
        'FAT': data["FAT"],
        'SERVINGS': data["SERVINGS"],
        'TOTAL_TIME': data["TOTAL_TIME"],
        'FEATURED': data["FEATURED"],
        'STATUS': data["STATUS"],
        "IMAGE": data["IMAGE"],

    }
async def Check_Recipe(schema:dict):
    try:
        Title = await Recipes_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Recipes_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Recipe(schema: dict) -> dict:

        Recipes = await Recipes_collection.insert_one(schema)
        return "Recipes Successfully added"


async def retrieve_all_Recipess():
    Recipes = []
    async for data in Recipes_collection.find():
        Recipes.append(Recipes_helper(data))
    return Recipes


async def retrieve_Recipes_by_id(Recipes_id: str) -> dict:
    Recipes = await Recipes_collection.find_one({"_id": ObjectId(Recipes_id)})
    if Recipes:
        return Single_Recipes_helper(Recipes)
    else:
        return "No Recipes found by this id"


async def delete_Recipes_data(id: str):
    data = await Recipes_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delte = await Delete_Old_Image(id)
        await Recipes_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Recipes(id: str, data: dict,flags:int):
    if len(data) < 1:
        return False
    Recipes = await Recipes_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"]=Recipes['IMAGE']
    if Recipes:
        updated_Recipes = await Recipes_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Recipes:
            return True
        return False
