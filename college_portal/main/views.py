from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4
import json
from django.contrib.auth.models import User

from .models import Student, LabSession, LabMark, Subject

def home(request):
    show_login = False
    error = False

    if request.method == "POST":
        show_login = True
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect("dashboard")
        else:
            error = True

    return render(request, "home.html", {
        "show_login": show_login,
        "error": error
    })


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "dashboard.html")


def syllabus(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "syllabus.html")

def timetable(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "timetable.html")


def pa_lab(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "pa_lab.html")
def exp1(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp1.html")
def exp2(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp2.html")
def exp3(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp3.html")
def exp4(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp4.html")
def exp5(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp5.html")
def exp6(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp6.html")
def exp7(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp7.html")
def exp8(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp8.html")
def exp9(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp9.html")
def exp10(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp10.html")
def exp11(request):
    if not request.user.is_authenticated:
        return redirect("home")
    return render(request, "exp11.html")


def lecturer_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("lab_marks")
        else:
            return render(request, "login.html", {"error": True})

    return render(request, "login.html")


def lecturer_register(request):
    error = None
    success = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            User.objects.create_user(
                username=username,
                password=password
            )
            success = "Account created successfully. Please login."

    return render(request, "lecturer_register.html", {
        "error": error,
        "success": success
    })
@login_required
def lab_marks(request):
    subject = Subject.objects.first()
    students = Student.objects.all()
    sessions = LabSession.objects.filter(subject=subject).order_by("date")

    table = []

    for student in students:
        marks_row = []
        total = 0
        count = 0

        for session in sessions:
            mark = LabMark.objects.filter(
                student=student,
                session=session
            ).first()

            if mark:
                marks_row.append(mark.marks)
                total += mark.marks
                count += 1
            else:
                marks_row.append("")

        avg = round(total / count, 2) if count else 0

        table.append({
            "roll": student.roll_no,
            "marks": marks_row,
            "avg": avg
        })

    return render(request, "lab_marks.html", {
    "sessions": sessions,
    "table": table,
    "session_ids_json": json.dumps([s.id for s in sessions])
})

    
@csrf_exempt
@login_required
def add_session(request):
    data = json.loads(request.body)

    subject = Subject.objects.first()
    if not subject:
        return JsonResponse(
            {"error": "No subject found. Please create a subject first."},
            status=400
        )

    LabSession.objects.create(
        subject=subject,
        date=data["date"],
        lecturer=request.user
    )

    return JsonResponse({"status": "ok"})

@csrf_exempt
def save_mark(request):
    data = json.loads(request.body)

    student = Student.objects.get(roll_no=data["roll"])
    session = LabSession.objects.get(id=data["session"])

    LabMark.objects.update_or_create(
        student=student,
        session=session,
        defaults={"marks": data["marks"]}
    )

    return JsonResponse({"status": "saved"})

@login_required
def download_lab_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lab_marks.pdf"'

    sessions = LabSession.objects.all().order_by('date')
    students = Student.objects.all()

    data = [['Roll No', 'Average']]

    for student in students:
        marks = LabMark.objects.filter(student=student)
        total = sum(m.marks for m in marks)
        avg = round(total / marks.count(), 2) if marks.exists() else 0
        data.append([student.roll_no, avg])

    doc = SimpleDocTemplate(response, pagesize=A4)

    from reportlab.lib import colors
    table = Table(data, repeatRows=1)
    table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ])

    doc.build([table])
    return response

@csrf_exempt
@login_required
def delete_session(request):
    data = json.loads(request.body)
    session_id = data.get("session_id")

    if not session_id:
        return JsonResponse({"error": "Session id missing"}, status=400)

    LabMark.objects.filter(session_id=session_id).delete()
    LabSession.objects.filter(id=session_id).delete()

    return JsonResponse({"status": "deleted"})
        


