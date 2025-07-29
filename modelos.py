from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Text
from database import meta, motor


categorias_model = Table('categorias',
                        meta,
                        Column('id', Integer, primary_key=True),
                        Column('nombre', String(100), nullable=False),
                        Column('slug', String(100), nullable=False)
                        )

productos_model = Table('productos',
                        meta,
                        Column('id', Integer, primary_key=True),
                        Column('nombre', String(100), nullable=False),
                        Column('slug', String(100), nullable=False),
                        Column('descripcion', Text(), nullable=False),
                        Column('precio', Integer, default=1),
                        Column('categorias_id', Integer, ForeignKey('categorias.id'))
                        )

prodcutos_fotos_model = Table('productos_fotos',
                        Column('id', Integer, primary_key=True),
                        Column('nombre', String(100), nullable=False),
                        Column('productos_id', Integer, ForeignKey('productos.id'))
                        )

meta.create_all(motor)