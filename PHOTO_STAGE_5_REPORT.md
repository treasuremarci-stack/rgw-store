# АКС — отчёт по этапу 5 фотографий товаров из 1С

Дата проверки: 2026-11-15  
Ветка: `photos-1c-stage-5`  
Основа: актуальный `main`, commit `c737ab146feb08ac961d9e8fd31c4d3f292994ee`  
Источник порядка: первоначальный отчёт инвентаризации `stage1_aks_1c_inventory.xlsx`, лист `Без фото`, позиции 113–140.

## Результат

- Проверено: **28 из 28** товаров.
- Получили фото: **24 товара**.
- Добавлено локальных изображений: **36 WebP**.
- Без фото оставлено: **4 товара**.
- Изменены только `products.json` для товаров этого этапа и новые папки изображений.
- `PROJECT_STATUS.md` не изменялся.

## Таблица товаров

| № | Название товара (ID; категория) | SKU | Основное фото | Доп. фото | Статус |
|---:|---|---|---|---:|---|
| 113 | D Link Сетевая карта D Link 100-1000 DGE-560 T (`cards-3`; Сетевые карты) | НФ-00000024 | `main.webp` | 0 | Добавлено |
| 114 | Куди Cudy PE10 Gigabit PCI Express Adapter (`cards-4`; Сетевые карты) | НФ-00001047 | `main.webp` | 0 | Добавлено |
| 115 | Куди Cudy PE10G 10G PCI Express Adapter (Marvell AQC113) (`cards-5`; Сетевые карты) | НФ-00001048 | `main.webp` | 0 | Добавлено |
| 116 | Пилот MERCURY 6240U-SCK 5m (`strips-5`; Сетевые фильтры / пилоты) | НФ-00000395 | Нет | 0 | Оставлено без фото: точная версия 5 m не подтверждена; вариант 1,8 m и сторонние карточки не использованы |
| 117 | Стабилизатор Automatic Voltage Regulator 1500VA (`stabilizers-8`; Стабилизаторы) | НФ-00000702 | Нет | 0 | Оставлено без фото: в номенклатуре нет бренда и точной модели |
| 118 | Aruba instant On AP 11 Access Point (`access-10`; Точки доступа) | НФ-00000001 | `main.webp` | 0 | Добавлено; точное соответствие AP11/APIN0303 проверено по HPE/FCC |
| 119 | Куди Cudy AP1300 Indoor (`access-11`; Точки доступа) | НФ-00001067 | `main.webp` | 0 | Добавлено |
| 120 | Куди Cudy AP1300 Outdoor (`access-12`; Точки доступа) | НФ-00001069 | `main.webp` | 0 | Добавлено |
| 121 | Куди Cudy AP3000 Outdoor (`access-13`; Точки доступа) | НФ-00001068 | `main.webp` | 0 | Добавлено |
| 122 | Флешка 128 GB Lexar JumpDrive V100 USB 3.0 (`acc-flash_drives-9`; Флешки) | НФ-00000527 | `main.webp` | 0 | Добавлено; на фото видна маркировка 128G |
| 123 | Флешка 256 GB Lexar JumpDrive Dual Drive D400 USB 3.0 (`acc-flash_drives-10`; Флешки) | НФ-00000528 | `main.webp` | 0 | Добавлено; на фото видна маркировка 256G |
| 124 | Флешка 64 GB Lexar JumpDrive V100 USB 3.0 (`acc-flash_drives-11`; Флешки) | НФ-00001106 | Нет | 0 | Оставлено без фото: чистый официальный кадр с маркировкой 64G не найден |
| 125 | Флешка 64 GB Lexar JumpDrive V400 USB 3.0 (`acc-flash_drives-12`; Флешки) | НФ-00001148 | Нет | 0 | Оставлено без фото: найденные чистые ассеты имеют маркировку 256G |
| 126 | Netcraze Air (NC-1613) (`mesh-13`; Mesh-системы) | НФ-00001114 | `main.webp` | 2 | Добавлено |
| 127 | Netcraze Challenger SE (NC-3911) (`mesh-14`; Mesh-системы) | НФ-00001116 | `main.webp` | 1 | Добавлено |
| 128 | Netcraze Extra (NC-1714) (`mesh-15`; Mesh-системы) | НФ-00001115 | `main.webp` | 1 | Добавлено |
| 129 | Netcraze Ultra (NC-1812) (`mesh-16`; Mesh-системы) | НФ-00001117 | `main.webp` | 3 | Добавлено |
| 130 | Куди Cudy M3000S (3-Pack) AX3000 Wi-Fi 6 Mesh Solution (`mesh-17`; Mesh-системы) | НФ-00001029 | `main.webp` | 0 | Добавлено; использован кадр именно 3-Pack без рекламной коробки |
| 131 | SSD 2,5 Lexar 1TB NM610 (`ssd-23`; SSD) | НФ-00001104 | `main.webp` | 0 | Добавлено |
| 132 | APC Easy UPS SRV 3000VA 230V М (`ups-14`; UPS) | НФ-00000789 | `main.webp` | 1 | Добавлено |
| 133 | APC Easy UPS SRV RM 3000VA 230V М (`ups-15`; UPS) | НФ-00000873 | `main.webp` | 1 | Добавлено |
| 134 | APC Easy UPS SRV RM 6000VA 230V М (`ups-16`; UPS) | НФ-00000843 | `main.webp` | 1 | Добавлено; выбран SRV6KRI без rail kit |
| 135 | APC Smart UPS SMC 2000 I С2000VA (`ups-17`; UPS) | НФ-00001138 | `main.webp` | 1 | Добавлено |
| 136 | Куди Cudy WE1300 AC1300 Wireless Dual Band PCIe Adapter (`wifi-17`; Wi-Fi адаптеры) | НФ-00001044 | `main.webp` | 0 | Добавлено |
| 137 | Куди Cudy WE3000 AX3000 Wi-Fi 6 PCI Express Adapter (`wifi-18`; Wi-Fi адаптеры) | НФ-00001045 | `main.webp` | 0 | Добавлено |
| 138 | Куди Cudy WE650 AC650 Wireless Dual-Band PCIe Adapter (`wifi-19`; Wi-Fi адаптеры) | НФ-00001043 | `main.webp` | 0 | Добавлено |
| 139 | Куди Cudy WE9300 BE9300 Wi-Fi 7 PCI Express Adapter (`wifi-20`; Wi-Fi адаптеры) | НФ-00001046 | `main.webp` | 1 | Добавлено; ассет взят со страницы точного WE9300, несмотря на внутреннее имя файла Cudy WE3000S |
| 140 | Куди Cudy WU1400 AC1300 Wi-Fi High Gain USB 3.0 Adapter (`wifi-21`; Wi-Fi адаптеры) | НФ-00001042 | `main.webp` | 0 | Добавлено |

## Обработка изображений

- Все подключённые файлы сохранены локально в `images/products/<id>/`.
- Формат: WebP, холст 1000×1000 px, белый фон `#FFFFFF`.
- Удалены рекламные композиции, коробки и внешние ссылки из карточек; для Mesh использованы только чистые product-only кадры.
- Для Aruba AP11 фон исходной фотографии из FCC-регистрации удалён и заменён на белый.
- Для APC использованы официальные product-rendition изображения Schneider Electric в высоком разрешении.
- Имена товара, ID, SKU, цены, остатки, характеристики и категории не изменялись.

## Источники

### D-Link и Cudy

- D-Link DGE-560T: <https://www.dlink.com/middle-east/en/products/dge-560t-gigabit-desktop-pci-express-adapter>
- Cudy PE10: <https://www.cudy.com/products/pe10-2-0>
- Cudy PE10G: <https://www.cudy.com/en-apac/products/pe10g-1-0>
- Cudy AP1300 Indoor: <https://www.cudy.com/en-us/products/ap1300-1-0>
- Cudy AP1300 Outdoor: <https://www.cudy.com/en-us/products/ap1300-outdoor-1-0>
- Cudy AP3000 Outdoor: <https://www.cudy.com/products/ap3000-outdoor-1-0>
- Cudy M3000S: <https://www.cudy.com/en-eu/products/m3000s-1-0>
- Cudy WE1300: <https://www.cudy.com/products/we1300-1-0>
- Cudy WE3000: <https://www.cudy.com/products/we3000-1-0>
- Cudy WE650: <https://www.cudy.com/products/we650-1-0>
- Cudy WE9300: <https://www.cudy.com/products/we9300-1-0>
- Cudy WU1400: <https://www.cudy.com/products/wu1400-2-0>

