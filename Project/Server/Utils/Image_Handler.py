import base64
import uuid


async def Image_Converter(Hax_Value):
    random_name = str(uuid.uuid4())
    decodeit = open(f"Server/static/{random_name}.jpg", 'wb')
    decodeit.write(base64.b64decode(Hax_Value))
    decodeit.close()
    img_path = "http://localhost:8000/images?id=Server%2Fstatic%2F" + \
        str(random_name)+".jpg"
    return img_path

