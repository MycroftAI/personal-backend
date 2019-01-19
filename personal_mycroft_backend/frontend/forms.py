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
from wtforms import Form, StringField, validators, SubmitField


class LoginForm(Form):
    username = StringField('Username:', validators=[validators.required(),
                                                 validators.Length(min=1,
                                                                   max=30)])
    password = StringField('Password:', validators=[validators.required(),
                                                    validators.Length(min=1,
                                                                      max=30)])
    email = StringField('Email:', validators=[validators.optional(),
                                              validators.Length(min=0,
                                                                max=50)])


class PairingForm(Form):
    name = StringField('Device name:')
    code = StringField('Pairing Code:', validators=[validators.required(),
                                                    validators.Length(min=6,
                                                                      max=6)])

    submit = SubmitField("Pair")
