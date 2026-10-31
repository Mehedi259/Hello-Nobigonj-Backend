from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.categories.models import Category
from apps.authors.models import Author
from apps.articles.models import Article
from apps.comments.models import Comment
from apps.subscribers.models import Subscriber
from apps.notifications.models import Notification
from apps.media_library.models import MediaFile
from apps.settings_app.models import SiteSetting
from apps.accounts.models import ActivityLog

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial realistic database records for Hello Desh News Portal and Admin Dashboard'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding Hello Desh database...'))

        # 1. Users
        admin_user, _ = User.objects.get_or_create(
            email='admin@hellodesh.com',
            defaults={
                'username': 'admin',
                'first_name': 'Mehedi',
                'last_name': 'Hasan',
                'role': 'superadmin',
                'status': 'active',
                'is_staff': True,
                'is_superuser': True,
                'avatar_url': '/images/admin-avatar.jpg',
                'bio': 'Chief Editor & Lead Administrator at Hello Desh',
                'designation': 'প্রধান সম্পাদক',
                'phone': '+880 1711-223344'
            }
        )
        admin_user.set_password('adminpassword123')
        admin_user.save()

        editor_user, _ = User.objects.get_or_create(
            email='editor@hellodesh.com',
            defaults={
                'username': 'editor',
                'first_name': 'শাকিল',
                'last_name': 'আহমেদ',
                'role': 'editor',
                'status': 'active',
                'is_staff': True,
                'avatar_url': '/images/reporter-rakib.jpg',
                'designation': 'বার্তা সম্পাদক',
                'phone': '+880 1722-334455'
            }
        )
        editor_user.set_password('editorpassword123')
        editor_user.save()

        reporter_user, _ = User.objects.get_or_create(
            email='reporter@hellodesh.com',
            defaults={
                'username': 'reporter',
                'first_name': 'মাহমুদুল',
                'last_name': 'হাসান',
                'role': 'reporter',
                'status': 'active',
                'is_staff': True,
                'avatar_url': '/images/reporter-rakib.jpg',
                'designation': 'বিশেষ প্রতিনিধি',
                'phone': '+880 1733-445566'
            }
        )
        reporter_user.set_password('reporterpassword123')
        reporter_user.save()

        self.stdout.write(self.style.SUCCESS('✓ Admin, Editor & Reporter accounts ready!'))

        # 2. Categories
        categories_data = [
            {'name': 'জাতীয়', 'name_en': 'National', 'slug': 'national', 'icon_name': 'Landmark', 'color': '#2563eb', 'order': 1},
            {'name': 'রাজনীতি', 'name_en': 'Politics', 'slug': 'politics', 'icon_name': 'Megaphone', 'color': '#dc2626', 'order': 2},
            {'name': 'অর্থনীতি', 'name_en': 'Economy', 'slug': 'economy', 'icon_name': 'TrendingUp', 'color': '#16a34a', 'order': 3},
            {'name': 'আন্তর্জাতিক', 'name_en': 'International', 'slug': 'international', 'icon_name': 'Globe', 'color': '#9333ea', 'order': 4},
            {'name': 'খেলাধুলা', 'name_en': 'Sports', 'slug': 'sports', 'icon_name': 'Trophy', 'color': '#ea580c', 'order': 5},
            {'name': 'বিনোদন', 'name_en': 'Entertainment', 'slug': 'entertainment', 'icon_name': 'Film', 'color': '#db2777', 'order': 6},
            {'name': 'তথ্যপ্রযুক্তি', 'name_en': 'Technology', 'slug': 'technology', 'icon_name': 'Cpu', 'color': '#0284c7', 'order': 7},
            {'name': 'জীবনযাপন', 'name_en': 'Lifestyle', 'slug': 'lifestyle', 'icon_name': 'Heart', 'color': '#0d9488', 'order': 8},
        ]

        cat_objs = {}
        for c in categories_data:
            obj, _ = Category.objects.update_or_create(
                slug=c['slug'],
                defaults=c
            )
            cat_objs[c['slug']] = obj

        self.stdout.write(self.style.SUCCESS(f'✓ {len(cat_objs)} Categories created!'))

        # 3. Authors
        authors_data = [
            {'name': 'ডেস্ক রিপোর্ট', 'role': 'প্রধান প্রতিবেদক', 'email': 'desk@hellodesh.com', 'avatar_url': '/images/reporter-rakib.jpg', 'location': 'ঢাকা'},
            {'name': 'শাকিল আহমেদ', 'role': 'রাজনৈতিক প্রতিবেদক', 'email': 'shakil@hellodesh.com', 'avatar_url': '/images/reporter-rakib.jpg', 'location': 'ঢাকা', 'user': editor_user},
            {'name': 'মাহমুদুল হাসান', 'role': 'বিশেষ প্রতিনিধি', 'email': 'mahmud@hellodesh.com', 'avatar_url': '/images/reporter-rakib.jpg', 'location': 'মুন্সীগঞ্জ', 'user': reporter_user},
            {'name': 'তানভীর আহমেদ', 'role': 'অর্থনীতি প্রতিনিধি', 'email': 'tanvir@hellodesh.com', 'avatar_url': '/images/reporter-rakib.jpg', 'location': 'মতিঝিল, ঢাকা'},
            {'name': 'মেহজাবিন চৌধুরী', 'role': 'বিনোদন ও সংস্কৃতি প্রতিবেদক', 'email': 'mehzabin@hellodesh.com', 'avatar_url': '/images/admin-avatar.jpg', 'location': 'ঢাকা'},
        ]

        author_objs = {}
        for a in authors_data:
            user_inst = a.pop('user', None)
            obj, _ = Author.objects.update_or_create(
                email=a['email'],
                defaults={**a, 'user': user_inst}
            )
            author_objs[a['name']] = obj

        self.stdout.write(self.style.SUCCESS(f'✓ {len(author_objs)} Authors created!'))

        # 4. Articles
        now = timezone.now()
        articles_data = [
            {
                'title': 'দেশের উন্নয়নে তরুণদের ভূমিকা অত্যন্ত গুরুত্বপূর্ণ: প্রধান উপদেষ্টা',
                'slug': 'role-of-youth-in-national-development-chief-adviser',
                'subtitle': 'নতুন বাংলাদেশ বিনির্মাণে তারুণ্যের শক্তিই মূল চালিকাশক্তি হতে যাচ্ছে',
                'excerpt': 'দেশের উন্নয়ন ও অগ্রগতিতে তরুণদের ভূমিকা অত্যন্ত গুরুত্বপূর্ণ বলে মন্তব্য করেছেন প্রধান উপদেষ্টা। তিনি বলেন, তরুণদের হাত ধরেই বৈষম্যহীন এবং সমৃদ্ধ এক নতুন বাংলাদেশ গড়ে উঠবে...',
                'content': 'দেশের উন্নয়ন ও অগ্রগতিতে তরুণদের ভূমিকা অত্যন্ত গুরুত্বপূর্ণ বলে মন্তব্য করেছেন প্রধান উপদেষ্টা ড. মুহাম্মদ ইউনূস। তিনি বলেন, তারুণ্যের স্বপ্ন এবং আত্মত্যাগের মধ্য দিয়েই এসেছে আমাদের নতুন স্বাধীনতা। এই তরুণদের মেধা, সততা ও উদ্ভাবনী ক্ষমতাকে কাজে লাগিয়েই আমরা বিশ্বদরবারে মাথা উঁচু করে দাঁড়াব।\n\nরাজধানীতে আয়োজিত এক সংলাপে প্রধান উপদেষ্টা বলেন, বিগত কয়েক দশকে বাংলাদেশ নানা সংকটের মধ্য দিয়ে গেছে। তবে চব্বিশের জুলাই অভ্যুত্থান প্রমাণ করেছে, দেশের তরুণরা কোনো অন্যায়কে মেনে নিতে রাজি নয়। আজ দেশ পুনর্গঠনে তরুণদের সেই প্রত্যয়কেই আমাদের মূল শক্তি হিসেবে বেছে নিতে হবে।\n\nপ্রধান উপদেষ্টা আরও উল্লেখ করেন, শিক্ষা ব্যবস্থার আধুনিকায়ন এবং কর্মসংস্থানের নতুন ক্ষেত্র তৈরি করা সরকারের অন্যতম প্রধান অগ্রাধিকার। ডিজিটাল বাংলাদেশ থেকে মানবিক ও প্রযুক্তিনির্ভর বাংলাদেশে রূপান্তরে তরুণদের মেধা কাজে লাগানো হবে। তিনি যুবসমাজকে ঐক্যবদ্ধ হয়ে দেশের শান্তি ও শৃঙ্খলা বজায় রাখার আহ্বান জানান।',
                'category': cat_objs['national'],
                'author': author_objs['ডেস্ক রিপোর্ট'],
                'image_url': '/images/hero-yunus.jpg',
                'image_caption': 'রাজধানীতে অনুষ্ঠানে বক্তব্য রাখছেন অন্তর্বর্তীকালীন সরকারের প্রধান উপদেষ্টা ড. মুহাম্মদ ইউনূস।',
                'is_hero': True,
                'is_breaking': True,
                'is_featured': True,
                'views': 18450,
                'tags': ['প্রধান উপদেষ্টা', 'ড. ইউনূস', 'জাতীয়', 'বাংলাদেশ', 'তরুণ সমাজ'],
                'published_at': now - timedelta(hours=2)
            },
            {
                'title': 'ছাত্রদের নতুন কর্মসূচি: কাল সারাদেশে মানববন্ধন',
                'slug': 'students-new-program-nationwide-human-chain-tomorrow',
                'subtitle': 'শিক্ষার্থীদের ন্যায্য দাবি আদায়ে রাজপথে থাকার ঘোষণা',
                'excerpt': 'সরকারের বিভিন্ন নীতিগত সিদ্ধান্তের প্রতিবাদে দেশের বিভিন্ন স্থানে আগামীকাল ছাত্রদের মানববন্ধন কর্মসূচি পালনের ঘোষণা দেওয়া হয়েছে...',
                'content': 'শিক্ষা প্রতিষ্ঠানের সংস্কার এবং শিক্ষার্থীদের নিরাপত্তা নিশ্চিতকরণসহ বিভিন্ন দাবিতে আগামীকাল সারাদেশে মানববন্ধন কর্মসূচি ঘোষণা করেছে ছাত্র প্রতিনিধিরা।\n\nআজ দুপুরে ঢাকা বিশ্ববিদ্যালয় ক্যাম্পাসে আয়োজিত এক জরুরি সংবাদ সম্মেলনে ছাত্র প্রতিনিধিরা এই কর্মসূচির ঘোষণা দেন। তারা জানান, দেশের সব বিশ্ববিদ্যালয় ও কলেজে একযোগে এই শান্তিপূর্ণ মানববন্ধন পালিত হবে। কোনো ধরনের উসকানি বা বিশৃঙ্খলা ছাড়াই শিক্ষার্থীরা নিজেদের দাবি তুলে ধরবেন।',
                'category': cat_objs['politics'],
                'author': author_objs['শাকিল আহমেদ'],
                'image_url': '/images/students-rally.jpg',
                'image_caption': 'বিক্ষোভে অংশ নিচ্ছেন সাধারণ শিক্ষার্থীরা। ছবি: হ্যালো দেশ',
                'is_featured': True,
                'featured_order': 1,
                'views': 12450,
                'tags': ['ছাত্র আন্দোলন', 'রাজনীতি', 'মানববন্ধন', 'ঢাকা বিশ্ববিদ্যালয়'],
                'published_at': now - timedelta(hours=2, minutes=15)
            },
            {
                'title': 'পদ্মা সেতুতে যান চলাচল স্বাভাবিক',
                'slug': 'traffic-normal-on-padma-bridge',
                'subtitle': 'দক্ষিণাঞ্চলের সঙ্গে নির্বিঘ্ন যোগাযোগ বজায় রয়েছে',
                'excerpt': 'পদ্মা সেতুতে যান চলাচল স্বাভাবিক রয়েছে; সেতু কর্তৃপক্ষ জানিয়েছে, আজ সকাল থেকে কোনো সমস্যা নেই এবং যানবাহন নির্বিঘ্নে চলাচল করছে...',
                'content': 'দক্ষিণাঞ্চলের প্রবেশদ্বার পদ্মা সেতু দিয়ে যানবাহন চলাচল স্বাভাবিক রয়েছে। ভোর থেকে টোল প্লাজায় কোনো ধরনের যানজট সৃষ্টি হয়নি এবং নির্বিঘ্নে চলাচল করছে ছোট-বড় সব ধরনের গাড়ি।\n\nপদ্মা সেতু কর্তৃপক্ষের দায়িত্বশীল কর্মকর্তারা জানিয়েছেন, নিয়মিত ট্রাফিক মনিটরিং এবং অতিরিক্ত টোল বুথ সচল থাকায় চালক ও যাত্রীরা স্বস্তির সঙ্গে সেতু পার হতে পারছেন। দুর্ঘটনা রোধে গতিসীমা নিয়ন্ত্রণে নজরদারি অব্যাহত রয়েছে।',
                'category': cat_objs['national'],
                'author': author_objs['মাহমুদুল হাসান'],
                'image_url': '/images/padma-bridge.jpg',
                'image_caption': 'পদ্মা সেতুতে সকালের স্বাভাবিক যান চলাচলের দৃশ্য। ছবি: সংগৃহীত',
                'is_featured': True,
                'featured_order': 2,
                'views': 9870,
                'tags': ['পদ্মা সেতু', 'যোগাযোগ', 'জাতীয়', 'সড়ক পরিবহন'],
                'published_at': now - timedelta(hours=3)
            },
            {
                'title': 'ঢাকায় আগামী সপ্তাহ থেকে মেট্রোরেলের আরও একটি স্টেশন চালু হচ্ছে',
                'slug': 'another-metro-station-opens-in-dhaka-next-week',
                'excerpt': 'রাজধানীবাসীর যাতায়াত আরও দ্রুত ও সুবিধাজনক করতে আগামী সপ্তাহ থেকে চালু হচ্ছে মেট্রোরেলের নতুন স্টেশন...',
                'content': 'ঢাকা ম্যাস ট্রানজিট কোম্পানি লিমিটেড (ডিএমটিসিএল) জানিয়েছে, এমআরটি লাইন-৬ এর সম্প্রসারিত অংশের একটি নতুন স্টেশন আগামী সপ্তাহ থেকেই যাত্রীদের জন্য উন্মুক্ত করে দেওয়া হবে। এর ফলে ট্রাফিকের চাপ উল্লেখযোগ্য হারে কমে আসবে।',
                'category': cat_objs['national'],
                'author': author_objs['ডেস্ক রিপোর্ট'],
                'image_url': '/images/metro-rail.jpg',
                'views': 8420,
                'tags': ['মেট্রোরেল', 'ঢাকা', 'যোগাযোগ', 'ডিএমটিসিএল'],
                'published_at': now - timedelta(hours=3, minutes=30)
            },
            {
                'title': 'নির্বাচন নিয়ে কোনো অনিশ্চয়তা নেই: সিইসি',
                'slug': 'no-uncertainty-about-election-cec',
                'excerpt': 'প্রধান নির্বাচন কমিশনার জানিয়েছেন, যথাসময়ে অবাধ ও সুষ্ঠু নির্বাচন অনুষ্ঠানে কমিশন সম্পূর্ণ প্রস্তুত রয়েছে...',
                'content': 'নির্বাচন কমিশনের এক জরুরি প্রেস ব্রিফিংয়ে প্রধান নির্বাচন কমিশনার জানিয়েছেন, ভোটার তালিকা হালনাগাদ ও প্রয়োজনীয় লজিস্টিকস প্রস্তুতি দ্রুত এগিয়ে চলছে। কোনো মহল থেকে আসা গুজব ও অনিশ্চয়তায় কান না দেওয়ার আহ্বান জানান তিনি।',
                'category': cat_objs['politics'],
                'author': author_objs['শাকিল আহমেদ'],
                'image_url': '/images/cec-briefing.jpg',
                'views': 11300,
                'tags': ['নির্বাচন', 'সিইসি', 'রাজনীতি'],
                'published_at': now - timedelta(hours=4)
            },
            {
                'title': 'ডলারের দাম স্থিতিশীল, বাজারে স্বস্তি',
                'slug': 'dollar-price-stable-relief-in-market',
                'excerpt': 'খোলাবাজারে মার্কিন ডলারের বিনিময় হার গত কয়েক সপ্তাহের তুলনায় কিছুটা স্থিতিশীল থাকায় আমদানিকারকদের মাঝে স্বস্তি ফিরে এসেছে...',
                'content': 'বাংলাদেশ ব্যাংকের কড়াকড়ি নজরদারি এবং রেমিট্যান্স প্রবাহ বাড়ার কারণে কার্ব মার্কেটে ডলারের বিনিময় মূল্য স্থিতিশীল হয়ে এসেছে। অর্থনীতিবিদরা মনে করছেন, নীতিগত সহায়তা অব্যাহত থাকলে মূল্যস্ফীতিও ক্রমান্বয়ে নিয়ন্ত্রণে আসবে।',
                'category': cat_objs['economy'],
                'author': author_objs['তানভীর আহমেদ'],
                'image_url': '/images/dollar-market.jpg',
                'views': 7650,
                'tags': ['ডলার', 'অর্থনীতি', 'মুদ্রাবাজার', 'রেমিট্যান্স'],
                'published_at': now - timedelta(hours=5)
            },
            {
                'title': 'বাংলাদেশের দুর্দান্ত জয়, সিরিজে সমতা',
                'slug': 'bangladesh-magnificent-victory-series-levelled',
                'excerpt': 'শেষ ওভারের রোমাঞ্চে বাংলাদেশ দল ৩ উইকেটে ম্যাচ জিতে সিরিজে সমতা ফিরিয়েছে। পুরো দেশ জয়ে উদ্বেলিত...',
                'content': 'মিরপুর শেরেবাংলা জাতীয় ক্রিকেট স্টেডিয়ামে অনুষ্ঠিত রোমাঞ্চকর ম্যাচে বাংলাদেশ জাতীয় ক্রিকেট দল জয়লাভ করেছে। শেষ ওভারে প্রয়োজন ছিল ১০ রান, যেখানে চার ও ছক্কায় ম্যাচ নিজেদের করে নেয় টাইগাররা। স্টেডিয়ামজুড়ে লাখো দর্শকের গগনবিদারী উল্লাস দেখা যায়।',
                'category': cat_objs['sports'],
                'author': author_objs['মাহমুদুল হাসান'],
                'image_url': '/images/cricket-win.jpg',
                'views': 15200,
                'is_popular': True,
                'popular_rank': 1,
                'tags': ['ক্রিকেট', 'টাইগার্স', 'খেলাধুলা', 'মিরপুর'],
                'published_at': now - timedelta(hours=5, minutes=30)
            },
            {
                'title': 'কৃত্রিম বুদ্ধিমত্তা ব্যবহারে বাংলাদেশের নতুন দিগন্ত',
                'slug': 'new-horizon-in-ai-adoption-in-bangladesh',
                'excerpt': 'শিক্ষা ও স্বাস্থ্যখাতে এআই ভিত্তিক সমাধান বাস্তবায়নে সরকারি ও বেসরকারি অংশীদারিত্বের এক নতুন রূপরেখা উন্মোচন করা হয়েছে...',
                'content': 'তথ্য ও যোগাযোগ প্রযুক্তি বিভাগের উদ্যোগে স্থানীয় সফটওয়্যার শিল্প ও বিশ্ববিদ্যালয়গুলোর যৌথ সহায়তায় তৈরি হচ্ছে জাতীয় এআই কৌশল। এর মাধ্যমে বাংলা প্রাকৃতিক ভাষা প্রক্রিয়াকরণ (NLP) এবং নাগরিক সেবার অটোমেশনে বিপ্লব ঘটবে বলে আশা করা হচ্ছে।',
                'category': cat_objs['technology'],
                'author': author_objs['ডেস্ক রিপোর্ট'],
                'image_url': '/images/ai-bangladesh.jpg',
                'views': 6430,
                'tags': ['এআই', 'প্রযুক্তি', 'তথ্যপ্রযুক্তি', 'উদ্ভাবন'],
                'published_at': now - timedelta(hours=6)
            },
            {
                'title': 'আন্তর্জাতিক চলচ্চিত্র উৎসবে বাংলাদেশের সিনেমা পুরস্কৃত',
                'slug': 'bangladeshi-film-wins-award-at-international-festival',
                'excerpt': 'প্রতিভাবান বাংলাদেশি নির্মাতার চলচ্চিত্র আন্তর্জাতিক মঞ্চে অর্জন করেছে সেরা মৌলিক চলচ্চিত্রের সম্মাননা...',
                'content': 'আন্তর্জাতিক চলচ্চিত্র উৎসবে বিশ্বের বাঘা বাঘা চলচ্চিত্রকে পেছনে ফেলে জুরি অ্যাওয়ার্ড জয় করেছে বাংলাদেশের স্বাধীন ধারার একটি সামাজিক চলচ্চিত্র। নির্মাতা ও কলাকুশলীদের এই অনন্য অর্জনে সংস্কৃতি অঙ্গনে বইছে আনন্দের জোয়ার।',
                'category': cat_objs['entertainment'],
                'author': author_objs['মেহজাবিন চৌধুরী'],
                'image_url': '/images/faria.jpg',
                'views': 8920,
                'is_popular': True,
                'popular_rank': 2,
                'tags': ['সিনেমা', 'বিনোদন', 'পুরস্কার', 'চলচ্চিত্র উৎসব'],
                'published_at': now - timedelta(hours=7)
            },
            {
                'title': 'যুক্তরাষ্ট্রে নতুন নীতিমালায় অভিবাসীদের নজর',
                'slug': 'immigrants-eye-new-us-policy-updates',
                'excerpt': 'ক্যাপিটল হিলে সদ্য উত্থাপিত ইমিগ্রেশন ও ভিসা বিল নিয়ে বিশ্বজুড়ে প্রবাসীদের মধ্যে আগ্রহ ও মিশ্র প্রতিক্রিয়া দেখা দিয়েছে...',
                'content': 'ওয়াশিংটন ডিসির ক্যাপিটল হিল থেকে প্রকাশিত এক প্রতিবেদনে জানা গেছে, দক্ষ কর্মীদের ওয়ার্ক ভিসা সহজীকরণে নতুন আইনি প্রস্তাবনা পেশ করা হয়েছে। এতে বাংলাদেশি পেশাজীবীদের জন্য সুযোগ বাড়বে বলে ধারণা বিশেষজ্ঞদের।',
                'category': cat_objs['international'],
                'author': author_objs['ডেস্ক রিপোর্ট'],
                'image_url': '/images/us-capitol.jpg',
                'views': 9510,
                'tags': ['যুক্তরাষ্ট্র', 'আন্তর্জাতিক', 'ভিসা', 'অভিবাসন'],
                'published_at': now - timedelta(hours=8)
            },
            {
                'title': 'কেন্দ্রীয় ব্যাংকের রিজার্ভ বৃদ্ধিতে গতি',
                'slug': 'growth-momentum-in-central-bank-reserves',
                'excerpt': 'প্রবাসী আয় বৃদ্ধি ও রপ্তানি আয় ইতিবাচক হওয়ায় বৈদেশিক মুদ্রার রিজার্ভে ইতিবাচক ধারা লক্ষ করা গেছে...',
                'content': 'বাংলাদেশ ব্যাংকের হালনাগাদ তথ্যানুযায়ী, চলতি মাসে রেমিট্যান্স ইনফ্লো বিগত বছরের একই সময়ের চেয়ে ১৮ শতাংশ বেশি এসেছে। ফলে নিট রিজার্ভ স্থিতিশীল অবস্থানে বজায় রয়েছে।',
                'category': cat_objs['economy'],
                'author': author_objs['তানভীর আহমেদ'],
                'image_url': '/images/forex-reserve.jpg',
                'views': 6120,
                'tags': ['রিজার্ভ', 'বাংলাদেশ ব্যাংক', 'অর্থনীতি', 'রেমিট্যান্স'],
                'published_at': now - timedelta(hours=9)
            },
            {
                'title': 'ত্বকের সুস্থতায় প্রাকৃতিক পরিচর্যার সহজ উপায়',
                'slug': 'easy-natural-skincare-routine-for-healthy-skin',
                'excerpt': 'ঋতু পরিবর্তনের এই সময়ে প্রাকৃতিক উপাদানের মাধ্যমে ত্বকের আর্দ্রতা ও স্বাভাবিক দীপ্তি বজায় রাখার জরুরি পরামর্শ...',
                'content': 'বিশেষজ্ঞ চর্মরোগ চিকিৎসকরা বলছেন, অতিরিক্ত রাসায়নিক পণ্যের বদলে প্রাকৃতিক উপাদান ও পর্যাপ্ত জলপানই ত্বকের স্বাস্থ্য সুরক্ষার মূল চাবিকাঠি। প্রতিদিনের সহজ রুটিন মেনে চললে ত্বক থাকবে উজ্জ্বল ও প্রাণবন্ত।',
                'category': cat_objs['lifestyle'],
                'author': author_objs['মেহজাবিন চৌধুরী'],
                'image_url': '/images/skincare.jpg',
                'views': 5230,
                'tags': ['স্কিনকেয়ার', 'জীবনযাপন', 'স্বাস্থ্য', 'সৌন্দর্য'],
                'published_at': now - timedelta(hours=10)
            },
            {
                'title': 'স্মার্টফোনে সাইবার সুরক্ষা নিশ্চিত করার আধুনিক নির্দেশিকা',
                'slug': 'modern-guide-to-ensuring-smartphone-cybersecurity',
                'excerpt': 'মোবাইল ব্যাংকিং ও ব্যক্তিগত তথ্যের নিরাপত্তায় পাসওয়ার্ড ও দ্বি-স্তরীয় প্রমাণীকরণের গুরুত্ব অপরিসীম...',
                'content': 'তথ্যপ্রযুক্তি বিশেষজ্ঞদের পরামর্শ অনুযায়ী, অপরিচিত লিংকে ক্লিক না করা এবং অ্যাপ অনুমোদনে সতর্ক থাকলে ফিশিং ও হ্যাকিংয়ের ঝুঁকি ৯০ শতাংশ হ্রাস পায়।',
                'category': cat_objs['technology'],
                'author': author_objs['শাকিল আহমেদ'],
                'image_url': '/images/mobile-security.jpg',
                'views': 4870,
                'tags': ['সাইবার নিরাপত্তা', 'স্মার্টফোন', 'তথ্যপ্রযুক্তি'],
                'published_at': now - timedelta(hours=11)
            },
            {
                'title': 'সাভারে জাতীয় স্মৃতিসৌধে শ্রদ্ধা নিবেদন',
                'slug': 'paying-homage-at-national-martyrs-memorial-savar',
                'excerpt': 'মহান শহীদদের স্মরণে জাতীয় স্মৃতিসৌধে বীর সন্তানদের প্রতি শ্রদ্ধা নিবেদন করেন সর্বস্তরের সাধারণ মানুষ...',
                'content': 'ভোরের আলো ফোটার সঙ্গে সঙ্গেই সাভারের জাতীয় স্মৃতিসৌধ প্রাঙ্গণে জড়ো হন হাজারো মানুষ। পুষ্পস্তবকে ঢেকে যায় স্মৃতিসৌধের বেদি। শহীদদের আত্মত্যাগের শপথ নিয়ে দেশ গড়ার অঙ্গীকার ব্যক্ত করেন তরুণ সমাজ।',
                'category': cat_objs['national'],
                'author': author_objs['মাহমুদুল হাসান'],
                'image_url': '/images/national-memorial.jpg',
                'views': 13800,
                'is_popular': True,
                'popular_rank': 3,
                'tags': ['জাতীয় স্মৃতিসৌধ', 'সাভার', 'জাতীয়', 'মুক্তিযুদ্ধ'],
                'published_at': now - timedelta(hours=12)
            }
        ]

        article_objs = []
        for a in articles_data:
            obj, _ = Article.objects.update_or_create(
                slug=a['slug'],
                defaults=a
            )
            article_objs.append(obj)

        self.stdout.write(self.style.SUCCESS(f'✓ {len(article_objs)} News Articles seeded with Ultra-HD images!'))

        # 5. Comments
        hero_art = article_objs[0]
        Comment.objects.get_or_create(
            article=hero_art,
            author_name='তানভীর আহমেদ',
            defaults={
                'author_email': 'tanvir@gmail.com',
                'content': 'অসাধারণ প্রতিবেদন! তরুণ সমাজের ঐক্যই আমাদের নতুন দেশকে এগিয়ে নিয়ে যাবে।',
                'likes': 14,
                'status': 'Approved'
            }
        )
        Comment.objects.get_or_create(
            article=hero_art,
            author_name='সাদিয়া তাসনিম',
            defaults={
                'author_email': 'sadia@gmail.com',
                'content': 'নতুন প্রজন্মের আত্মত্যাগ যেন বৃথা না যায়। ধন্যবাদ হ্যালো দেশকে এই সুন্দর প্রতিবেদনের জন্য।',
                'likes': 9,
                'status': 'Approved'
            }
        )

        cricket_art = article_objs[6]
        Comment.objects.get_or_create(
            article=cricket_art,
            author_name='রাকিবুল হাসান',
            defaults={
                'author_email': 'rakib@gmail.com',
                'content': 'কী দুর্দান্ত জয়! শেষ ওভারে বাউন্ডারি দেখে চোখে পানি চলে এসেছিল। সাবাশ বাংলাদেশ!',
                'likes': 22,
                'status': 'Approved'
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Reader comments seeded!'))

        # 6. Subscribers
        subs = [
            'mridul@hellodesh.com',
            'reader1@gmail.com',
            'student.union@du.ac.bd',
            'business.lead@dhaka.com'
        ]
        for s in subs:
            Subscriber.objects.get_or_create(email=s, defaults={'status': 'Active'})
        self.stdout.write(self.style.SUCCESS('✓ Subscribers seeded!'))

        # 7. Notifications
        Notification.objects.get_or_create(
            title='নতুন প্রতিবেদন প্রকাশিত হয়েছে',
            defaults={
                'description': 'প্রধান উপদেষ্টার ভাষণ সংক্রান্ত জাতীয় সংবাদ সফলভাবে প্রকাশিত হয়েছে।',
                'notification_type': 'success',
                'read': False
            }
        )
        Notification.objects.get_or_create(
            title='নতুন পাঠক মন্তব্য',
            defaults={
                'description': 'তানভীর আহমেদ প্রধান খবরের নিচে একটি নতুন মন্তব্য করেছেন।',
                'notification_type': 'info',
                'read': False
            }
        )
        Notification.objects.get_or_create(
            title='সার্ভার ব্যাকআপ সম্পন্ন',
            defaults={
                'description': 'প্রতিদিনের ডেটাবেস স্ন্যাপশট ও ব্যাকআপ স্বয়ংক্রিয়ভাবে সম্পন্ন হয়েছে।',
                'notification_type': 'info',
                'read': True
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Admin notifications seeded!'))

        # 8. Media Library Files
        media_list = [
            ('hero-yunus.jpg', '/images/hero-yunus.jpg', '715 KB', '1920x1080'),
            ('students-rally.jpg', '/images/students-rally.jpg', '1.1 MB', '1920x1080'),
            ('padma-bridge.jpg', '/images/padma-bridge.jpg', '944 KB', '1920x1080'),
            ('national-memorial.jpg', '/images/national-memorial.jpg', '932 KB', '1920x1080'),
            ('metro-rail.jpg', '/images/metro-rail.jpg', '962 KB', '1920x1080'),
            ('cec-briefing.jpg', '/images/cec-briefing.jpg', '803 KB', '1920x1080'),
            ('cricket-win.jpg', '/images/cricket-win.jpg', '926 KB', '1920x1080'),
            ('dollar-market.jpg', '/images/dollar-market.jpg', '828 KB', '1920x1080'),
            ('ai-bangladesh.jpg', '/images/ai-bangladesh.jpg', '835 KB', '1920x1080'),
            ('faria.jpg', '/images/faria.jpg', '831 KB', '1920x1080'),
            ('forex-reserve.jpg', '/images/forex-reserve.jpg', '975 KB', '1920x1080'),
            ('us-capitol.jpg', '/images/us-capitol.jpg', '822 KB', '1920x1080'),
            ('skincare.jpg', '/images/skincare.jpg', '740 KB', '1920x1080'),
            ('mobile-security.jpg', '/images/mobile-security.jpg', '132 KB', '1920x1080'),
        ]
        for name, url, size, dims in media_list:
            MediaFile.objects.get_or_create(
                name=name,
                defaults={
                    'file_url': url,
                    'file_type': 'image',
                    'size': size,
                    'dimensions': dims,
                    'uploaded_by': admin_user
                }
            )
        self.stdout.write(self.style.SUCCESS('✓ Media library assets seeded!'))

        # 9. Activity Log
        ActivityLog.objects.get_or_create(
            title='সংবাদ প্রকাশ: দেশের উন্নয়নে তরুণদের ভূমিকা',
            defaults={
                'user': admin_user,
                'activity_type': 'publish',
                'detail': 'প্রধান উপদেষ্টা বিষয়ক বিশেষ প্রতিবেদন মূল ব্যানারে প্রকাশিত হয়েছে।',
                'ip_address': '127.0.0.1'
            }
        )
        ActivityLog.objects.get_or_create(
            title='নতুন মন্তব্য অনুমোদন',
            defaults={
                'user': editor_user,
                'activity_type': 'comment',
                'detail': 'তানভীর আহমেদের মন্তব্য সফলভাবে অনুমোদিত হয়েছে।',
                'ip_address': '127.0.0.1'
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Activity logs seeded!'))

        # 10. Site Settings
        SiteSetting.get_settings()
        self.stdout.write(self.style.SUCCESS('✓ Site settings initialized!'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Hello Desh Database Seeding Completed Successfully!'))
