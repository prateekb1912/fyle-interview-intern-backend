from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.decorators import validates
from core.models.assignments import Assignment, GradeEnum
from core.libs.helpers import GeneralObject
from core.libs.exceptions import FyleError


class AssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    content = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    teacher_id = auto_field(dump_only=True)
    student_id = auto_field(dump_only=True)
    grade = auto_field(dump_only=True)
    state = auto_field(dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return Assignment(**data_dict)


class AssignmentSubmitSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    teacher_id = fields.Integer(required=True, allow_none=False)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)

class AssignmentGradingSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none = False)
    grade = fields.String(required=True, allow_none=False)

    @validates('grade')
    def validate_grade(self, value):
        try:
            return GradeEnum(value)
        except ValueError:
            raise FyleError(400, 'Invalid grade value')

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)