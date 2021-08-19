from utils import SQLiteDB


if __name__ == "__main__":
    db = SQLiteDB("todoList.db")
    r1 = db.raw("delete from main")
    r2 = db.raw("delete from detail")
    if r1 == '200' and r2 == '200':
        print("清理成功~")
