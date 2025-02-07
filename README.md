![Node.js](/docs/img/InventoryCRM.png)
![Node.js](/docs/img/About.png)
Эффективный учет и контроль спортивного инвентаря в школе играет
важную роль в обеспечении высокого уровня проведения спортивных
мероприятий и занятий физической культурой. \
Управление спортивным инвентарём через веб-интерфейс может значительно облегчить отслеживание наличия, состояния и
распределения спортивного инвентаря, а также планирование его закупок.
![Node.js](/docs/img/Start.png)
  #### Установите LTS версию [NodeJS](https://nodejs.org/)
  ```
  apt install nodejs
  ```
  #### Установите пакеты
  ```
  npm i
  ```
  #### Запустите проект
  ```
  npm start
  ```
![Node.js](/docs/img/Block.png)
![Node.js](/docs/img/db_design.jpg)
![Node.js](/docs/img/Func.png)
| Блок-схема | Код |
|----------|----------|
|![Node.js](/docs/img/Получение.png)|![No Name](/docs/img/Получение_код.jpg)|
|![Node.js](/docs/img/Замена.png)|![Node.js](/docs/img/Замена_код.jpg)|
|![Node.js](/docs/img/Ремонт.png)|![Node.js](/docs/img/setitemforcell.PNG)|

![Node.js](/docs/img/Inter.png)
![Node.js](/docs/img/Регистрация.png)
Регистрация пользователя в системе.\
Пользователь должен осуществить ввод имени, никнейма, пароля и повторного пароля. Для успешной регистрации пароли должны совпадать.

![Node.js](/docs/img/Авторизация.png)
Авторизация пользователя в системе.\
Пользователь должен ввести почту и пароль от своего аккаунта, после чего он может успешно войти на сайт.

![Node.js](/docs/img/new_field.jpg)
Создание игрового поля.\
Для создания игрового поля администратор должен нажать на кнопку «Добавить поле» во вкладке «Поля», после чего ввести название и указать размер стороны поля (не меньше 2-х и не больше 26-и) во всплывающем окне.

![Node.js](/docs/img/new_item.jpg)
Создание нового приза.\
Для создания нового приза администратор должен нажать на кнопку «Добавить приз» во вкладке «Призы», после чего ввести название и стоимость приза, а так же добавить изображение во всплывающем окне.

![Node.js](/docs/img/new_ship.jpg)
Создание нового корабля на поле.\
Для создания нового корабля администратор должен нажать на любую из свободных клеток поля, после чего выбрать приз из списка заранее созданных призов.

![Node.js](/docs/img/add_user_to_field.jpg)
Добавление игрока на поле.\
В окне редактирования пользователей на поле администратор в поиск вписывает id пользователя или его никнейм, после чего добавляет на поле.

![Node.js](/docs/img/shot_counting.jpg)
Начисление выстрелов.\
В окне редактирования пользователей на поле администратор изменяет количество выстрелов для пользователя.

![Node.js](/docs/img/auth.jpg)
Авторизация пользователя в системе.\
Пользователь должен ввести почту и пароль от своего аккаунта, после чего он может успешно войти на сайт.

![Node.js](/docs/img/select_field.jpg)
Выбор поля для пользователя.\
На странице с полями пользователь выбирает любое из доступных полей и нажимает кнопку «Играть на этом поле»

![Node.js](/docs/img/field.jpg)
![Node.js](/docs/img/winnign_priz.jpg)
Осуществление выстрела.\
Пользователь осуществляет выстрел нажатием на клетку поля. В случае попадания клетка поля будет помечена квадратом, а пользователю высветится сообщение о выигранном призе. В случае непопадания, на месте выстрела будет стоять крестик. Если у пользователя нет выстрелов, после попытки осуществить выстрел система уведомит о том, что выстрелов недостаточно.

![Node.js](/docs/img/all_items.png)
Просмотр списка всех призов.\
Зайдя во вкладку «Все подарки» пользователь может посмотреть список всех призов, которые он может выиграть.

![Node.js](/docs/img/my_items.jpg)
Просмотр списка призов.\
Зайдя во вкладку «Мои подарки» пользователь может посмотреть список выигранных им призов.
