Parsing online.metro-cc.ru
--------------------------

Здравствуйте!  

Тестируйте и смотрите код изначально async metro.py файла в этой директории. Если очень часто запускать этот код, сайт перестанет выдавать ответ, содержащий блоки продуктов, возвращает пустой html. В таком случае можете запустить код metro.py, но поскольку тут не используется асинхронное программирование, код будет выполняться очень долго, потому что для того, чтобы получить бренд товара, нужно "провалиться" в страницу товара.

>Где найти проверку на наличие товара?

Я со страницы html беру все блоки с class="catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop", что уже значит, что товар в наличии. У блока товара, которого нет в наличии, class="catalog-2-level-product-card product-card subcategory-or-type__products-item is-out-of-stock" отличается.

Если возникнут вопросы по коду, буду рад ответить вам в обратной связи!

Спасибо,  
Данила