from Server.Database import *
import os
IMAGEDIR=os.getcwd()

def bodyparts_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "IMAGE": data["IMAGE"],
    }

async def Check_Bodypart(schema: dict):
    try:
        Title = await Bodyparts_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Bodyparts_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Bodypart(schema: dict) -> dict:

  
        Title = await Bodyparts_collection.insert_one(schema)
        return "Body Part Successfully added"


async def retrieve_all_bodyparts():
    bodyparts = []
    async for data in Bodyparts_collection.find():
        bodyparts.append(bodyparts_helper(data))
    return bodyparts


async def retrieve_bodypart_by_id(bodypart_id: str) -> dict:
    bodyparts = await Bodyparts_collection.find_one({"_id": ObjectId(bodypart_id)})
    if bodyparts:
        return bodyparts_helper(bodyparts)


async def delete_bodypart_data(id: str):
    data = await Bodyparts_collection.find_one({"_id": ObjectId(id)})
    if data:
        Img_delete = await Delete_Old_Image(id)
        await Bodyparts_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_bodypart(id: str, data: dict,flags:int):
    if len(data) < 1:
        return False
    bodypart = await Bodyparts_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"]=bodypart['IMAGE']
    if bodypart:
        updated_bodypart = await Bodyparts_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_bodypart:
            return True
        return False
