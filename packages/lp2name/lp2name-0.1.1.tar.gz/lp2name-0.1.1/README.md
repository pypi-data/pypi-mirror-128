# lp2name

# Usage
```python
import lp2name.models
from lp2name import User
import lp2name

db = lp2name.models.DB(user='db_user', password='db_password',
                          name='db_name', host='db_host')

luck = lp2name.LuckPerms(db)
user: User = luck.get_user_by_name('cofob')
print(user.username)
print(user.uuid)
user: User = luck.get_user_by_uuid('931be104-f4a9-369d-ab89-b709dcd44a03')
print(user.username)
print(user.uuid)
```
