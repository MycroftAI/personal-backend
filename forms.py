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
