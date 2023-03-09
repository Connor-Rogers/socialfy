from pydal import DAL 
from decouple import config

db  = DAL(f"postgres://{config('DB_USER')}:{config('DB_PASS')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}")

