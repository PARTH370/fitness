from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Exercise_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": str(data["TITLE"]),
        "BODYPART": data["BODYPART"],
        "EQUIPMENT": data["EQUIPMENT"],
        'LEVEL': data["LEVEL"],
        "REST": data["REST"],
        "SETS": data["SETS"],
        "REPS": data["REPS"],
        "VIDEO_URL": data["VIDEO_URL"],
        "INSTRUCTION": data["INSTRUCTION"],
        "TIPS": data["TIPS"],
        "IMAGE": data["IMAGE"],
    }

async def Check_Exercises(schema: dict):
    try:
        Title = await Exercise_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else: 
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Exercise_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Exercise(schema: dict) -> dict:

        Exercise = await Exercise_collection.insert_one(schema)
        return "Exercise Successfully added"


async def retrieve_all_Exercises():
    exercise = []
    async for data in Exercise_collection.find():
        exercise.append(Exercise_helper(data))
    return exercise


async def retrieve_exercise_by_id(exercise_id: str) -> dict:
    exercise = await Exercise_collection.find_one({"_id": ObjectId(exercise_id)})
    if exercise:
        return Exercise_helper(exercise)
    else:
        return "No Exercise found by this id"


async def delete_exercise_data(id: str):
    data = await Exercise_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Exercise_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_exercise(id: str, data: dict,flags:int):
    if len(data) < 1:
        return False
    exercise = await Exercise_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"]=exercise['IMAGE']
    if exercise:
        updated_exercise = await Exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_exercise:
            return True
        return False
