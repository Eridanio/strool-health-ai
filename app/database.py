from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://strool_user:SUA_SENHA@dpg-d747th1aae7s73bcdvkg-a.oregon-postgres.render.com/strool"

engine = create_engine(DATABASE_URL)

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS consultas (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            nome TEXT,
            idade INTEGER,
            dia INTEGER,
            mes INTEGER,
            hora TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))
        conn.commit()