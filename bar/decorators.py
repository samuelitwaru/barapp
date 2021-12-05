from django.contrib.auth.decorators import user_passes_test


def groups_required(*group_names):
	"""Requires user membership in atleast one of the groups passed in"""
	def in_groups(user):
		if user.is_authenticated:
			if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
				return True
		return False

	return user_passes_test(in_groups, login_url='bar:logout')