from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import RegistrationForm, LoginForm, ProfileEditForm, CustomPasswordChangeForm
from .models import User


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect("project_list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Войдите в систему.")
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """User login view using email + password."""
    if request.user.is_authenticated:
        return redirect("project_list")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "project_list")
                return redirect(next_url)
            else:
                messages.error(request, "Неверный email или пароль")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """User logout view."""
    logout(request)
    return redirect("project_list")


def profile(request, pk):
    """Public user profile page showing their projects."""
    user = get_object_or_404(User, pk=pk)
    projects = user.projects.all()
    return render(request, "users/profile.html", {"profile_user": user, "projects": projects})


@login_required
def edit_profile(request):
    """Edit own profile view."""
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
            return redirect("profile", pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


def users_list(request):
    """Paginated list of users with optional filtering (Variant 1)."""
    active_filter = request.GET.get("filter", "")
    qs = User.objects.all()

    if request.user.is_authenticated and active_filter:
        user = request.user

        if active_filter == "favorites_authors":
            # Authors of projects the user has favorited
            fav_project_ids = user.favorites.values_list("project_id", flat=True)
            from projects.models import Project
            author_ids = Project.objects.filter(id__in=fav_project_ids).values_list(
                "author_id", flat=True
            )
            qs = User.objects.filter(id__in=author_ids)

        elif active_filter == "my_project_participants":
            # Participants of projects authored by the current user
            from projects.models import Project
            my_project_ids = Project.objects.filter(author=user).values_list("id", flat=True)
            participant_ids = Project.objects.filter(
                id__in=my_project_ids
            ).values_list("participants__id", flat=True)
            qs = User.objects.filter(id__in=participant_ids).exclude(id=user.id)

        elif active_filter == "users_who_like_my_projects":
            # Users who favorited the current user's projects
            from projects.models import FavoriteProject
            my_project_ids = user.projects.values_list("id", flat=True)
            liker_ids = FavoriteProject.objects.filter(
                project_id__in=my_project_ids
            ).values_list("user_id", flat=True)
            qs = User.objects.filter(id__in=liker_ids).exclude(id=user.id)

        elif active_filter == "joined_authors":
            # Authors of projects the current user has joined
            from projects.models import Project
            joined_projects = user.joined_projects.all()
            author_ids = joined_projects.values_list("author_id", flat=True)
            qs = User.objects.filter(id__in=author_ids).exclude(id=user.id)

    qs = qs.order_by("-date_joined")
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/users_list.html", {
        "page_obj": page_obj,
        "active_filter": active_filter,
    })


@login_required
def change_password(request):
    """Change password view."""
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно изменён")
            return redirect("profile", pk=request.user.pk)
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})
