from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
 
# Create & Read
def student_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        course = request.POST['course']
        Student.objects.create(name=name, age=age, course=course)
        return redirect('student_list')
    students = Student.objects.all()
    return render(request, 'student_app/student_list.html', {'students': students})
 
# Update
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.age = request.POST['age']
        student.course = request.POST['course']
        student.save()
        return redirect('student_list')
    return render(request, 'student_app/edit_student.html', {'student': student})
 
# Delete
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')
