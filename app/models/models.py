from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Rates(models.Model):
    """
    Insurance Rate model
    """
    id = fields.BigIntField(pk=True)

    date = fields.DateField(null=True, auto_now_add=True)
    cargo_type = fields.CharField(max_length=255)
    rate = fields.FloatField()

    modified_at = fields.DatetimeField(auto_now=True)

Rate_Pydantic = pydantic_model_creator(Rates, name="Rate")
