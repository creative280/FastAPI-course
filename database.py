from sqlalchemy import create_engine, MetaData


motor = create_engine("mysql+pymysql://root:123456@localhost:3306/fastapi")

meta = MetaData()

conectar = motor.connect()