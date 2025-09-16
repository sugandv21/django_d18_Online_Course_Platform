from rest_framework import viewsets
from django.db.models import Prefetch
from .models import Course, Module, Lesson, Instructor
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer, InstructorSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.prefetch_related('courses').all()
    serializer_class = InstructorSerializer

class LessonViewSet(viewsets.ModelViewSet):
    """
    Optimize lesson retrieval using select_related on module and course.
    This ensures that when serializing a lesson we do not cause extra queries
    to access lesson.module and lesson.module.course.
    """
    queryset = Lesson.objects.select_related('module__course').all()
    serializer_class = LessonSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    """
    For Modules we prefetch lessons — but the lessons queryset itself uses
    select_related to avoid N+1 if LessonSerializer touches module/course.
    """
    lessons_qs = Lesson.objects.select_related('module__course').all()
    queryset = Module.objects.select_related('course').prefetch_related(
        Prefetch('lessons', queryset=lessons_qs, to_attr='prefetched_lessons')
    ).all()
    serializer_class = ModuleSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return super().get_serializer(*args, **kwargs)
