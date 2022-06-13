import base64
import uuid


async def Image_Converter(Hax_Value):
    random_name = str(uuid.uuid4())
    decodeit = open(f"Project/Server/Static/{random_name}.jpg", 'wb')
    decodeit.write(base64.b64decode(Hax_Value))
    decodeit.close()
    # mg_path = "http://localhost:8000/images?id=Server%2FStatic%2F" + \
    #     str(random_name)+".jpg"
    img_path = "https://myfiti.herokuapp.com/images?id=Server%2FStatic%2F" + \
        str(random_name)+".jpg"
    return img_path

