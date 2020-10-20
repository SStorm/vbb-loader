import sys
from crate import client


# Note: ability to connect to multiple nodes has been de-scoped
def migrate(db_url: str, username: str, password: str):
    print(f"Will connect to CrateDB at '{db_url}' ...")
    conn = client.connect(db_url, username=username, password=password)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("Success")


if __name__ == '__main__':
    # Parse args
    if len(sys.argv) != 4:
        print("Usage: ")
        print("./init.py [db-connection-url] [user] [password]")
        exit(1)

    url = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    migrate(url, user, password)
