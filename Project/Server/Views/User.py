from datetime import timedelta
from sys import flags
from bson import ObjectId
from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Utils.Auth_Bearer import *
from Project.Server.Database import User_collection
from Project.Server.Controller.User import update_user
from Project.Server.Controller.User import Add_User_Measures,Update_Measurments,retrieve_user_measurment,Add_User_Details,Delete_Old_Image,Check_Email_Mobile ,retrieve_all_Users, delete_user_data, retrieve_user_by_id
from fastapi.encoders import jsonable_encoder
from Project.Server.Models.User import User_Details,Add_Measurment, Login, ChangePassword

router = APIRouter()


@router.post("/", response_description="User Registration")
async def User_Registration(data: User_Details = Body(...)):
    data = jsonable_encoder(data)
    Email= await Check_Email_Mobile(data)
    if Email == False:
        return {"code": 200, "Msg": 'Email or Mobile Already Registered'}
    if len(data['IMAGE'])>0:
        img_path=await Image_Converter(data['IMAGE'])
    else:
        img_path=""
    data['IMAGE'] = str(img_path)
    data['PassWord'] = get_password_hash(data['PassWord'])
    Output = await Add_User_Details(data)
    return {"code": 200, "Msg": Output}


@router.get("/", response_description="Get all User Details")
async def get_all_Users():
    workout = await retrieve_all_Users()
    if workout:
        return {"code": 200, "Data": workout}
    return {"Data": workout, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get user information data by id")
async def get_user_data(id):
    data = await retrieve_user_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete user data by id")
async def delete_User(id: str):
    data = await delete_user_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_user_data(id: str, req: User_Details = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    flags=0
    if len(req["IMAGE"])!=0:
        # Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_user = await update_user(id, req,flags)
    if updated_user:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }

@router.post("/{id}", response_description="Change Status")
async def Change_Status(id: str):
    data = await User_collection.find_one({"_id": ObjectId(id)})
    if data:
        if data["Status"]=="Active":
            await User_collection.update_one({"_id": ObjectId(id)}, {"$set": {"Status": "Inactive"}})
        else:
            await User_collection.update_one({"_id": ObjectId(id)}, {"$set": {"Status": "Active"}})
        return {"code": 200, "Msg": "Status Changed Successfully"}
    return {"code": 404, "Msg": "Id may not exist"}


@router.post("/Login/", response_description="Login User")
async def login(User: Login = Body(...)):
    user = jsonable_encoder(User)
    if user["Social"] == True:
        users = await User_collection.find_one({"Mobile": (user['Email'])})
    try:
        int(user["Email"])
        users = await User_collection.find_one({"Mobile": int(user['Email'])})
    except:
        users = await User_collection.find_one({"Email": user['Email']})
        # mobiles = await user_collection.find_one({"mobile": user['email']})
    if users and user["Social"] == True:
        access_token = create_access_token(
            data={"sub": user["Email"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer", "_id": str(users["_id"]), 'name': users['Name']}
    if users:
        if (verify_password(user['PassWords'], users['PassWord'])):
            access_token = create_access_token(
                data={"sub": users["Email"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            return {"code": 200,"access_token": access_token, "token_type": "bearer", "_id": str(users["_id"]), 'name': users['Name']}
        else:
            return {"code": 404, "message": "Password not match"}
    return {"code": 404, "message": "User not found or invalid Details"}


@router.post("/Change_Password/{id}", response_description="Change the password")
async def change_password(id: str, User: ChangePassword = Body(...)):
    User = jsonable_encoder(User)
    data = await User_collection.find_one({"_id": ObjectId(id)})
    print(User["old_passWords"])
    if verify_password(User['old_passWords'],data['PassWord']):
        data['PassWord'] = get_password_hash(User['new_password'])
        status = await User_collection.find_one_and_update({"_id": ObjectId(id)}, 
                                                       {"$set": data})
        return {"code": 200, "message":"Password changed successfully"}
    else:
        return {"code": 404, "message": "Please enter Valid Old Password"}


@router.post("/Add_Measurment/{id}", response_description="Add Measurment")
async def add_measurment(id: str, Measurment: Add_Measurment = Body(...)):
    data= jsonable_encoder(Measurment)
    data["User_id"]=str(id)
    status = await Add_User_Measures(data)
    return {"code": 200, "message": "Measurment added successfully"}

@router.get("/Get_Measurment/{id}", response_description="Get Measurment")
async def Get_Measurment(id: str):
    data = await retrieve_user_measurment(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}

@router.put("/Update_Measurment/{id}", response_description="Update Measurment")
async def Update_Measurment(id: str, Measurment: Add_Measurment = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await Update_Measurments(id, req)
    if updated_user:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }