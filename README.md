# ALGO_ASYNC_API

Асинхронная Библиотека для Взаимодействия с Бекэндом платформы Algoritmika.

> Данная библиотека не является Официальной и не связана с Алгоритмикой.

> Первоначальная Версия Синхронной Библиотеки Находится: [Здесь](https://github.com/moontr3/algo_api/)

> Используйте эту библиотеку только в учебных целях! Создатели ALGO_ASYNC_API не несут ответственности за любые повреждения, нанесенные платформе во время использования.

## Установка

Вы можете устновить библиотеку при помощи `pip`:

```bash
pip install git+https://github.com/Vadim-Khristenko/algo_async_api
```

## Лицензия

Данная Библиотека Лицензирована согласно [Лицензии MIT](LICENSE)

## Быстрое начало

```python
import asyncio
import algo_async_api as api

login = "Ваш Логин"
password = "Ваш Пароль"

async def main():
    session = await api.AsyncSession.create(login, password)
    check = await session.my_profile()
    print(check.first_name)
    print(check.last_name)
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Установите Библиотеку при помощи

```bash
pip install git+https://github.com/Vadim-Khristenko/algo_async_api
```

## Документация

Здесь вы можете найти Поддробную документацию того, как работает бибилотека. [Ссылка на Документацию](docs/Documentation.md)

## Что Сделано?

- [x] Пользователи
- [x] Проекты
- [x] Изменение Проектов
- [x] Тренды
- [x] Комментарии и Реакции в Зале Славы

## Что планируется сделать?

- [ ] Создание Проектов класса Картинки
- [ ] Изменение Профиля
