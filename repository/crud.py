from typing import List, Type, Union

import sqlalchemy
from sqlalchemy.orm import Session, DeclarativeMeta

'''
Usage Examples
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_crud import crud

from my_app.models import MyModel

# Set up the SQLAlchemy session
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
db = Session()

# Create a new object
model = crud.create_model(db, MyModel, schema={"name": "John Doe"})

# Retrieve all objects
models = crud.get_models(db, MyModel)

# Retrieve an object by ID
model = crud.get_model(db, MyModel, model_id=1)

# Retrieve objects by a specific attribute
models = crud.get_models_by_attribute(db, MyModel, attribute="name", attribute_value="John Doe")
model = crud.get_model_by_attribute(db, MyModel, attribute="uuid", attribute_value="123e4567-e89b-12d3-a456-426614174000")

# Update an object
model = crud.update_model(db, MyModel, model_id=1, schema={"name": "Jane Doe"})

# Delete an object
crud.delete_model(db, MyModel, model_id=1)
Getting Started
'''


def get_models(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        offset: int = 0,
        limit: int = 100,
) -> List[DeclarativeMeta]:
    return db.query(model).offset(offset).limit(limit).all()


def get_model(
        db: Session, model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta], model_id: int
) -> Union[DeclarativeMeta, None]:
    return get_model_by_attribute(
        db=db, model=model, attribute="id", attribute_value=model_id
    )


def get_model_by_attribute(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        attribute: str,
        attribute_value,
) -> Union[DeclarativeMeta, None]:
    if hasattr(model, attribute):
        model_attribute = getattr(model, attribute)
        return db.query(model).filter(model_attribute == attribute_value).first()
    else:
        raise AttributeError


def get_model_by_attributes(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        query: dict,
) -> Union[DeclarativeMeta, None]:
    dohas = False
    # 遍历query

    # 创建一个空查询
    query = db.query(model)

    # 遍历字典的每一项
    for key, value in dict.items():
        # 检查模型是否有这个属性
        if hasattr(model, key):
            # 如果有，将此属性对应的条件添加到查询中
            query = query.filter(getattr(model, key) == value)
            dohas = True

    if dohas:
        # 执行查询
        return query.first()
    else:
        raise AttributeError


def get_models_by_attributes(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        query_dict: dict,
        offset: int = 0,
        limit: int = 100,
) -> list[Type[DeclarativeMeta]]:
    dohas = False
    # 遍历query

    # 创建一个空查询
    query = db.query(model)

    # 遍历字典的每一项
    for key, value in query_dict.items():
        # 检查模型是否有这个属性
        if hasattr(model, key):
            # 如果有，将此属性对应的条件添加到查询中
            query = query.filter(getattr(model, key) == value)
            dohas = True

    if dohas:
        # 执行查询
        return query.offset(offset).limit(limit).all()
    else:
        raise AttributeError


def get_models_by_attribute(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        attribute: str,
        attribute_value,
        offset: int = 0,
        limit: int = 100,
) -> List[DeclarativeMeta]:
    if hasattr(model, attribute):
        model_attribute = getattr(model, attribute)
        return (
            db.query(model)
            .filter(model_attribute == attribute_value)
            .offset(offset)
            .limit(limit)
            .all()
        )
    else:
        raise AttributeError


def create_model(
        db: Session, model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta], schema: dict
) -> DeclarativeMeta:
    db_model = model(**schema)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def add_entity(db: Session, entity) -> DeclarativeMeta:
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def update_model(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        model_id: int,
        schema: dict,
) -> Union[DeclarativeMeta, None]:
    db_model = get_model(db=db, model=model, model_id=model_id)
    for key, value in schema.items():
        if hasattr(db_model, key):
            setattr(db_model, key, value)
        else:
            raise AttributeError

    db.commit()
    db.refresh(db_model)
    return db_model


def update_model_by_attribute(
        db: Session,
        model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        lookup_attribute: str,
        lookup_attribute_value,
        schema: dict,
) -> Union[DeclarativeMeta, None]:
    db_model = get_model_by_attribute(
        db=db,
        model=model,
        attribute=lookup_attribute,
        attribute_value=lookup_attribute_value,
    )
    for key, value in schema.items():
        if hasattr(db_model, key):
            setattr(db_model, key, value)
        else:
            raise AttributeError

    db.commit()
    db.refresh(db_model)
    return db_model


def delete_model(
        db: Session, model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta], model_id: int
) -> None:
    db_model = get_model(db=db, model=model, model_id=model_id)
    db.delete(db_model)
    db.commit()


def link_models(
        db: Session,
        parent_model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        parent_id: int,
        child_model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        child_id: int,
        backref: str,
) -> Union[DeclarativeMeta, None]:
    parent = get_model(db=db, model=parent_model, model_id=parent_id)
    child = get_model(db=db, model=child_model, model_id=child_id)

    if hasattr(parent, backref):
        getattr(parent, backref).append(child)
        db.commit()
        db.refresh(parent)
        return parent
    else:
        raise AttributeError


def unlink_models(
        db: Session,
        parent_model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        parent_id: int,
        child_model: Type[sqlalchemy.orm.decl_api.DeclarativeMeta],
        child_id: int,
        backref: str,
) -> Union[DeclarativeMeta, None]:
    parent = get_model(db=db, model=parent_model, model_id=parent_id)
    child = get_model(db=db, model=child_model, model_id=child_id)

    if hasattr(parent, backref):
        getattr(parent, backref).remove(child)
        db.commit()
        db.refresh(parent)
        return parent
    else:
        raise AttributeError
