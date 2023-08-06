# SchinkenDB
I made this DataBase just so I have made one this is not actually useful or fast   
and the code is no gud   
don't use under any circumstances!   
HA GAYYYYY

default and only user: admin   
default and only password: admin   
maybe in the future the user and password are changeable     

Host:
```python
from SchinkenDB import SchinkenHost

db = SchinkenHost("FileName.sdb")
db.run()
```
Client:
```python
from SchinkenDB import SchinkenClient

db = SchinkenClient("127.0.0.1", "admin", "admin")

print(db.set("t", "test"))
print(db.get("t"))
```
