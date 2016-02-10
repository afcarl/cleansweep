from cleansweep.models import Place
from flask_wtf import Form
import wtforms
from wtforms import FieldList, FormField, SelectField, StringField, TextAreaField, HiddenField
from wtforms import validators

from ... import models
from ...voterlib import voterdb

class SignupForm(Form):
    name = StringField('Name', [validators.Required()])
    phone = StringField('Phone Number', [validators.Required()])
    voterid = StringField('Voter ID')
    locality = StringField('Locality')
    place = HiddenField()

    def validate_phone(self, field):
        phone = field.data
        if models.PendingMember.find(phone=phone) or models.Member.find(phone=phone):
            raise validators.ValidationError('This phone number is already used')

    def validate_voterid(self, field):
        if not field.data and self.place.data == "None":  # TODO highlight locality field too
            raise validators.ValidationError("You must provide either a valid voter ID or locality.")

        if self.voterid.data:
            voterid = self.voterid.data
            voterinfo = voterdb.get_voter(voterid=voterid)
            if not voterinfo:
                raise validators.ValidationError("Invalid Voter ID")
