import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .ai_utils import ai_quiz_generator, simple_summarize

from .forms import NoteForm, SignUpForm
from .models import Note, Summary
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("note_list")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "study/note_list.html", {"notes": notes})

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user

            # If a file is uploaded, read its content
            if note.uploaded_file:
                ext = os.path.splitext(note.uploaded_file.name)[1].lower()
                if ext == ".txt":
                    text = note.uploaded_file.read().decode("utf-8")
                    note.content = text
                # (we will extend later for PDF/docx)

            note.save()
            return redirect("note_detail", pk=note.pk)
    else:
        form = NoteForm()
    return render(request, "study/note_form.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("note_list")
    else:
        form = SignUpForm()
    return render(request, "auth/signup.html", {"form": form})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    summary = None
    quiz = None

    if hasattr(note, "summary"):
        summary = note.summary.content

    if request.method == "POST":
        if "summarize" in request.POST:
            summary_text = simple_summarize(note.content)
            summary_obj, created = Summary.objects.get_or_create(note=note)
            summary_obj.content = summary_text
            summary_obj.save()
            summary = summary_text

        elif "quiz" in request.POST:
            quiz = ai_quiz_generator(note.content)

    return render(
        request,
        "study/note_detail.html",
        {"note": note, "summary": summary, "quiz": quiz}
    )

def quiz_view(request):
    if request.method == "POST":
        text = request.POST.get("notes")
        questions = ai_quiz_generator(text)
        return render(request, "notes/quiz.html", {"questions": questions})
    return render(request, "notes/quiz.html", {"questions": []})
