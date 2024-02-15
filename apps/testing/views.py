from pytils.translit import slugify
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.testing.forms import AnswerTestForm
from apps.testing.models import Test, Option, AnswerProfile, QuestionTest, TestsResult
from apps.profile.models import Profile


def answer_test(request):
    user = request.user
    is_auth = user.is_authenticated
    if not is_auth:
        return redirect("/")

    test = get_object_or_404(Test, is_publish=True)
    options = Option.objects.all()
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        keys = list(request.POST.keys())
        keys.remove('test_name')
        test_name = request.POST.get('test_name')
        for key in keys:
            results = request.POST.getlist(key)
            options = Option.objects.filter(pk__in=results)
            
            answer = AnswerProfile.objects.create(
                profile=profile,
                question=QuestionTest.objects.get(pk=options.first().question.id),
                test_result_user=test_name,
            )
            answer.option.add(*options)
            answer.save()

        # Сохранения Результата теста
        test_result = TestsResult.objects.create(profile=profile, name=test_name)
        test_result.slug = slugify(test_result.name)
        test_result.save()
        return JsonResponse({'status': 'success', 'message': 'Answer Success Added'})
    else:
        form = AnswerTestForm(test=test)
    return render(request, 'testing/test_page.html', {'form': form, 'test': test, 'options': options})


class TestResultView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        is_auth = user.is_authenticated
        if not is_auth:
            return redirect("/")

        keys = self.request.GET.keys()
        profile = Profile.objects.get(user=request.user)
        nums = []
        for key in keys:
            list_nums = self.request.GET.getlist(key)
            nums += list_nums

        options = Option.objects.filter(id__in=nums)
        return render(request, 'testing/rezult_test.html', {'nickname': profile.nickname, 'options': options})
