from django.contrib.auth.decorators import user_passes_test

def group_required(group_name: str | list[str]):
    def in_group(user):
        if isinstance(group_name, list):
            return user.is_authenticated and any(user.groups.filter(name=grp).exists() for grp in group_name)
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)
