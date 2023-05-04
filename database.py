# import os
# from sqlalchemy import create_engine, text

# db_connection_string = f"mysql+pymysql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DATABASE')}?charset=utf8mb4"

# engine = create_engine(
#   db_connection_string,
#   connect_args={
#     "ssl": {
#       "ssl_ca": "/etc/ssl/cert.pem"
#     }
#   }
# )

# with engine.connect() as conn:
#   results = conn.execute(text("select * from books"))

#   fetched_results = [r._asdict() for r in results]
#   print(fetched_results)