from personal_mycroft_backend.database.admin import AdminDatabase
from personal_mycroft_backend.backend.remote_admin_api import BackendMycroftAPI


db = AdminDatabase(debug=True)
name = "jarbas"
mail = "jarbasai@mailfence.com"
api = "admin_key"
db.add_user(name, mail, api)


ap = BackendMycroftAPI("admin_key", url="http://0.0.0.0:6712/v0.1/")
username = "test_user"
code = "XQFTNM"
uuid = "cc3524c7-ff52-42b3-af8f-de89249b19c8"
mail = "fakemail2@not_real.com"
print(ap.pair(code, uuid, mail, username))