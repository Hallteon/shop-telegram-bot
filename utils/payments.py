from aiogram.types import ShippingOption, LabeledPrice

post_shipping_option = ShippingOption(id="post_option", title="Отправка по Почте России")
post_shipping_option.add(LabeledPrice(label="Стандартная отправка", amount=20000))
post_shipping_option.add(LabeledPrice(label="Срочная отправка", amount=50000))

pickup_shipping_option = ShippingOption(id="pickup_option", title="Самовывоз из Екатеринбурга")
pickup_shipping_option.add(LabeledPrice(label="Стандартный самовывоз (через 5 дней))", amount=5000))
pickup_shipping_option.add(LabeledPrice(label="Срочный самовывоз (через 1 день))", amount=20000))

to_home_shipping_option = ShippingOption(id="to_home_option", title="Доставка на дом в Екатеринбурге")
to_home_shipping_option.add(LabeledPrice(label="Стандартная доставка (через 1 дня))", amount=15000))
to_home_shipping_option.add(LabeledPrice(label="Быстрая доставка (через 3 часа))", amount=25000))

