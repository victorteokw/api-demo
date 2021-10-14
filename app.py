from __future__ import annotations
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from dotenv import load_dotenv
from jsonclasses import jsonclass, jsonenum, types
from jsonclasses_pymongo import pymongo, Connection
from jsonclasses_server import api, authorized, create_flask_server

load_dotenv()

Connection.default.set_url('mongodb://localhost:27017/apidemodb')


@jsonenum
class Sex(Enum):
    MALE = 1
    FEMALE = 2


@authorized
@api
@pymongo
@jsonclass
class User:
    id: str = types.readonly.str.primary.mongoid.required
    username: str = types.str.unique.authidentity.required
    email: Optional[str] = types.str.email.unique.authidentity
    password: Optional[str] = types.writeonly.str.length(8, 16).salt.authbycheckpw
    auth_code: Optional[str] = types.str.authby(
        types.crossfetch('AuthorizationCode', 'email').fval('value').eq(types.passin)
    ).temp
    sex: Optional[Sex] = types.writeonce.enum(Sex)
    orders: list[Order] = types.nonnull.listof('Order').linkedby('user')
    favorites: list[Favorite] = types.nonnull.listof('Favorite').linkedby('user')
    selling_products: list[Product] = types.nonnull.listof('Product').linkedby('seller')
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@authorized
@api
@pymongo
@jsonclass
class Admin:
    id: str = types.readonly.str.primary.mongoid.required
    username: str = types.str.unique.authidentity.required
    password: Optional[str] = types.writeonly.str.length(8, 16).salt.authbycheckpw
    sex: Optional[Sex] = types.writeonce.enum(Sex)
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@api(enable='E')
@pymongo
@jsonclass
class AuthorizationCode:
    id: str = types.readonly.str.primary.mongoid.required
    email: Optional[str] = types.str.email.unique
    phone_no: Optional[str] = types.str.digit.unique
    value: str = types.str.fsetonsave(types.randomdigits(4)).required
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.umininterval(timedelta(minutes=1)).required


@api
@pymongo
@jsonclass
class Product:
    id: str = types.readonly.str.primary.mongoid.required
    name: str
    seller: User = types.objof('User').linkto.asopd.required
    image: Optional[str] = types.uploader('image').str.url
    category: Category = types.objof('Category').linkto.required
    orders: list[Order] = types.nonnull.listof('Order').linkedby('product')
    favorites: list[Favorite] = types.nonnull.listof('Favorite').linkedby('product')
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@api
@pymongo
@jsonclass
class Category:
    id: str = types.readonly.str.primary.mongoid.required
    name: str
    parent: Optional[Category] = types.objof('Category').linkto
    children: list[Category] = types.nonnull.listof('Category').linkedby('parent')
    products: list[Product] = types.nonnull.listof('Product').linkedby('category')
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@api
@pymongo
@jsonclass
class Order:
    id: str = types.readonly.str.primary.mongoid.required
    quantity: int = types.int.default(1).min(1).required
    price: float = types.float.min(0).required
    user: User = types.objof('User').linkto.required
    product: Product = types.objof('Product').linkto.required
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


@api
@pymongo
@jsonclass
class Favorite:
    id: str = types.readonly.str.primary.mongoid.required
    user: User = types.objof('User').linkto.required
    product: Product = types.objof('Product').linkto.required
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required


app = create_flask_server()
