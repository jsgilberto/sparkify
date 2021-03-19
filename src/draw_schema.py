from constants import POSTGRES_USER as user
from constants import POSTGRES_PASSWORD as password
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData


def main():
    graph = create_schema_graph(
        concentrate=False,
        show_datatypes=False,
        metadata=MetaData(f"postgresql://{user}:{password}@127.0.0.1/sparkifydb"),
        rankdir="TB",
        relation_options={'fontsize': "8.0"}
    )
    graph.write_png("sparkifydb_erd.png")

if __name__ == "__main__":
    main()