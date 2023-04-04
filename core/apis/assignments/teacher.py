from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
import logging

from .schema import AssignmentSchema, AssignmentGradingSchema

logger = logging.Logger(__name__)

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.auth_principal
@decorators.accept_payload
def grade_assignments(incoming_payload, p):
    """Grade an assignment"""    
    try:
        grade_assignment_payload = AssignmentGradingSchema().load(incoming_payload)
    except Exception as err:
        print(err.messages)
        return APIResponse.respond(data={'error': err.messages})

    print('Loaded payload:', grade_assignment_payload)  

    graded_assignment = Assignment.grade_assignment(
        _id=grade_assignment_payload.id,
        _grade=grade_assignment_payload.grade,
        principal=p
    )

    db.session.commit()
    
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    
    return APIResponse.respond(data=graded_assignment_dump)
