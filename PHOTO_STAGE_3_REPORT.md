# АКС — этап 3 из 5: фотографии товаров из 1С

## Область работ

- Репозиторий: `treasuremarci-stack/rgw-store`
- Исходная ветка: `main` на коммите `c737ab146feb08ac961d9e8fd31c4d3f292994ee`
- Рабочая ветка: `photos-1c-stage-3`
- Источник нумерации: `stage1_aks_1c_inventory.xlsx`, лист `Без фото`
- Обработан только диапазон №57–84 из первоначального отчёта.
- `PROJECT_STATUS.md` не изменялся.

## Результат по товарам

| № | Название товара | SKU | ID | Основное фото | Доп. фото | Статус |
|---:|---|---|---|---:|---:|---|
| 57 | Оперативка Corsair Vengeance DDR5 16 Gb 6000 | НФ-00001165 | `ram-13` | 1 | 0 | Добавлено |
| 58 | Оперативка Kingston FURY Beast 16 ГБ DDR5 6000 | НФ-00001123 | `ram-14` | 1 | 1 | Добавлено |
| 59 | Оперативка Lexar DDR4 3200 8 Gb | НФ-00000388 | `ram-15` | 1 | 1 | Добавлено |
| 60 | Оперативка Lexar DDR4 3200 32 Gb | НФ-00000390 | `ram-16` | 1 | 1 | Добавлено |
| 61 | Оперативка Lexar DDR4-3200 32GB Ноутбук | НФ-00000381 | `ram-17` | 1 | 0 | Добавлено |
| 62 | Оперативка Lexar DDR5-5600 32GB | НФ-00000382 | `ram-18` | 1 | 0 | Добавлено |
| 63 | Кулер Segotep cooler К6 PRO | НФ-00001162 | `cooling-22` | 1 | 0 | Добавлено |
| 64 | Кулер реверсивный | НФ-00001164 | `cooling-23` | 0 | 0 | Не добавлено: нет бренда и точной модели |
| 65 | Зажим Пач Панель | НФ-00000508 | `patch_panels-3` | 0 | 0 | Не добавлено: нет производителя и артикула |
| 66 | Принтер CANON ISENSYS 463DW | НФ-00000401 | `printers-11` | 1 | 1 | Добавлено |
| 67 | Принтер Canon i-SENSYS MF664Cdw | НФ-00001103 | `printers-12` | 1 | 1 | Добавлено |
| 68 | Принтер Canon i-SENSYS MF667Cdw | НФ-00001128 | `printers-13` | 1 | 1 | Добавлено |
| 69 | Принтер EPSON L15150 | НФ-00000787 | `printers-14` | 1 | 0 | Добавлено |
| 70 | Принтер HP Color Laser Jet Pro 4303 fdw | НФ-00001142 | `printers-15` | 1 | 0 | Добавлено |
| 71 | Принтер HP Laser Jet Pro 4003 dn | НФ-00001152 | `printers-16` | 1 | 0 | Добавлено |
| 72 | Принтер HP Laser Jet MFP M141W | НФ-00001153 | `printers-17` | 1 | 1 | Добавлено |
| 73 | Проектор EPSON CO-W01 | НФ-00001149 | `acc-projectors_screens-20` | 1 | 1 | Добавлено |
| 74 | Проектор EPSON EB-X49 | НФ-00001151 | `acc-projectors_screens-21` | 1 | 0 | Добавлено |
| 75 | Процессор Intel Core i5 -14400 | НФ-00000436 | `cpu-18` | 1 | 0 | Добавлено |
| 76 | Процессор TRAY Ultra 5 225K | НФ-00001120 | `cpu-19` | 0 | 0 | Не добавлено: модель 225K не подтверждена в каталоге Intel |
| 77 | Процессор TRAY Ultra 7 270K Plus | НФ-00001121 | `cpu-20` | 1 | 0 | Добавлено |
| 78 | Бейсус C00081100121-00 BackseatPal L1 In-vehicle Car Charger 3U+3C 110W Cosmic Black | НФ-00000009 | `acc-other_accessories-7` | 1 | 0 | Добавлено |
| 79 | Бейсус P1011160A113-01 Palm Fast Charger C+U 30W EU Cluster Black | НФ-00000013 | `acc-other_accessories-8` | 1 | 0 | Добавлено |
| 80 | Бейсус WKCD010013 Orange Dot Wireless Presenter (Green Laser)(Charging) Grey | НФ-00000015 | `acc-other_accessories-9` | 1 | 0 | Добавлено |
| 81 | Коврик | НФ-00000458 | `acc-other_accessories-10` | 0 | 0 | Не добавлено: нет бренда и точной модели |
| 82 | Keenetic Carrier KN-1721 | НФ-00000820 | `routers-25` | 1 | 1 | Добавлено |
| 83 | Keenetic Hopper SE KN-3812 | НФ-00000823 | `routers-26` | 1 | 1 | Добавлено |
| 84 | Keenetic Launcher KN-1221-01 | НФ-00000819 | `routers-27` | 1 | 0 | Добавлено |

## Сводка

- Проверено: **28 из 28** товаров.
- Фотографии добавлены: **24 товара**.
- Добавлено локальных изображений: **34 WebP** — 24 основных и 10 дополнительных.
- Без фотографий оставлено: **4 товара**.
- Внешние URL в карточки товаров не добавлялись.
- ID, SKU, названия, цены, характеристики, категории и фильтры не изменялись.

### Причины отсутствия фото

1. `cooling-23`: название «Кулер реверсивный» не содержит бренда или точной модели; безопасно выбрать изображение невозможно.
2. `patch_panels-3`: «Зажим Пач Панель» — неоднозначное общее название без производителя и артикула.
3. `cpu-19`: в официальных материалах Intel подтверждаются Core Ultra 5 225 и 225F, но точная модель «225K» не подтверждена; похожее изображение использовать нельзя.
4. `acc-other_accessories-10`: название «Коврик» не содержит бренда, типа и модели.

## Источники изображений

Использовались официальные страницы производителей, официальные региональные магазины, дистрибьюторы и точные карточки товаров. Для каждой модели проверялось совпадение названия, артикула или модельного кода.

- Corsair Vengeance: [Terabyte Shop](https://www.terabyteshop.com.br/produto/41295/memoria-ddr5-corsair-vengeance-16gb-6000mhz-cinza-cmk16gx5m1e6000z36).
- Kingston FURY Beast: [официальная страница Kingston](https://www.kingston.com/en/memory/gaming/kingston-fury-beast-ddr5-memory?kit=single+module&speed=6000mt%2Fs&total+%28kit%29+capacity=16gb).
- Lexar DDR4 UDIMM, DDR4 SODIMM и DDR5 UDIMM: [официальные страницы Lexar](https://americas.lexar.com/product/lexar-ddr4-3200-udimm-desktop-memory/), [DDR4 SODIMM](https://americas.lexar.com/product/lexar-ddr4-3200-sodimm-laptop-memory/), [DDR5 UDIMM](https://www.lexar.com/pl/products/Lexar-DDR5-UDIMM-Desktop-Memory/).
- Segotep K6 PRO: [официальная страница Segotep](https://www.segotep.com/CN/home/product?id=ec3608b1-63f3-4cc3-bd2b-7bdb9edf5f29).
- Canon MF463dw, MF664Cdw и MF667Cdw: точные карточки [MF463dw](https://okoffice.bg/bg/p/1000000000046058/lazeren-printer-3v1-canon-mf463dw), [MF664Cdw](https://www.printerland.co.uk/product/canon-i-sensys-mf664cdw/172064), [MF667Cdw](https://www.printerland.co.uk/product/canon-i-sensys-mf667cdw/172065).
- Epson L15150: [точная карточка Epson L15150](https://www.bilsarf.com.tr/urun/epson-ecotank-l15150).
- HP 4303fdw, HP 4003dn и HP M141w: точные карточки [4303fdw](https://www.infomulti.com.br/impressoras/laser/multifuncional-hp-cor-laserjet-pro-4303fdw-33ppm-5hh67a-696), [4003dn](https://chipsync.ae/products/hp-laserjet-pro-4003dn-sku-2z609ab19), [M141w](https://www.kio.rs/srb-rs/product/hp-laserjet-mfp-m141w/).
- Epson CO-W01 и EB-X49: официальные страницы [CO-W01](https://www.epson.co.za/projectors/business-education/co-w01-v11ha86040) и [EB-X49](https://www.epson.co.ke/projectors/business-education/eb-x49-v11h982040); для CO-W01 использован точный packshot из [ICOM](https://icom.ge/cdn/shop/products/w01_w_std_01_png.png?v=1708261660).
- Intel Core i5-14400 и Core Ultra 7 270K Plus: точные карточки [i5-14400](https://compx.ua/procesor-intel-core-i5-14400-bx8071514400-t-2299471/) и [270K Plus](https://28bit.ru/protsessor-intel-core-ultra-7-270k-plus-oem-at807683b9b4884/).
- Baseus BackseatPal L1, Palm 30W и Orange Dot WKCD010013: [BackseatPal](https://baseus.co.za/products/baseus-backseatpal-l1-in-vehicle-car-charger-110w), [Palm](https://b2b.e-baseus.com/5126-baseus-palm-szybka-ladowarka-sieciowa-c-u-30w-eu-cluster-black.html), [официальная карточка Orange Dot](https://baseusofficialstore.com/product/baseus-orange-dot-wireless-presenter-green-lasercharging-grey/).
- Keenetic Carrier и Hopper SE: [официальные страницы Keenetic](https://keenetic.com/en/keenetic-carrier) и [Hopper SE](https://keenetic.com/en/keenetic-hopper-se).
- Keenetic Launcher KN-1221-01: точная карточка [G-Store](https://www.g-store.org/product/wi-fi-router-keenetic-launcher-kn-1221).

### Проверка прав использования

Для поиска приоритетно использовались страницы производителей и точные карточки поставщиков. В открытых источниках не найдено универсального разрешения на повторное коммерческое использование всех изображений. Поэтому перед публичной коммерческой публикацией следует подтвердить право использования изображений у поставщика или правообладателя каталога. В репозитории сохранены только локальные оптимизированные WebP-файлы; внешние ссылки на изображения сайтом не загружаются.

## Обработка и проверка

- Все добавленные файлы — WebP `1000×1000`, RGB.
- Фон по углам проверен как `#FFFFFF`.
- Изображения приведены к единому белому холсту и масштабу без изменения внешнего вида товара.
- Проверены пути из `products.json`; битых ссылок на добавленные изображения нет.
- Выполнены `node --check product.js`, `node --check rgw_global_catalog.js` и `git diff --check`.
- Изменены только записи изображений 24 товаров этапа 3 и новые папки изображений; общие скрипты, категории и `PROJECT_STATUS.md` не изменялись.

## Изменённые файлы

- `products.json`
- `images/products/ram-13/` … `images/products/ram-18/`
- `images/products/cooling-22/`
- `images/products/printers-11/` … `images/products/printers-17/`
- `images/products/acc-projectors_screens-20/` и `acc-projectors_screens-21/`
- `images/products/cpu-18/` и `cpu-20/`
- `images/products/acc-other_accessories-7/` … `acc-other_accessories-9/`
- `images/products/routers-25/` … `routers-27/`
- `PHOTO_STAGE_3_REPORT.md`

## GitHub

- SHA финального коммита: `01872560d0f2e2d6e5c11b961f90924518f39525`.
- Pull Request в `main`: [#3 — АКС — этап 3: фотографии товаров из 1С (№57–84)](https://github.com/treasuremarci-stack/rgw-store/pull/3).
- Объединение Pull Request не выполнялось.
