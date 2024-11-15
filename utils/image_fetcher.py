import base64
from .logging_config import log_execution
import aiohttp
import asyncio
from io import BytesIO
from PIL import Image

@log_execution
async def fetch_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image = Image.open(BytesIO(await response.read()))
                buffer = BytesIO()
                image.save(buffer, format="WEBP", quality=60)
                image_bytes = buffer.getvalue()

                # Encode to base64
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                return str(image_base64)
            else:
                print(f"Error: {response.status}")
