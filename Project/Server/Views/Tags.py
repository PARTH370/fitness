from fastapi import APIRouter, Body
from Project.Server.Controller.Tags import Add_Tag, delete_Tag_data, retrieve_all_Tags, retrieve_Tag_by_id, update_Tag
from Models.Tags import Tags
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/", response_description="Add Tag")
async def add_Tags_data(schema: Tags = Body(...)):
    schema = jsonable_encoder(schema)
    Output = await Add_Tag(schema)
    return {"code": 200,"Msg":Output }


@router.get("/",response_description="Get all Tags")
async def get_all_Tags():
    Tags = await retrieve_all_Tags()
    if Tags:
        return {"code": 200,"Data":Tags}
    return {"Data":Tags,"Msg":"Empty list return"}

@router.get("/{id}",response_description="Get Tag data by id")
async def get_Tag_data(id):
    data = await retrieve_Tag_by_id(id)
    if data:
        return {"code": 200,"Data":data}
    return {"Msg":"Id may not exist"}

@router.delete("/{id}",response_description="Delete Tag data by id")
async def delete_Tag(id:str):
    data = await delete_Tag_data(id)
    if data:
        return {"code": 200,"Msg":data}
    return {"Msg":"Id may not exist"}

@router.put("/{id}")
async def update_Tag_data(id: str, req: Tags = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_Tag = await update_Tag(id, req)
    if updated_Tag:
        return {"code": 200,"Data":"Data updated Successfully"}

    return {
        "code": 404,"Data":"Something Went Wrong"
    }

