# discordsrv_api

# Usage
```python
import discordsrv_api.models
from discordsrv_api import User
import discordsrv_api

db = discordsrv_api.models.DB(user='db_user', password='db_password',
                              name='db_name', host='db_host')

luck = discordsrv_api.DiscordSRV(db)
user: User = luck.get_uuid('3267586347348')
print(user.uuid)
user: User = luck.get_discord('931be104-f4a9-369d-ab89-b709dcd44a03')
print(user.discord)
```
