import random

from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation


def get_child_from_schoolkid_model(schoolkid):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned(
            'Введенное имя либо пустое, либо слишком распространенное. '
            'Необходимо ввести полностью ФИО.'
        )
    except Schoolkid.DoesNotExist:
        raise Schoolkid.DoesNotExist(
            'Такого имени не существует в базе. '
            'Проверьте правильность написания '
            'и наличие такого ученика на сайте.'
        )


def fix_marks(schoolkid):
    child = get_child_from_schoolkid_model(schoolkid)
    Mark.objects.filter(schoolkid=child, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    child = get_child_from_schoolkid_model(schoolkid)
    Chastisement.objects.filter(schoolkid=child).delete()


def create_commendation(schoolkid, subject, commendation_text=None):
    if not commendation_text:
        commendation_text = random.choice(
            [
                'Молодец!',
                'Отлично!',
                'Хорошо!',
                'Гораздо лучше, чем я ожидал!',
                'Ты меня приятно удивил!',
                'Великолепно!',
                'Прекрасно!',
                'Ты меня очень обрадовал!',
                'Именно этого я давно ждал от тебя!',
                'Сказано здорово – просто и ясно!',
                'Ты, как всегда, точен!',
                'Очень хороший ответ!',
                'Талантливо!',
                'Ты сегодня прыгнул выше головы!',
                'Я поражен!',
                'Уже существенно лучше!',
                'Потрясающе!',
                'Замечательно!',
                'Прекрасное начало!',
                'Так держать!',
                'Ты на верном пути!',
                'Здорово!',
                'Это как раз то, что нужно!',
                'Я тобой горжусь!',
                'С каждым разом у тебя получается всё лучше!',
                'Мы с тобой не зря поработали!',
                'Я вижу, как ты стараешься!',
                'Ты растешь над собой!',
                'Ты многое сделал, я это вижу!',
                'Теперь у тебя точно все получится!',
            ]
        )
    child = get_child_from_schoolkid_model(schoolkid)
    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject,
    ).order_by('-date').first()
    if not lesson:
        raise Lesson.DoesNotExist(
            'Проверьте правильность написания предмета. '
            'Сверьтесь с наличием предмета на сайте в расписании.'
        )
    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
