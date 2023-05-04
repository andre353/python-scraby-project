import os
from sqlalchemy import create_engine
# from sqlalchemy import create_engine, text

engine = create_engine(f"mysql+pymysql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DATABASE')}?charset=utf8mb4")

# db_connection_string = f"mysql+pymysql://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/{os.getenv("DATABASE")}?charset=utf8mb4"


# engine = create_engine(
#   db_connection_string,
#   connect_args={
#     "ssl": {
#       "ssl_ca": "/etc/ssl/cert.pem"
#     }
#   }
# )

# with engine.connect() as conn:
#   result = conn.execute(text("select * from books"))
#   print(result.all())