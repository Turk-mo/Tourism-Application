from activities.models import Activity
# this method will generate and copy # of random activities based on the given number & Fields
def activity_generate_qs(qs=Activity.objects.all()):
    if qs.count() < 50:
        for obj in qs:

            user                = obj.user
            title               = obj.title
            image_thumbanil     = obj.image_thumbanil
            genre               = obj.genre
            secondary           = obj.secondary.all()
            overview            = obj.overview
            charge              = obj.charge
            new_obj             = Activity.objects.create(
                user = user,
                title = title,
                image_thumbanil = image_thumbanil,
                genre = genre,
                
                overview = overview,
                charge = charge
            )
            for gen in secondary:
                new_obj.secondary.add(gen)
            new_obj.save()
        qstwo = Activity.objects.all()
        if qstwo.count() <= 50:
            return activity_generate_qs(qs=qstwo)
        return qs.count

activity_generate_qs()
