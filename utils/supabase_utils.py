import pandas as pd

from supabase_keys import supabase

liga_mx_players = pd.read_csv("data/radar/liga_mx/players.csv")
liga_mx_keepers = pd.read_csv("data/radar/liga_mx/keepers.csv")
mls_players = pd.read_csv("data/radar/mls/players.csv")
mls_keepers = pd.read_csv("data/radar/mls/keepers.csv")

def create_table(table_name, columns):
    columns_sql = ",\n  ".join([f'"{col}" TEXT' for col in columns])
    sql = f'''
    CREATE TABLE IF NOT EXISTS "{table_name}" (
      {columns_sql}
    );
    '''
    try:
        res = supabase.rpc("execute_sql", {"sql": sql}).execute()
        print(f"✅ Tabla `{table_name}` creada.")
    except Exception as e:
        print(f"❌ Error creando `{table_name}`:\n{e}")

create_table("players_liga_mx", liga_mx_players.columns)
create_table("keepers_liga_mx", liga_mx_keepers.columns)
create_table("players_mls", mls_players.columns)
create_table("keepers_mls", mls_keepers.columns)

def insert_dataframe(df, table_name):
    data = df.to_dict(orient="records")
    for chunk in [data[i:i+500] for i in range(0, len(data), 500)]:
        try:
            res = supabase.table(table_name).insert(chunk).execute()
            print(f"✅ Insertados {len(chunk)} registros en `{table_name}`")
        except Exception as e:
            print(f"❌ Error insertando en `{table_name}`:\n{e}")

insert_dataframe(liga_mx_players, "players_liga_mx")
insert_dataframe(liga_mx_keepers, "keepers_liga_mx")
insert_dataframe(mls_players, "players_mls")
insert_dataframe(mls_keepers, "keepers_mls")