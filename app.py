from __future__ import annotations
from typing import Optional
from datetime import datetime
from enum import Enum
from jsonclasses import jsonclass, jsonenum, types
from jsonclasses_pymongo import pymongo, Connection
from jsonclasses_server import api, create_flask_server


Connection.default.set_url('mongodb://localhost:27017/apidemodb')


@jsonenum
class Sex(Enum):
    MALE = 1
    FEMALE = 2


@api
@pymongo
@jsonclass
class User:
    id: str = types.readonly.str.primary.mongoid.required
    username: str = types.str.unique.required
    email: Optional[str] = types.str.email.unique
    sex: Optional[Sex] = types.writeonce.enum(Sex)
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@api
@pymongo
@jsonclass
class Product:
    id: str = types.readonly.str.primary.mongoid.required
    name: str
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@api
@pymongo
@jsonclass
class Category:
    id: str = types.readonly.str.primary.mongoid.required
    name: str
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


app = create_flask_server()
