from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, StudentViewSet, TeacherViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'subjects', SubjectViewSet, basename='subject')

urlpatterns = router.urls
