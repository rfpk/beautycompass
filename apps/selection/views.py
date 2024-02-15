from django.shortcuts import render, get_object_or_404, redirect

from apps.profile.models import Profile
from apps.testing.models import TestsResult
from apps.selection.models import Selection
from apps.selection.forms import AnswerSelectionForm


def answer_selection(request):
    user = request.user
    is_auth = user.is_authenticated
    if not is_auth:
        return redirect("/")
    
    selection = get_object_or_404(Selection, is_publish=True)
    if request.method == 'POST':
        form = AnswerSelectionForm(request.POST, selection=selection)
        if form.is_valid():
            form.save_answers(request.user)
    else:
        form = AnswerSelectionForm(selection=selection)
    
    profile = Profile.objects.filter(user=user).first()
    test_results = (TestsResult.objects
                        .filter(profile__user=request.user)
                        .select_related('profile')
                    )
    return render(request, 'selection/answer_selection.html', {
        'form': form,
        'test': selection,
        'test_results': test_results,
        'nickname': profile.nickname,
    })
