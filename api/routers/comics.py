from fastapi import APIRouter, status, HTTPException, Form
from typing import Annotated
from pydantic import PositiveInt

router = APIRouter(prefix="/api", tags=["comics"])

comics = {}


def init_comics():
    comics.update(
        items=[
            {"comics": "Marvel"},
            {"comics": "DC"},
            {"comics": "Bubble"}
        ])
    for idx, comics_obj in enumerate(comics["items"], start=1):
        comics_obj["id"] = idx


init_comics()


def get_items():
    comics_list = comics["items"]
    comics_values = [item['comics'] for item in comics_list]
    return comics_values


@router.get("")
def read_items():
    value = get_items()
    return {"comics": value}


@router.get("/{comic_id}", responses={
    status.HTTP_200_OK: {
        "description": "Comics Found",
        "content": {
            "application/json": {
                "example": {
                    "data": {
                        "comics": "Миф",
                        "id": 4
                    },
                },
            },
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Comics not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Comics #4 does not exist",
                },
            },
        },
    },
},
            )
def get_comic(comic_id: PositiveInt):
    comics_values = comics["items"]
    if comic_id > len(comics_values):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comics{comic_id} doesn't exist")
    comics_value = comics_values[comic_id - 1]
    return comics_value


@router.post("",
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_201_CREATED: {
                     "description": "Comics Created",
                     "content": {
                         "application/json": {
                             "example": {
                                 "data": {
                                     "comics": "Миф",
                                     "id": 4
                                 },
                             },
                         },
                     },
                 },
                 status.HTTP_400_BAD_REQUEST: {
                     "description": "Comics already exists",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Comics 'Name' already exists",
                             },
                         },
                     },
                 },
             },
             )
def add_movie(
        title: Annotated[str, Form()],
):
    comics_values = comics["items"]
    if any(title.lower() == item["comics"].lower() for item in comics_values):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Comics {title!r} already exists",
        )

    new_comics = {"comics": title.title()}

    comics_values.append(new_comics)
    new_comics["id"] = len(comics_values)
    # respond with new item
    return {
        "comics": new_comics,
    }
