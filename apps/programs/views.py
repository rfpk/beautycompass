import json
from random import randint, sample
from django.views import View
from django.http import JsonResponse
from django.db.models import F, Q, IntegerField
from django.db.models.functions import Cast
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from apps.products.models import Product
from apps.programs.models import Program, ProgramResult, ComplexResult, Complex
from apps.profile.models import Profile
from apps.testing.models import TestsResult, AnswerProfile

from apps.tools.utils import slugify


class ProgramsSaved(LoginRequiredMixin, ListView):
    model = ProgramResult
    template_name = 'selection/saved.html'
    context_object_name = 'programs'

    def get_pagination(self, type_: str, query_param: str, paginate_by: int = 5):
        data = []
        is_str = isinstance(type_, str)

        if is_str and type_ == 'test':
            data = TestsResult.objects.filter(profile__user=self.request.user).select_related('profile')

        if is_str and type_ == 'program':
            data = ProgramResult.objects.filter(profile__user=self.request.user).select_related('profile')

        if data:
            paginator = Paginator(data, paginate_by)
            page = self.request.GET.get(query_param)
            page = page if page else 1

            try:
                data = paginator.page(page)
            except (InvalidPage, EmptyPage):
                data = paginator.page(paginator.num_pages)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result_tests'] = self.get_pagination('test', 'page_test')
        context['programs'] = self.get_pagination('program', 'page_program')
        return context


class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)
        program = self.get_object()
        context['program_complexes'] = program.program_complexes.all().prefetch_related('products')
        return context


