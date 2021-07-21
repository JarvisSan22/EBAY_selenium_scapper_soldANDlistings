from setting import session
from user import *







def tests():
    #DBにレコードの追加
    for i in range(0,10):
        user = User()
        user.name= f"user{i}"
        session.add(user)
        session.commit()

    #すべて取得
    users = session.query(User).all()
    for user in users:
        print(user.name)

    names=["user3","user5"]
    users= session.query(User).filter(User.name.in_(names)).all()
    for user in users:
        print(user.name,user.age)