import psycopg2
import environ


env = environ.Env()
environ.Env.read_env()

connection = psycopg2.connect(
    host=env('HOST'),
    database=env('DATABASE'),
    user=env('USER'),
    password=env('PASSWORD')
)
