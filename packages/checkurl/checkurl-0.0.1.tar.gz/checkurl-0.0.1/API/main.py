import pathlib
import json
import os

from fastapi import FastAPI, Request

from src.checkurl import check_urls_by_string

app = FastAPI()


@app.get("/")
async def alive():
    return "API are alive"


@app.post("/check-urls")
async def check_urls(request: Request):
    json_param = await request.json()
    return check_urls_by_string(json_param)


@app.get("/all-reports")
async def all_reports():
    output = dict()
    output["report"] = []
    for path in pathlib.Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../backup')).iterdir():
        if path.is_file():
            try:
                f = open(path, )
            except OSError as errOpenFile:
                print("File cannot be open")
                return -1
            try:
                data = json.load(f)
            except ValueError as err:
                print("JSON file cannot be loaded")
                return -2
            for i in data['report']:
                output["report"].append(i)
            f.close()
    return output
