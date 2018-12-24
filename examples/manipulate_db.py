from personal_mycroft_backend.database.devices import DeviceDatabase

db = DeviceDatabase()

username = "test_user"
code = "XQFTNM"
uuid = "cc3524c7-ff52-42b3-af8f-de89249b19c8"
mail = "fakemail2@not_real.com"

# add a device to the db
if not db.add_device(uuid):

    # cant commit device to db before pairing, make available for pairing
    db.add_unpaired_device(uuid, code)

    if not db.add_device(uuid):
        # user did not pair yet, perform manual pairing
        from personal_mycroft_backend.backend.remote_admin_api import \
            BackendMycroftAPI

        ap = BackendMycroftAPI("admin_key", url="http://0.0.0.0:6712/v0.1/")
        print(ap.pair(code, uuid, mail, username))


# Browse the db
from pprint import pprint

device = db.get_device_by_uuid(uuid)
print(device.name)
print(device.last_seen)
print(device.created_at)
print(device.paired)
print(device.uuid)
print(device.ips)

db.add_ip(uuid, "0.0.0.0")
print(device.ips)

location = device.location
print(location.city)

config = device.config
print(config.lang)
print(config.opt_in)


print(db.total_devices())
print(db.total_users())


# Edit the db
stt = config.stt
print(stt.engine_type)
stt.engine_type = "google"

db.commit()  # save changes

location_conf = {
    "city": {
      "code": "Lawrence",
      "name": "Lawrence",
      "state": {
        "code": "KS",
        "name": "Kansas",
        "country": {
          "code": "US",
          "name": "United States"
        }
      }
    },
    "coordinate": {
      "latitude": 38.971669,
      "longitude": -95.23525
    },
    "timezone": {
      "code": "America/Chicago",
      "name": "Central Standard Time",
      "dstOffset": 3600000,
      "offset": -21600000
    }
  }

user = device.user
print(user.mail)
print(user.name)
print(user.password)

db.add_user(mail, "joe", "badPassword")
print(user.mail)
print(user.name) # changed to joe
print(user.password) # no longer empty



