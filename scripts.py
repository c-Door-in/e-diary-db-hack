import random

from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation


def fix_marks(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    Mark.objects.filter(schoolkid=child, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
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
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject,
    ).order_by('-date').first()
    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
