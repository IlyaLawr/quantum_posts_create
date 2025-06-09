from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(prefix='', tags=['page'])


@router.get('/', response_class=FileResponse)
async def main_page():
    return FileResponse('presentation/static/index.html')
