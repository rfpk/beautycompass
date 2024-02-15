from django.http import JsonResponse

from apps.tools.database_operations import ADD, REMOVE


def model_action(model, request_model_name, object_model, profile):

    last_object_action = model.objects.filter(profile=profile,
                                              content_type__model=request_model_name,
                                              object_id=object_model.id)
    last_object_action = last_object_action.last()
    if last_object_action:
        if last_object_action.type_action == ADD:
            new_object_action = model.objects.create(profile=profile, content_object=object_model,
                                                     type_action=REMOVE
                                                     )
            if request_model_name == 'overview':
                object_model.author.rating -= 1
                object_model.author.save(update_fields=['rating'], )
            return new_object_action
    new_object_action = model.objects.create(profile=profile,
                                             content_object=object_model)
    if request_model_name == 'overview':
        object_model.author.rating -= 1
        object_model.author.save(update_fields=['rating'], )
    return new_object_action


def check_profile_permission(object_action, profile):
    class_name_object_action = object_action.__class__.__name__
    if class_name_object_action == 'Overview':
        if object_action.author == profile.profile_author.first():
            return JsonResponse(
                {
                    "message": "Creator this object can not set action!",
                    "status": "error",
                }
            )
    elif class_name_object_action in ['Brand', 'Article']:
        manufacturer_profile = object_action.manufacturer.profile
        if manufacturer_profile == profile:
            return JsonResponse(
                {
                    "message": "Creator this object can not set action!",
                    "status": "error",
                }
            )
    elif class_name_object_action == 'Product':
        manufacturer_profile = object_action.series.brand.manufacturer.profile
        if manufacturer_profile == profile:
            return JsonResponse(
                {
                    "message": "Creator this object can not set action!",
                    "status": "error",
                }
            )
    elif class_name_object_action == 'ConversationPost':
        if object_action.profile == profile:
            return JsonResponse(
                {
                    "message": "Creator this object can not set action!",
                    "status": "error",
                }
            )
    return True



