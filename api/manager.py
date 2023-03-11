from django.db import models
from django.db.models import Q

class ThreadManager(models.Manager):
    """This is a custom manager class that is used to manage Thread objects. 
        It defines a get_or_new method that retrieves or creates a new chat thread between two users.
    """
    def get_or_new(self, user, other_user):
        if user == other_user:
            return None, False
        qlookup1 = Q(user_one=user) & Q(user_two=other_user)
        qlookup2 = Q(user_one=other_user) & Q(user_two=user)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            if user != other_user:
                obj = self.model(user_one=user, user_two=other_user)
                obj.save()
                return obj, True
            return None, False