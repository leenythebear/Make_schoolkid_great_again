from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Commendation, Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Lesson
import random


def get_schoolkid_object(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except MultipleObjectsReturned:
        print("Найдено слишком много учеников. Пожалуйста, уточните запрос")
    except ObjectDoesNotExist:
        print("Не найдено ни одного ученика. Пожалуйста, проверьте запрос")
    else:
        return schoolkid


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_marks.update(points=5)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject_name):
    commendations = ['Молодец!', 'Отлично!', 'Хорошо!',
                     'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                     'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
                     'Именно этого я давно ждал от тебя!',
                     'Сказано здорово – просто и ясно!',
                     'Ты, как всегда, точен!', 'Очень хороший ответ!',
                     'Талантливо!', 'Ты сегодня прыгнул выше головы!',
                     'Я поражен!', 'Уже существенно лучше!',
                     'Потрясающе!', 'Замечательно!', 'Прекрасное начало!',
                     'Так держать!', 'Ты на верном пути!',
                     'Здорово!', 'Это как раз то, что нужно!',
                     'Я тобой горжусь!',
                     'С каждым разом у тебя получается всё лучше!',
                     'Мы с тобой не зря поработали!',
                     'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                     'Ты многое сделал, я это вижу!',
                     'Теперь у тебя точно все получится!']
    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                    group_letter=schoolkid.group_letter,
                                    subject__title=subject_name).order_by('date')
    if lessons:
        lesson = lessons.last()
        commendation = random.choice(commendations)
        Commendation.objects.create(created=lesson.date,
                                    subject=lesson.subject,
                                    schoolkid=schoolkid,
                                    teacher=lesson.teacher,
                                    text=commendation)
    else:
        print("Такой предмет не найден. Пожалуйста, проверьте запрос")


def make_schoolkid_happy_again(schoolkid_name, subject_name):
    schoolkid = get_schoolkid_object(schoolkid_name)
    if schoolkid:
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject_name)