### Lexar

- JumpDrive V100: <https://www.lexar.com/global/products/Lexar-JumpDrive-V100-USB-3-0-Flash-Drive/>
- JumpDrive Dual Drive D400: <https://www.lexar.com/global/products/Lexar-JumpDrive-Dual-Drive-D400-USB-3-1-Type-C-/>
- NM610: <https://www.lexar.com/de/products/Lexar-NM610-M-2-2280-NVMe-SSD/>

### Netcraze

- Air NC-1613: <https://netcraze.ru/ru/netcraze-air>
- Challenger SE NC-3911: <https://netcraze.ru/ru/netcraze-challenger-se>
- Extra NC-1714: <https://netcraze.ru/ru/netcraze-extra>
- Ultra NC-1812: <https://netcraze.ru/ru/netcraze-ultra>

### Aruba/HPE и APC

- HPE Aruba AP11 QuickSpecs: <https://www.hpe.com/us/en/collaterals/collateral.a00062187enw.html>
- HPE Aruba AP11 Installation Guide: <https://arubanetworking.hpe.com/techdocs/hardware/instantonaps/ap11/Aruba_AP11_Installation_Guide_EN.pdf>
- FCC external photos for HPE regulatory model APIN0303: <https://fccid.io/Q9DAPIN0303/External-Photos/External-Photos-20180120-v1-APIN0303-External-Photo-3745919>
- APC SRV3KI: <https://www.se.com/za/en/product/SRV3KI/apc-easy-ups-online-srv-3000va-230v/>
- APC SRV3KRI: <https://www.se.com/tr/tr/product/SRV3KRI/apc-easy-ups-srv-rm-3000va-230v/>
- APC SRV6KRI: <https://www.se.com/uk/en/product/SRV6KRI/apc-easy-ups-online-6kva-6kw-rackmount-4u-230v-hard-wire-3wire1p%2Bn%2Be-outlet-intelligent-card-slot-lcd-w-o-rail-kit/>
- APC SMC2000I: <https://www.se.com/uk/en/product/SMC2000I/apc-smartups-c-line-interactive-2000va-tower-230v-6x-iec-c13%201x-iec-c19-outlets-usb-and-serial-communication-avr-graphic-lcd/>

## Права на использование

Для использованных ассетов найден источник производителя или официальной регуляторной документации. Явная отдельная лицензия на коммерческое размещение фотографий на сайте в источниках не указана. Перед объединением Pull Request требуется ручная проверка права коммерческого использования; изображения с неподтверждёнными правами не следует публиковать без такого подтверждения.

## Изменённые файлы

- `products.json` — подключены 24 товара этапа 5, изменены только поля `image` и `images`.
- `images/products/cards-3/`
- `images/products/cards-4/`
- `images/products/cards-5/`
- `images/products/access-10/` … `images/products/access-13/`
- `images/products/acc-flash_drives-9/` … `images/products/acc-flash_drives-10/`
- `images/products/mesh-13/` … `images/products/mesh-17/`
- `images/products/ssd-23/`
- `images/products/ups-14/` … `images/products/ups-17/`
- `images/products/wifi-17/` … `images/products/wifi-21/`
- `PHOTO_STAGE_5_REPORT.md`

SHA коммита и ссылка на Pull Request будут добавлены после финальной проверки и публикации ветки. В `main` изменения не объединялись.
