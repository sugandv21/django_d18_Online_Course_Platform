from rest_framework import viewsets
from django.db.models import Prefetch
from .models import School, Teacher, Student, Subject
from .serializers import (
    SchoolDetailSerializer, SchoolListSerializer,
    TeacherSerializer, StudentSerializer, SubjectSerializer
)

class SchoolViewSet(viewsets.ModelViewSet):
    """
    - list: returns schools (use list serializer)
    - retrieve: returns school with nested students (SchoolDetailSerializer)
    Query optimization: prefetch students to avoid N+1.
    """
    queryset = School.objects.all()
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolListSerializer

    def get_queryset(self):
        # Prefetch students (and their subjects if you want)
        student_qs = Student.objects.select_related('school').prefetch_related('subjects')
        return School.objects.prefetch_related(Prefetch('students', queryset=student_qs))

class StudentViewSet(viewsets.ModelViewSet):
    """
    Student endpoints. Optimize with select_related('school') to fetch school in same query.
    """
    queryset = Student.objects.select_related('school').prefetch_related('subjects').all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    Teacher endpoints. Optimize with prefetch_related('subjects') since it's ManyToMany.
    """
    queryset = Teacher.objects.prefetch_related('subjects').all()
    serializer_class = TeacherSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