class ProgrammCreateView(LoginRequiredMixin, View):
    def get_tags(self, type: int) -> list:
        """Get Tags Format"""
        match type:
            case 1:
                return [
                    slugify('гидрофильный бальзам'),
                    slugify('гидрофильное масло'),
                    slugify('молочко'),
                    slugify('крем'),
                    slugify('мицеллярная вода'),
                    slugify('двухфазное средство'),
                ]
            case 4:
                return [
                    slugify('сыворотка'),
                    slugify('концентрат'),
                    slugify('эссенция'),
                ]
            case 8:
                return [
                    slugify('AHA-кислоты'),
                    slugify('Гликолевая кислота'),
                    slugify('Миндальная кислота'),
                    slugify('Ретинол / ретиналь'),
                    slugify('Транексамовая кислота'),
                    slugify('Яблочная кислота'),
                ]
            case 10:
                return [
                    slugify('маска'),
                    slugify('тканевая маска'),
                    slugify('альгинатная маска'),
                    slugify('патчи'),
                ]
            case _:
                return []

    def get_age_tags(self, age: str) -> list:
        """Get Age Tags (Principle by age)"""
        match age.lower():
            case 'до 25':
                return [
                    slugify('Акне'),
                    slugify('Пигментация / постакне'),
                    slugify('Черные точки'),
                ]
            case '25-35':
                return [
                    slugify('Пигментация / постакне'),
                    slugify('Снятие раздражения'),
                    slugify('Заживление'),
                ]
            case '35-45' | 'больше 45':
                return [
                    slugify('Тонус / лифтинг кожи'),
                    slugify('Тусклый оттенок / неровная текстура'),
                ]
            case _:
                return []

    def get_skin_tags(self, skin: str) -> list:
        """Get Tags selected problems"""
        match skin.lower():
            case 'обезвоженность':
                return [slugify('Увлажнение'), slugify('Обезвоженность / сухость')]
            case 'пигментация' | 'пигментные пятна':
                return [slugify('Пигментация / постакне')]
            case 'тусклый цвет' | 'тусклый цвет лица':
                return [slugify('Тусклый оттенок / неровная текстура')]
            case 'неровный тон и текстура' | 'неровный тон и текстура кожи':
                return [slugify('Тусклый оттенок / неровная текстура')]
            case 'покраснения и раздражения':
                return [slugify('Снятие раздражения'), slugify('Заживление')]
            case 'воспаления и высыпания':
                return [slugify('Акне')]
            case 'расширенные поры и черные точки':
                return [slugify('Черные точки'), slugify('Тусклый оттенок / неровная текстура')]
            case 'потеря упругости и эластичности' | 'потеря упругости и эластичности, морщины':
                return [slugify('Тонус / лифтинг кожи'), slugify('Мимические морщины')]
            case 'купероз и розацеа':
                return [slugify('Розацеа / купероз')]
            case _:
                return []

    def get_skin_type(self, skin_type: str, sensitive_skin: str = None, type: int = None) -> Q:
        """Get Skin Query"""
        q_object = Q()
        if skin_type and sensitive_skin:
            any_skin = slugify('Любая кожа') if type in [5, 6, 8, 9] else ''
            skin = [slugify(f'{skin_type} кожа'), slugify(f'{sensitive_skin} кожа'), any_skin]
            q_object = Q(prescription__slug__in=skin)
        elif skin_type or sensitive_skin:
            any_skin = slugify('Любая кожа') if skin_type else ''
            skin_type = slugify(f'{skin_type if skin_type else sensitive_skin} кожа')
            q_object = Q(prescription__slug__in=[skin_type, any_skin])
        return q_object

    def get_sex(self, sex: str) -> Q:
        """Get Sex Query"""
        data = []
        if sex == 'Мужчина':
            data = [slugify('Мужская'), slugify('Унисекс')]
        elif sex == 'Женщина':
            data = [slugify('Женская')]
        elif sex == 'Унисекс':
            data = [slugify('Мужская'), slugify('Унисекс'), slugify('Женская')]
        q_object = Q(sex__slug__in=data)
        return q_object

    def get_age(self, age) -> Q:
        """Get Age Query"""
        age_product = slugify('Антивозрастной уход')
        q_objects = Q()
        if age in ['до 25', '25-35', '35-45']:
            # age до 25 исключить Антивозрастной уход
            q_objects = ~Q(key_action__slug__in=[age_product])
        elif age == 'больше 45':
            # больше 45 добавить Антивозрастной уход
            q_objects = Q(key_action__slug__in=[age_product])
        return q_objects

    def exclude_retinol_retinal(self) -> Q:
        """Exclude retinol / retinal if pregnant"""
        slugs = [
            slugify('Ретинол / ретиналь'),
            slugify('Ретинол'),
            slugify('Ретиналь')
        ]
        return ~Q(key_asset__slug__in=slugs)

    def get_products(self, query):
        """Get Products"""
        return (Product.objects
                .select_related('brand', 'format')
                .prefetch_related('prescription', 'sex', 'key_action', 'key_asset')
                .filter(query)
                .defer(
                    'series', 'description', 'use_description', 'composition',
                    'category', 'created_at', 'updated_at', 'new_status', 'tag',
                    'brand__image', 'brand__description', 'brand__short_description',
                    'brand__country', 'brand__favorite_action', 'brand__conversion',
                    'brand__views', 'brand__manufacturer', 'brand__tag', 'brand__slug',
                )
                .annotate(rating_product=F('rating') / 5 * 100)
                .annotate(product_rating_int=Cast('rating_product', IntegerField()))
                .distinct('brand__name'))

    def create_query(self, main_slug: str, second_slug: str, skin_type: str,
                     sensitive_skin: str = None, age: str = None, type: int = None) -> Product:
        """Create Query if products with sex Men < 5"""
        query = Q()
        query &= self.get_skin_type(skin_type, sensitive_skin, type)
        query &= self.get_sex('Женщина')
        query &= self.get_age(age)
        products = (self.get_products(query)
                    .filter(prescription__slug__in=[main_slug])
                    .filter(prescription__slug__in=[second_slug]))
        return products

    def get_products_by_category(self, type: int, skin_type: str = None, hormonal_status: str = None, sex: str = None,
                                 age: str = None, season: str = 1, sensitive_skin: str = None, tags: list = None,
                                 skin_condition: list = None):
        q_objects = Q()

        if skin_type or sensitive_skin:
            q_objects &= self.get_skin_type(skin_type, sensitive_skin, type)

        if sex:
            q_objects &= self.get_sex(sex)

        if age:
            q_objects &= self.get_age(age)

        if int(season) == 4 or (
                hormonal_status and hormonal_status.lower() in ['беременна/кормлю грудью', 'беременна', 'кормлю грудью']
        ):
            q_objects &= self.exclude_retinol_retinal()

        # Get Products
        products = self.get_products(q_objects)

        match type:
            case 1:
                products = (
                    products
                    .filter(prescription__slug__in=[slugify('Демакияж')])
                    .filter(format__slug__in=tags)
                )
            case 2:
                products = (
                    products.filter(prescription__slug__in=[slugify('Умывание')])
                    .filter(prescription__slug__in=[slugify('Для лица')])
                )
            case 3:
                products = (
                    products.filter(prescription__slug__in=[slugify('Тонизирование')])
                    .filter(prescription__slug__in=[slugify('Для лица')])
                )
            case 4:
                main_slug = slugify('Для лица')
                second_slug = slugify('Уходовое средство')

                products = (
                    products
                    .filter(prescription__slug__in=[main_slug])
                    .filter(prescription__slug__in=[second_slug])
                    .filter(format__slug__in=tags)
                )
                # Если пол мужской, теги: мужская / унисекс. Но если не наберется 5 средств
                # с такими тегами, предлагаем с тегом «женская»
                if sex == 'Мужчина' and products.count() < 5:
                    products = (self.create_query(main_slug, second_slug, skin_type, sensitive_skin, age, type)
                                .filter(format__slug__in=tags)
                                )

                # Фильтрация по проблеме
                if skin_condition:
                    skins = []
                    for el in skin_condition:
                        skins += self.get_skin_tags(el)

                    # Фильтрация по Принцип по возрасту
                    age_tags = self.get_age_tags(age)
                    if age_tags:
                        skins = list(set(age_tags + skins))
                    products = products.filter(key_action__slug__in=skins)

                # Если сезон «лето», исключить из выборки средства с активами: AHA-кислоты, ..., Яблочная кислота.
                if int(season) == 4:
                    acids_tags = self.get_tags(8)
                    products = products.exclude(key_asset__slug__in=acids_tags)

                # Если клиентка беременная или кормящая (отметка из теста), то независимо от сезона
                # исключить средства с: Ретинол / ретиналь
            case 5:
                products = (
                    products.filter(prescription__slug__in=[slugify('Уходовое средство')])
                    .filter(prescription__slug__in=[slugify('Для лица')])
                    .filter(prescription__slug__in=[slugify('Дневной крем')])
                )
            case 6:
                products = (
                    products
                    .filter(prescription__slug__in=[slugify('Уходовое средство')])
                    .filter(prescription__slug__in=[slugify('Для лица')])
                    .filter(prescription__slug__in=[slugify('ночной крем'), slugify('ночная маска')])
                )
            case 7:
                products = (
                    products.filter(prescription__slug__in=[slugify('Уходовое средство')])
                    .filter(prescription__slug__in=[slugify('Для кожи вокруг глаз')])
                )
                if sex == 'Мужчина' and products.count() < 5:
                    first_slug = slugify('Уходовое средство')
                    second_slug = slugify('Для кожи вокруг глаз')
                    products = self.create_query(first_slug, second_slug, skin_type, sensitive_skin, age, type)
            case 8:
                def filter_season_query(season):
                    return Q(key_action__slug__in=filter_season[int(season)])

                def check_acids(acids_products, tags):
                    key_asset_slugs = list(acids_products.values_list('key_asset__slug', flat=True))
                    return bool(set(tags).intersection(key_asset_slugs))

                slug = slugify('Солнцезащита')
                filter_season = {
                    1: [slugify('SPF 16-25'), slugify('SPF 26-35')],
                    2: [slugify('SPF 11-15'), slugify('SPF 16-25')],
                    3: [slugify('SPF 16-25'), slugify('SPF 26-35')],
                    4: [slugify('SPF 36-55'), slugify('SPF 56-100')],
                }
                products = (
                    products.filter(prescription__slug__in=[slug])
                )
                products_acids = (products.filter(filter_season_query(season)))
                # Проверка пол мужской, теги: мужская / унисекс. Если не наберется пять средств с таким тегом,
                # предлагаем с тегом «женская».
                if sex == 'Мужчина' and products_acids.count() < 5:
                    products_acids_woman = (self.create_query(slug, slug, skin_type, sensitive_skin, age, type))
                    products_acids_woman_season = products_acids_woman.filter(filter_season_query(season))
                    # Проверка есть ли кислоты в ключевых активах
                    is_asids = check_acids(products_acids_woman_season, tags)
                    if is_asids:
                        products = products_acids_woman.filter(filter_season_query(4))
                    else:
                        products = products_acids_woman_season
                else:
                    # Проверка есть ли кислоты в ключевых активах
                    is_acids = check_acids(products_acids, tags)

                    if is_acids:
                        # Проверка есть ли кислоты в ключевых активах
                        products = (products.filter(Q(key_action__slug__in=filter_season[4])))
                    else:
                        products = products_acids
            case 9:
                products = (
                    products.filter(prescription__slug__in=[slugify('Для лица')])
                    .filter(prescription__slug__in=[slugify('Отшелушивание')])
                )
                if sex == 'Мужчина' and products.count() < 5:
                    first_slug = slugify('Для лица')
                    second_slug = slugify('Отшелушивание')
                    products = self.create_query(first_slug, second_slug, skin_type, sensitive_skin, age, type)
            case 10:
                def random_num(max: int):
                    return randint(0, max - 1)

                main_slug = slugify('Для лица')
                second_slug = slugify('Уходовое средство')
                products = (
                    products.filter(prescription__slug__in=[main_slug])
                    .filter(prescription__slug__in=[second_slug])
                    .filter(format__slug__in=tags)
                )

                # Если пол мужской, теги: мужская / унисекс. Если не наберется пять средств
                # с таким тегом, предлагаем с тегом «женская».
                if sex == 'Мужчина' and products.count() < 5:
                    products = (self.create_query(main_slug, second_slug, skin_type, sensitive_skin, age, type)
                                .filter(format__slug__in=tags))

                # В этой выборке подбираем пять масок с разным функционалом.

                # Одна маска с тегом: Очищение.
                clean_product = products.filter(key_action__slug__in=[slugify('Очищение')])
                clean_product = list(
                    clean_product.values_list('id', 'slug', 'thumbnail', 'name', 'brand__name', 'product_rating_int'))
                clean_product = sample(clean_product, min(len(clean_product), 1))

                # И еще четыре маски по выбранной проблеме (как и целевой уход)
                if skin_condition:
                    skins = []
                    for el in skin_condition:
                        skins += self.get_skin_tags(el)
                    products = (products
                                .filter(key_action__slug__in=skins)
                                .exclude(key_action__slug__in=[slugify('Очищение')]))
                else:
                    if clean_product:
                        products = products.exclude(key_action__slug__in=[slugify('Очищение')])

                products = list(
                    products.values_list('id', 'slug', 'thumbnail', 'name', 'brand__name', 'product_rating_int'))
                products = sample(products, min(len(products), 4))
                products = clean_product + products
                return products
            case _:
                pass

        # Random Products
        products = list(products.values_list('id', 'slug', 'thumbnail', 'name', 'brand__name', 'product_rating_int'))
        products = sample(products, min(len(products), 5))
        return products

    def get_answers_test(self, test_name: str, profile: Profile) -> dict:
        """Get Answers user test"""
        answers = get_list_or_404(
            AnswerProfile,
            test_result_user=test_name,
            profile=profile
        )

        data = {
            'skin_condition': None,
            'skin_around_eye': None,
        }

        def append_data(type_param: str, text: str):
            if type_param in data:
                data[type_param].append(text)
            else:
                data[type_param] = [text]

        for answer in answers:
            options = answer.option.all()
            for option in options:
                match option.question.text.lower():
                    case 'вы':
                        data['sex'] = option.text.capitalize()
                    case 'вам':
                        data['age'] = option.text
                    case 'ваши ощущения после умывания водой':
                        skin_type = {
                            'кожу стягивает': 'Сухая',
                            'есть ощущение чистоты и свежести': 'Нормальная',
                            'спустя некоторое время появляется жирный блеск': 'Комбинированная',
                            'есть ощущение недостаточного очищения кожи': 'Жирная',
                        }
                        data['skin_type'] = skin_type[option.text.lower()]
                    case 'поры на вашем лице':
                        data['pore'] = option.text
                    case 'бывают ли воспаления':
                        data['inflammation'] = option.text
                    case 'какой у вас тип старения':
                        data['aging_type'] = option.text
                    case 'что вы отмечаете прямо сейчас':
                        append_data('skin_condition', option.text)
                    case 'кожа вокруг глаз':
                        append_data('skin_around_eye', option.text)
                    case 'часто ли уходовая косметика вызывает раздражение, покраснение, жжение?':
                        data['allergy'] = 'Чувствительная' if option.text == 'да' else None
                    case ('в данный момент вы беременны, кормите грудью или '
                          'планируете беременность в течение ближайших 6 месяцев?'):
                        if option.text == 'да':
                            data['hormonal_status'] = 'Беременна/кормлю грудью'
                        else:
                            data['hormonal_status'] = 'Не беременна/не кормлю грудью'
                    case _:
                        pass
        return data

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        is_result_test = self.request.GET.get('question_2', None)  # Взять результат теста
        season = self.request.GET.get('question_1', None)  # Сезон
        sex = self.request.GET.get('question_3', None)  # Пол
        age = self.request.GET.get('question_4', None)  # Возраст
        skin_type = self.request.GET.get('question_5', None)  # Тип Кожи
        hormonal_status = self.request.GET.get('question_8', None)  # Гормональный статус
        sensitive_skin = self.request.GET.get('question_9', None)  # Чувствительная кожа
        skin_condition = self.request.GET.getlist('question_7', None)
        aging_type = self.request.GET.get('question_6', None)  # Тип Старения
        program = self.request.GET.get('question_10', None)  # Программа
        allergy = self.request.GET.get('question_11', None)  # Алергия
        price_category = self.request.GET.get('question_12', None)  # Ценовая категория
        cosmetics_category = self.request.GET.get('question_13', None)  # Категория косметики
        country = self.request.GET.get('question_14', None)  # Страна производства
        exclude_assets = self.request.GET.get('question_15', None)  # Исключить активы

        skin = sensitive_skin if sensitive_skin else skin_type

        if is_result_test == 'yes':
            # Если Пользователь выбрал Тест
            test_name = self.request.GET.get('test_name', None)  # Имя Теста
            # Получение ответов на тест
            data = self.get_answers_test(test_name, profile)

            # Установка параметров
            sex = data['sex']
            age = data['age']
            skin_type = data['skin_type']
            hormonal_status = data['hormonal_status']
            sensitive_skin = data['allergy']
            skin_condition = data['skin_condition']

            # Получение продуктов
            skin = sensitive_skin if sensitive_skin else skin_type

        # Получение Продуктов (Демакияж)
        makeup_removers = self.get_products_by_category(1, skin, hormonal_status, tags=self.get_tags(1))

        # Получение Продуктов (Очищение)
        cleansing = self.get_products_by_category(2, skin, hormonal_status, sex=sex)

        # Получение Продуктов (Тонизирование)
        toning = self.get_products_by_category(3, skin, hormonal_status, sex=sex)

        # Получение Продуктов (Целевой Уход)
        targeted_care = self.get_products_by_category(4, skin_type, hormonal_status, sex, age, season,
                                                      tags=self.get_tags(4), skin_condition=skin_condition)

        # Получение Продуктов (Дневной базовый уход)
        day_basic_care = self.get_products_by_category(5, skin_type, hormonal_status, sex, age, season,
                                                       sensitive_skin)
        # Получение Продуктов (Ночной базовый уход)
        night_basic_care = self.get_products_by_category(6, skin_type, hormonal_status, sex, age, season,
                                                         sensitive_skin)

        # Получение Продуктов (Для кожи вокруг глаз)
        around_eyes = self.get_products_by_category(7, skin_type, hormonal_status, sex, age, season)

        # Получение Продуктов (Защита от солнца)
        sun_protection = self.get_products_by_category(8, skin_type, hormonal_status, sex, age, season,
                                                       sensitive_skin, tags=self.get_tags(8))

        # Получение Продуктов (Отшелушивание)
        exfoliation = self.get_products_by_category(9, skin_type, hormonal_status, sex, age,
                                                    sensitive_skin=sensitive_skin)

        # Получение Продуктов (Дополнительный уход)
        additional_care = self.get_products_by_category(10, sex=sex, age=age, tags=self.get_tags(10),
                                                        skin_condition=skin_condition, sensitive_skin=sensitive_skin)

        complexes = list((Complex.objects
                          .filter(program__is_publish=True)
                          .select_related('program')).values('recommendation', 'title', 'program__id'))

        return render(request, 'programs/program.html', {
            'makeup_removers': makeup_removers,
            'cleansing': cleansing,
            'toning': toning,
            'targeted_care': targeted_care,
            'day_basic_care': day_basic_care,
            'night_basic_care': night_basic_care,
            'around_eyes': around_eyes,
            'exfoliation': exfoliation,
            'sun_protection': sun_protection,
            'additional_care': additional_care,
            'complexes': complexes,
            'program_id': complexes[0]['program__id'],
            'nickname': profile.nickname,
            'skin': skin,
            'sensitive_skin': sensitive_skin,
            'season': season,
            'skin_conditions': skin_condition,
        })

    def post(self, request, *args, **kwargs):
        program_id = request.POST.get('program_id')
        program_name = request.POST.get('program_name')
        program_desc = request.POST.get('program_description')
        data = json.loads(request.POST.get('data'))

        profile = Profile.objects.get(user=request.user)
        program = Program.objects.filter(id=program_id).first()

        # Сохранение Программы
        program_result = ProgramResult.objects.create(
            name=program_name,
            profile=profile,
            program=program,
            description=program_desc,
        )
        for elements in data:
            products_id = []
            complex_name = None
            recommendation = None
            for elem in elements:
                products_id.append(elem['productId'])
                recommendation = elem['recomendation']
                complex_name = elem['complexesName']

            # Сохранения Комплекса
            products = Product.objects.filter(pk__in=products_id)
            complex_result = ComplexResult.objects.create(
                title=complex_name,
                recommendation=recommendation,
                program=program_result
            )
            complex_result.products.add(*products)
            complex_result.save()

        return JsonResponse({'status': 'success', 'message': 'Answer Success Added'})
