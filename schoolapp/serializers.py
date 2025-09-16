from rest_framework import serializers
from .models import School, Teacher, Student, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class TeacherSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subjects']

class StudentSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_no', 'school', 'subjects']

class SchoolDetailSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'students']

class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']
