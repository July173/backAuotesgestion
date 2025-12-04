from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.assign.views.EnterpriseViewset import EnterpriseViewset
from apps.assign.views.BossViewset import BossViewset
from apps.assign.views.HumanTalentViewset import HumanTalentViewset
from apps.assign.views.ModalityProductiveStageViewset import ModalityProductiveStageViewset
from apps.assign.views.RequestAsignationViewset import RequestAsignationViewset
from apps.assign.views.AsignationInstructorViewset import AsignationInstructorViewset
from apps.assign.views.AsignationInstructorHistoryViewset import AsignationInstructorHistoryViewset
from apps.assign.views.VisitFollowingViewset import VisitFollowingViewset
from apps.assign.views.FormRequestPDFViewset import FormRequestPDFAPIView
from apps.assign.views.MessageViewset import MessageViewset

router = DefaultRouter()
router.register(r'enterprise', EnterpriseViewset, basename='assign_enterprise')
router.register(r'boss', BossViewset, basename='assign_boss')
router.register(r'human_talent', HumanTalentViewset, basename='assign_human_talent')
router.register(r'modality_productive_stage', ModalityProductiveStageViewset, basename='assign_modality_productive_stage')
router.register(r'request_asignation', RequestAsignationViewset, basename='assign_request_asignation')
router.register(r'asignation_instructor', AsignationInstructorViewset, basename='assign_asignation_instructor')
router.register(r'asignation_instructor_history', AsignationInstructorHistoryViewset, basename='assign_asignation_instructor_history')
router.register(r'visit_following', VisitFollowingViewset, basename='assign_visit_following')
router.register(r'message', MessageViewset, basename='assign_message')

urlpatterns = [
    path('', include(router.urls)),
    path('form-requests/upload-pdf/', FormRequestPDFAPIView.as_view(), name='form_requests_upload_pdf'),
]
