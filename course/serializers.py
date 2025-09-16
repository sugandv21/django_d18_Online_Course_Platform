from rest_framework import serializers
from .models import Course, Module, Lesson, Instructor

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']

class InstructorSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'bio', 'courses']

class LessonSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(read_only=True)
    module_title = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'module', 'module_title', 'course_id']

    def get_module_title(self, obj):
        return obj.module.title if obj.module else None

    def get_course_id(self, obj):
        return obj.module.course.id if (obj.module and obj.module.course) else None

class ModuleSerializer(serializers.ModelSerializer):
    lessons = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='lesson-detail'   
    )
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'course', 'lessons']
