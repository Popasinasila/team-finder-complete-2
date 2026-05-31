from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import FavoriteProject, Project


def project_list(request):
    """Main page — paginated list of projects sorted by newest first."""
    qs = Project.objects.select_related("author").all()
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Collect favorite project ids for the current user
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(
            request.user.favorites.values_list("project_id", flat=True)
        )

    return render(request, "projects/project_list.html", {
        "page_obj": page_obj,
        "fav_ids": fav_ids,
    })


def project_detail(request, pk):
    """Project detail page."""
    project = get_object_or_404(Project, pk=pk)
    is_author = request.user.is_authenticated and request.user == project.author
    is_participant = (
        request.user.is_authenticated
        and project.participants.filter(pk=request.user.pk).exists()
    )
    is_favorite = (
        request.user.is_authenticated
        and FavoriteProject.objects.filter(user=request.user, project=project).exists()
    )
    participants = project.participants.all()

    return render(request, "projects/project_detail.html", {
        "project": project,
        "is_author": is_author,
        "is_participant": is_participant,
        "is_favorite": is_favorite,
        "participants": participants,
    })


@login_required
def create_project(request):
    """Create a new project."""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, "Проект успешно создан!")
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, "projects/create_project.html", {"form": form})


@login_required
def edit_project(request, pk):
    """Edit an existing project (author only)."""
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.author:
        messages.error(request, "У вас нет прав для редактирования этого проекта")
        return redirect("project_detail", pk=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Проект обновлён")
            return redirect("project_detail", pk=pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/edit_project.html", {"form": form, "project": project})


@login_required
@require_POST
def complete_project(request, pk):
    """Mark project as completed (author only)."""
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.author:
        messages.error(request, "У вас нет прав для этого действия")
        return redirect("project_detail", pk=pk)

    project.status = "completed"
    project.save()
    messages.success(request, "Проект завершён")
    return redirect("project_detail", pk=pk)


@login_required
def favorites(request):
    """Show current user's favorite projects."""
    fav_entries = request.user.favorites.select_related("project__author").order_by("-created_at")
    projects = [entry.project for entry in fav_entries]

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "projects/favorites.html", {"page_obj": page_obj})


@login_required
@require_POST
def toggle_favorite(request, pk):
    """Toggle favorite status for a project. Returns JSON {is_favorite: bool}."""
    project = get_object_or_404(Project, pk=pk)
    fav, created = FavoriteProject.objects.get_or_create(user=request.user, project=project)
    if not created:
        fav.delete()
        return JsonResponse({"is_favorite": False})
    return JsonResponse({"is_favorite": True})


@login_required
@require_POST
def join_project(request, pk):
    """Toggle participation in a project."""
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.author:
        messages.error(request, "Автор не может вступить в собственный проект")
        return redirect("project_detail", pk=pk)

    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        messages.info(request, "Вы покинули проект")
    else:
        project.participants.add(request.user)
        messages.success(request, "Вы вступили в проект!")

    return redirect("project_detail", pk=pk)
