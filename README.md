Лабораторная работа №10. Django

В предыдущей работе от вас требовалось написать REST API сервер, предоставляющий интерфейс (API) для ведения заметок. В этой работе от вас требуется написать веб-приложение с использованием веб-фреймворка Django, которое бы стало промежуточным звеном между клиентом и API.
Ваше приложение должно предоставлять пользователю веб-интерфейс (UI):
форма регистрации и авторизации (при регистрации пользователю должно отправляться уведомление на почту с подтверждением регистрации);
CRUD (Create/Read/Update/Delete) для списка задач;
возможность поделиться списком задач с другим пользователем;
CRUD для отдельно взятой задачи (не забывайте, что задачам можно добавлять теги).
Бонусные задачи: Вы можете использовать bootstrap для более красивого отображения страниц, ajax, чтобы лишний раз не делать перезагрузку страницы и django-channels, чтобы пользователи в режиме реального времени могли видеть изменения в списках "расшаренных" (shared) задач.

ps. Сервер 9 лабы запускать python manage.py runserver 8080
