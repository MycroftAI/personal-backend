# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from sqlalchemy import Column, Text, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from personal_mycroft_backend.database import Base
from os.path import expanduser, join, exists
from os import makedirs

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    api_key = Column(String)
    name = Column(String)
    mail = Column(String)
    last_seen = Column(Integer, default=0)


class AdminDatabase(object):
    def __init__(self, path=None, debug=False):
        if path is None:
            path = join(expanduser("~"), ".mycroft", "personal_backend")
            if not exists(path):
                makedirs(path)
            path = 'sqlite:///' + join(path, 'admins.db')
        self.db = create_engine(path)
        self.db.echo = debug

        Session = sessionmaker(bind=self.db)
        self.session = Session()
        Base.metadata.create_all(self.db)

    def update_timestamp(self, user_name, timestamp):
        user = self.get_user_by_name(user_name)
        if user:
            user = user[0]
        else:
            return False
        user.last_seen = timestamp
        self.commit()
        return True

    def change_api(self, user_name, new_key):
        user = self.get_user_by_name(user_name)
        if user:
            user = user[0]
        else:
            return False
        user.api_key = new_key
        self.commit()
        return True

    def get_user_by_api_key(self, api_key):
        return self.session.query(Admin).filter_by(api_key=api_key).all()

    def get_user_by_name(self, name):
        return self.session.query(Admin).filter_by(name=name).all()

    def add_user(self, name=None, mail=None, api=""):
        try:
            user = Admin(api_key=api, name=name, mail=mail,
                         id=self.total_users()+1)
            self.session.add(user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def total_users(self):
        return self.session.query(Admin).count()

    def commit(self):
        self.session.commit()

if __name__ == "__main__":
    db = AdminDatabase(debug=True)
    name = "jarbas"
    mail = "jarbasai@mailfence.com"
    api = "admin_key"
    db.add_user(name, mail, api)


