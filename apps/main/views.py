import logging
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseBadRequest

from .forms import (
    UserRegistrationForm,
    LoginUserForm, PasswordReset, ChangePasswordForm,
)
from apps.profile.models import Profile, User
from ..verification.models import RegistrationLink, PasswordResetLink
from ..verification.signing import (
    RegistrationTokenGenerator,
    PasswordResetTokenGenerator,
)

logger = logging.getLogger("main")


def register(request):
    if request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.POST["password1"] != request.POST["password2"]:
                return JsonResponse(
                    {"message": _("Passwords are not the same"), "status": "error"}
                )
            else:
                email = form.cleaned_data['username']
                link_count = RegistrationLink.max_count(email)

                link = RegistrationLink.objects.create(
                    email=email,
                    password=make_password(data["password1"]),
                    phone=form.cleaned_data['phone'],
                    nickname=form.cleaned_data['nickname'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    count=link_count,
                )

                backend = RegistrationTokenGenerator(link)
                sign, token = backend.dump_data(link.pk, "user")
                url = backend.create_url(reverse("main:activate_register"), sign, token)

                link.url = url
                link.save(update_fields=["url"])

                context = {"host": settings.HOST, "url": url}
                body_text = render_to_string("email/register_body.txt", context)

                send_mail(
                    "Регистрация",
                    body_text,
                    settings.EMAIL_HOST_USER,
                    [data["username"]],
                    fail_silently=False,
                )

                return JsonResponse(
                    {
                        "message": _("A confirmation email has been sent to you"),
                        "status": "success",
                    }
                )

        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )

    return HttpResponseBadRequest()


def login_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("landing:main_page")})
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.filter(username=data["email"]).first()
            if user:
                user = authenticate(username=user.username, password=data["password"])
                if user is not None:
                    login(request, user)
                    referer_url = request.META.get('HTTP_REFERER')
                    if referer_url:
                        return redirect(referer_url)
                    else:
                        return redirect('landing:main_page')
                else:
                    return JsonResponse(
                        {
                            "message": _("The data entered is incorrect."),
                            "status": "error",
                        }
                    )
            else:
                return JsonResponse(
                    {"message": _("There is no such user"), "status": "error"}
                )
        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )

    return HttpResponseBadRequest()


@login_required
def logout_user(request):
    logout(request)
    return redirect("landing:main_page")


def activate_user(request):
    sign = request.GET.get("sign")
    token = request.GET.get("token")
    backend = RegistrationTokenGenerator()
    sign_data = backend.check_sign(sign)
    if not sign_data:
        return HttpResponseBadRequest()

    link = RegistrationLink.objects.filter(id=sign_data["id"]).first()
    if not link:
        return HttpResponseBadRequest()

    link_count = RegistrationLink.max_count(link.email)
    link.count = link_count
    backend.record = link

    if not backend.check_token("user", token):
        return HttpResponseBadRequest()

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=link.email
            )
            user.password = link.password
            user.save(update_fields=['password', ])

            profile = user.user_profile
            profile.phone = link.phone
            profile.nickname = link.nickname
            profile.first_name = link.first_name
            profile.last_name = link.last_name
            profile.save(update_fields=['phone', 'nickname', 'first_name', 'last_name', ])

            link.profile = profile
            link.is_used = True
            link.count = link_count + 1
            link.save(update_fields=["profile", "is_used", "count"])

    except IntegrityError as e:
        logger.exception(f"User({link.id}) creation error: {e}")
        return HttpResponseBadRequest()

    login(request, user)
    return redirect(reverse("landing:main_page"))


def change_password(request):
    if request.method == "POST":
        form = PasswordReset(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.filter(user__username=data["email"]).first()
            if profile:
                link_count = PasswordResetLink.max_count(profile)

                link = PasswordResetLink.objects.create(
                    profile=profile,
                    count=link_count,
                )

                backend = PasswordResetTokenGenerator(link)
                sign, token = backend.dump_data(link.pk, profile.user)
                url = backend.create_url(reverse("main:reset_password"), sign, token)

                link.url = url
                link.save(update_fields=["url"])

                context_body = {"host": settings.HOST, "url": url, "host_name": settings.HOST_NAME}
                body_text = render_to_string(
                    "email/chang_password.txt", context_body
                )
                send_mail(
                    "Сброс пароля",
                    body_text,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data["email"]],
                    fail_silently=False,
                )
            return JsonResponse(
                {
                    "message": _("A confirmation email has been sent to you"),
                    "status": "success",
                },
            )

        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )

    return HttpResponseBadRequest()


def reset_password(request):
    sign = request.GET.get("sign")
    token = request.GET.get("token")
    backend = PasswordResetTokenGenerator()
    sign_data = backend.check_sign(sign)
    if not sign_data:
        return HttpResponseBadRequest()

    link = PasswordResetLink.objects.filter(id=sign_data["id"]).first()
    if not link:
        return HttpResponseBadRequest()

    user = link.profile.user

    link_count = PasswordResetLink.max_count(link.profile)

    link.count = link_count
    backend.record = link
    if not backend.check_token(user, token):
        return HttpResponseBadRequest()

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user.set_password(form.cleaned_data["password"])
                    user.save()

                    link.is_used = True
                    link.count = link_count + 1
                    link.save(update_fields=["is_used", "count"])
            except IntegrityError as e:
                logger.exception(f"Profile({link.id}) password reset error: {e}")
                return HttpResponseBadRequest()

            messages.success(request, "Пароль успешно изменен")
            return redirect("main:index")

    context = {
        "form_change": ChangePasswordForm(),
    }
    return render(request, "site/change_password.html", context)
