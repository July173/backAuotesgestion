from apps.assign.entity.models.AsignationInstructorHistory import AsignationInstructorHistory

class AsignationInstructorHistoryRepository:
    def __init__(self):
        self.model = AsignationInstructorHistory

    def create_history(self, asignation_instructor, old_instructor_id, message):
        return self.model.objects.create(
            asignation_instructor=asignation_instructor,
            old_instructor_id=old_instructor_id,
            message=message
        )

    def list_by_asignation(self, asignation_instructor_id):
        return self.model.objects.filter(asignation_instructor_id=asignation_instructor_id)
