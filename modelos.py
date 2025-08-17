from datetime import datetime
from email.policy import default
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Text, DateTime
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

productos_fotos_model = Table('productos_fotos',
                        meta,
                        Column('id', Integer, primary_key=True),
                        Column('nombre', String(100), nullable=False),
                        Column('productos_id', Integer, ForeignKey('productos.id'))
                        )

perfil_model = Table('perfil',
               meta,
               Column('id', Integer, primary_key=True),
               Column('nombre', String(100), nullable=False)
               )

usuarios_model = Table('usuarios',
               meta,
               Column('id', Integer, primary_key=True),
               Column('nombre', String(100), nullable=False),
               Column('correo', String(100), nullable=False),
               Column('contraseña', String(160), nullable=False),
               Column('fecha', DateTime()),
               Column('perfil_id', Integer, ForeignKey('perfil.id'))
               )


meta.create_all(motor)