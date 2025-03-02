from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends
import uvicorn
from fastapi.responses import HTMLResponse
from api.routers.comics import router as items_router, get_items

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(items_router)



@app.get("/", response_class=HTMLResponse)
def index(request: Request, items: dict = Depends(get_items)):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@app.get("/about/", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, port=8001)