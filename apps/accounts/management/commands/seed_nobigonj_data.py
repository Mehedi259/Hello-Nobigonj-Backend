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
from apps.settings_app.models import SiteSetting
from apps.accounts.models import ActivityLog

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial realistic database records for Hello Nobigonj News Portal and Admin Dashboard'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding Hello Nobigonj database...'))

        # 1. Users
        admin_user, _ = User.objects.get_or_create(
            email='admin@hellonobigonj.com',
            defaults={
                'username': 'admin',
                'first_name': 'Mehedi',
                'last_name': 'Hasan',
                'role': 'superadmin',
                'status': 'active',
                'is_staff': True,
                'is_superuser': True,
                'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
                'bio': 'প্রধান সম্পাদক ও প্রকাশক, হ্যালো নবীগঞ্জ',
                'designation': 'প্রধান সম্পাদক',
                'phone': '+880 1711-223344'
            }
        )
        admin_user.set_password('adminpassword123')
        admin_user.save()

        editor_user, _ = User.objects.get_or_create(
            email='editor@hellonobigonj.com',
            defaults={
                'username': 'editor',
                'first_name': 'শাকিল',
                'last_name': 'আহমেদ',
                'role': 'editor',
                'status': 'active',
                'is_staff': True,
                'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80',
                'designation': 'বার্তা সম্পাদক',
                'phone': '+880 1722-334455'
            }
        )
        editor_user.set_password('editorpassword123')
        editor_user.save()

        reporter_user, _ = User.objects.get_or_create(
            email='reporter@hellonobigonj.com',
            defaults={
                'username': 'reporter',
                'first_name': 'মাহমুদুল',
                'last_name': 'হাসান',
                'role': 'reporter',
                'status': 'active',
                'is_staff': True,
                'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80',
                'designation': 'বিশেষ প্রতিনিধি (নবীগঞ্জ)',
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
            {'name': 'নবীগঞ্জ ও সিলেট', 'name_en': 'Nabiganj & Sylhet', 'slug': 'nobigonj-sylhet', 'icon_name': 'MapPin', 'color': '#059669', 'order': 3},
            {'name': 'প্রবাস', 'name_en': 'Expatriates', 'slug': 'probash', 'icon_name': 'Plane', 'color': '#0284c7', 'order': 4},
            {'name': 'অর্থনীতি', 'name_en': 'Economy', 'slug': 'economy', 'icon_name': 'TrendingUp', 'color': '#16a34a', 'order': 5},
            {'name': 'খেলাধুলা', 'name_en': 'Sports', 'slug': 'sports', 'icon_name': 'Trophy', 'color': '#ea580c', 'order': 6},
            {'name': 'বিনোদন', 'name_en': 'Entertainment', 'slug': 'entertainment', 'icon_name': 'Film', 'color': '#db2777', 'order': 7},
            {'name': 'তথ্যপ্রযুক্তি', 'name_en': 'Technology', 'slug': 'technology', 'icon_name': 'Cpu', 'color': '#4f46e5', 'order': 8},
            {'name': 'ভিডিও ও মাল্টিমিডিয়া', 'name_en': 'Multimedia', 'slug': 'multimedia', 'icon_name': 'Video', 'color': '#e11d48', 'order': 9},
            {'name': 'মতামত', 'name_en': 'Opinion', 'slug': 'opinion', 'icon_name': 'FileText', 'color': '#475569', 'order': 10},
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
            {'name': 'ডেস্ক রিপোর্ট', 'role': 'প্রধান প্রতিবেদক', 'email': 'desk@hellonobigonj.com', 'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80', 'location': 'নবীগঞ্জ'},
            {'name': 'শাকিল আহমেদ', 'role': 'বার্তা সম্পাদক', 'email': 'shakil@hellonobigonj.com', 'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80', 'location': 'সিলেট', 'user': editor_user},
            {'name': 'মাহমুদুল হাসান', 'role': 'স্টাফ রিপোর্টার', 'email': 'mahmud@hellonobigonj.com', 'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80', 'location': 'নবীগঞ্জ বাজার', 'user': reporter_user},
            {'name': 'লন্ডন প্রতিনিধি', 'role': 'ইউকে করেসপন্ডেন্ট', 'email': 'london@hellonobigonj.com', 'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80', 'location': 'লন্ডন, যুক্তরাজ্য'},
            {'name': 'মেহজাবিন চৌধুরী', 'role': 'সংস্কৃতি ও ফিচার প্রতিনিধি', 'email': 'mehzabin@hellonobigonj.com', 'avatar_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80', 'location': 'ঢাকা'},
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
                'title': 'নবীগঞ্জে ভয়াবহ বন্যায় ক্ষতিগ্রস্ত ৫০০ পরিবার: ত্রাণ ও পুনর্বাসনের জরুরি ডাক',
                'slug': 'nobigonj-flood-500-families-affected-relief-call',
                'subtitle': 'কুশিয়ারা নদীর তীরবর্তী এলাকায় প্লাবন, পাশে দাঁড়াচ্ছে স্থানীয় প্রশাসন ও প্রবাসী ফোরাম',
                'excerpt': 'নবীগঞ্জ উপজেলায় সাম্প্রতিক ভারী বর্ষণ ও উজান থেকে নেমে আসা পাহাড়ি ঢলে প্লাবিত হয়েছে নিম্নাঞ্চল। ক্ষতিগ্রস্ত ৫০০ পরিবারের মাঝে জরুরি ত্রাণ ও ওষুধ বিতরণে এগিয়ে এসেছে স্থানীয় প্রশাসন ও যুক্তরাজ্য প্রবাসী কমিটি...',
                'content': 'নবীগঞ্জ উপজেলায় সাম্প্রতিক ভারী বর্ষণ ও উজান থেকে নেমে আসা পাহাড়ি ঢলে কুশিয়ারা নদীর পানি বিপৎসীমার ওপর দিয়ে প্রবাহিত হচ্ছে। এতে উপজেলার দীঘলবাক, ইনাতগঞ্জ ও আউশকান্দি ইউনিয়নের নিম্নাঞ্চল প্লাবিত হয়ে প্রায় ৫০০ পরিবার পানিবন্দি হয়ে পড়েছে।\n\nউপজেলা নির্বাহী কর্মকর্তা ও স্থানীয় প্রশাসন অবিলম্বে ত্রাণ কার্যক্রম শুরু করেছে। শুকনো খাবার, নিরাপদ পানি এবং বিশুদ্ধকরণ ট্যাবলেট বিতরণ করা হচ্ছে। এদিকে লন্ডন ও মধ্যপ্রাচ্যে অবস্থানরত নবীগঞ্জ প্রবাসীরা তহবিল সংগ্রহ করে বন্যাকবলিত দুর্গম এলাকায় নৌকায় করে ত্রাণ পৌঁছে দিচ্ছেন।\n\nস্থানীয় বাসিন্দারা জানান, কুশিয়ারা নদীর বাঁধ টেকসইভাবে সংস্কার করা না হলে প্রতি বছরই নদীপাড়ের মানুষকে এই দুর্ভোগ পোহাতে হবে। পানি উন্নয়ন বোর্ডের পক্ষ থেকে ক্ষতিগ্রস্ত বাঁধে জরুরি ভিত্তিতে বালুর বস্তা ফেলার কাজ চলছে।',
                'category': cat_objs['nobigonj-sylhet'],
                'author': author_objs['মাহমুদুল হাসান'],
                'image_url': 'https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=1200&q=80',
                'image_caption': 'নবীগঞ্জের প্লাবিত নিম্নাঞ্চলে নৌকায় করে ত্রাণ নিয়ে যাচ্ছেন স্বেচ্ছাসেবকরা। ছবি: হ্যালো নবীগঞ্জ',
                'is_hero': True,
                'is_breaking': True,
                'is_featured': True,
                'views': 18450,
                'tags': ['নবীগঞ্জ', 'বন্যা', 'সিলেট', 'ত্রাণ', 'কুশিয়ারা নদী'],
                'published_at': now - timedelta(hours=1)
            },
            {
                'title': 'সিলেটের চা বাগানে নতুন পর্যটন কেন্দ্র উদ্বোধন: কর্মসংস্থানের নতুন দিগন্ত',
                'slug': 'sylhet-tea-garden-new-tourism-center-opened',
                'subtitle': 'লাক্কাতুড়া ও মালনীছড়া চা বাগানে পরিবেশবান্ধব ইকো-ট্যুরিজমের প্রসার',
                'excerpt': 'সবুজে ঘেরা সিলেটে পরিবেশবান্ধব পর্যটনের অংশ হিসেবে নতুন ইকো-ট্যুরিজম সেন্টারের উদ্বোধন করা হয়েছে। এতে স্থানীয় তরুণ ও চা শ্রমিকদের পরিবারের জন্য কর্মসংস্থান সৃষ্টি হচ্ছে...',
                'content': 'সিলেটের নয়নাভিরাম দুটি চা বাগান এলাকায় আজ নতুন ইকো-ট্যুরিজম ও হেরিটেজ সেন্টারের আনুষ্ঠানিক উদ্বোধন করা হয়েছে। বেসামরিক বিমান পরিবহন ও পর্যটন মন্ত্রণালয় এবং স্থানীয় অংশীজনদের যৌথ উদ্যোগে এই কেন্দ্রটি গড়ে তোলা হয়েছে।\n\nএখানে দেশি-বিদেশি পর্যটকরা চা উৎপাদনের প্রাচীন ইতিহাস, চা পাতা চয়ন এবং চা শ্রমিকদের জীবনধারার সাথে পরিচিত হতে পারবেন। উদ্যোক্তারা জানিয়েছেন, পরিবেশ রক্ষা করে এই কেন্দ্র থেকে অর্জিত আয়ের একটি বড় অংশ চা শ্রমিকদের কল্যাণে ব্যয় করা হবে।',
                'category': cat_objs['nobigonj-sylhet'],
                'author': author_objs['শাকিল আহমেদ'],
                'image_url': 'https://images.unsplash.com/photo-1588880331179-bc9b93a0cb5e?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'সিলেটের সবুজে ঘেরা চা বাগানে পর্যটকদের পদচারণা। ছবি: হ্যালো নবীগঞ্জ',
                'is_featured': True,
                'featured_order': 1,
                'views': 12340,
                'tags': ['সিলেট', 'চা বাগান', 'পর্যটন', 'ইকো-ট্যুরিজম'],
                'published_at': now - timedelta(hours=2, minutes=15)
            },
            {
                'title': 'যুক্তরাজ্য ও ইউরোপ প্রবাসী সিলেটীদের বিনিয়োগে নবীগঞ্জে আধুনিক হাসপাতাল কমপ্লেক্স',
                'slug': 'uk-sylheti-expatriate-hospital-complex-nobigonj',
                'subtitle': 'স্বাস্থ্যসেবায় যুগান্তকারী পদক্ষেপ, সুবিধাবঞ্চিতদের জন্য থাকবে বিনামূল্যে চিকিৎসার ব্যবস্থা',
                'excerpt': 'নবীগঞ্জ উপজেলার সাধারণ মানুষের দোরগোড়ায় আধুনিক ও উন্নত চিকিৎসা সেবা পৌঁছে দিতে যুক্তরাজ্য ও ইউরোপ প্রবাসী সিলেটিদের অর্থায়নে নির্মিত হচ্ছে ১০০ শয্যাবিশিষ্ট বিশেষায়িত হাসপাতাল...',
                'content': 'যুক্তরাজ্য ও ইউরোপের বিভিন্ন দেশে বসবাসরত নবীগঞ্জ ও সিলেট অঞ্চলের প্রবাসীদের অর্থায়নে নবীগঞ্জে একটি পূর্ণাঙ্গ বিশেষায়িত দাতব্য হাসপাতাল নির্মাণের কাজ শুরু হয়েছে।\n\nপ্রকল্প সংশ্লিষ্টরা জানান, আধুনিক আইসিইউ, সিসিইউ, ডায়াগনস্টিক ল্যাব এবং মা ও শিশু কল্যাণ কেন্দ্র অন্তর্ভুক্ত থাকবে এই হাসপাতালে। দরিদ্র ও সুবিধাবঞ্চিত রোগীরা এখানে নামমাত্র মূল্যে বা বিনামূল্যে বিশেষজ্ঞ চিকিৎসকের সেবা পাবেন। প্রবাসী কমিউনিটির এই উদ্যোগকে সর্বস্তরের মানুষ সাধুবাদ জানিয়েছেন।',
                'category': cat_objs['probash'],
                'author': author_objs['লন্ডন প্রতিনিধি'],
                'image_url': 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'প্রস্তাবিত ১০০ শয্যার আধুনিক হাসপাতাল কমপ্লেক্সের প্রাথমিক মডেল।',
                'is_featured': True,
                'featured_order': 2,
                'views': 10560,
                'tags': ['প্রবাস', 'যুক্তরাজ্য', 'নবীগঞ্জ', 'হাসপাতাল', 'স্বাস্থ্যসেবা'],
                'published_at': now - timedelta(hours=3, minutes=30)
            },
            {
                'title': 'কুশিয়ারা নদীর বাঁধ সংস্কারে দ্রুত পদক্ষেপ গ্রহণের নির্দেশ জেলা প্রশাসনের',
                'slug': 'kushiyara-river-embankment-repair-nobigonj',
                'subtitle': 'ভাঙন রোধে দীর্ঘমেয়াদি টেকসই প্রকল্প অনুমোদন',
                'excerpt': 'হবিগঞ্জ জেলা প্রশাসনের উচ্চপর্যায়ের দল নবীগঞ্জে কুশিয়ারা নদীর তীরবর্তী ভাঙনকবলিত এলাকা পরিদর্শন করেছে এবং টেকসই বাঁধ নির্মাণে নির্দেশনা দিয়েছে...',
                'content': 'কুশিয়ারা নদীর ভাঙন থেকে নবীগঞ্জ উপজেলার বিস্তীর্ণ ফসলি জমি, বাজার ও জনবসতি রক্ষায় দ্রুত ও টেকসই পদক্ষেপ গ্রহণের নির্দেশ দিয়েছে হবিগঞ্জ জেলা প্রশাসন।\n\nউপজেলা প্রশাসন ও পানি উন্নয়ন বোর্ডের কর্মকর্তাদের সাথে এক জরুরি পর্যালোচনা সভায় সিদ্ধান্ত হয়, বর্ষার পানি নামার সাথে সাথেই স্থায়ী জিওব্যাগ ও ব্লক ডাম্পিংয়ের কাজ পুরোদমে শুরু করা হবে। নদীভাঙনে ভিটেমাটি হারানো পরিবারগুলোর পুনর্বাসনেও প্রয়োজনীয় সহায়তা দেওয়া হবে।',
                'category': cat_objs['nobigonj-sylhet'],
                'author': author_objs['মাহমুদুল হাসান'],
                'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'কুশিয়ারা নদীর তীরে ভাঙন প্রতিরোধে প্রস্তুতি। ছবি: হ্যালো নবীগঞ্জ',
                'is_featured': True,
                'featured_order': 3,
                'views': 8920,
                'tags': ['কুশিয়ারা নদী', 'নবীগঞ্জ', 'হবিগঞ্জ', 'নদীভাঙন'],
                'published_at': now - timedelta(hours=4)
            },
            {
                'title': 'দেশের সার্বিক সংস্কার ও উন্নয়নে তরুণদের ভূমিকা অত্যন্ত গুরুত্বপূর্ণ: প্রধান উপদেষ্টা',
                'slug': 'national-development-youth-role-adviser',
                'subtitle': 'নতুন বাংলাদেশ বিনির্মাণে তারুণ্যের শক্তিই মূল চালিকাশক্তি হতে যাচ্ছে',
                'excerpt': 'দেশের উন্নয়ন ও অগ্রগতিতে তরুণদের ভূমিকা অত্যন্ত গুরুত্বপূর্ণ বলে মন্তব্য করেছেন প্রধান উপদেষ্টা। তিনি বলেন, তরুণদের মেধা ও আত্মত্যাগের মধ্য দিয়েই সমৃদ্ধ এক বাংলাদেশ গড়ে উঠবে...',
                'content': 'দেশের সার্বিক উন্নয়ন ও সংস্কার কার্যক্রমে তরুণদের সম্পৃক্ততা অপরিহার্য বলে উল্লেখ করেছেন অন্তর্বর্তীকালীন সরকারের প্রধান উপদেষ্টা।\n\nতিনি বলেন, দুর্নীতিমুক্ত ও বৈষম্যহীন সমাজ প্রতিষ্ঠায় যুবসমাজের উদ্ভাবনী চিন্তা ও নেতৃত্ব অত্যন্ত গুরুত্বপূর্ণ। রাষ্ট্রীয় কাঠামোতে জবাবদিহিতা নিশ্চিত করতে এবং কর্মসংস্থান বাড়াতে সরকার সর্বাত্মক চেষ্টা চালিয়ে যাচ্ছে। তিনি তরুণদের দেশকে ভালোবাসতে এবং দেশ গঠনে সচেষ্ট হওয়ার আহ্বান জানান।',
                'category': cat_objs['national'],
                'author': author_objs['ডেস্ক রিপোর্ট'],
                'image_url': 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'সংলাপে বক্তব্য রাখছেন প্রধান উপদেষ্টা। ছবি: পিআইডি',
                'views': 14890,
                'tags': ['জাতীয়', 'প্রধান উপদেষ্টা', 'বাংলাদেশ', 'সংস্কার'],
                'published_at': now - timedelta(hours=5)
            },
            {
                'title': 'সিলেট জেলা স্টেডিয়ামে জমকালো আয়োজনে অনূর্ধ্ব-১৯ ক্রিকেট টুর্নামেন্ট শুরু',
                'slug': 'sylhet-u19-cricket-tournament-nobigonj-victory',
                'subtitle': 'উদ্বোধনী ম্যাচে নবীগঞ্জ যুব একাদশ ৩ উইকেটে মাধবপুরকে হারাল',
                'excerpt': 'সিলেট আন্তর্জাতিক ক্রিকেট স্টেডিয়াম সংলগ্ন আউটার গ্রাউন্ডে অনূর্ধ্ব-১৯ আন্তঃউপজেলা ক্রিকেট টুর্নামেন্টের পর্দা উঠেছে। উদ্বোধনী ম্যাচে দারুণ জয় পেয়েছে নবীগঞ্জ...',
                'content': 'সিলেটে শুরু হয়েছে বিভাগীয় অনূর্ধ্ব-১৯ যুব ক্রিকেট প্রতিযোগিতা। জমকালো উদ্বোধনী অনুষ্ঠানে জাতীয় দলের সাবেক খেলোয়াড়রা উপস্থিত ছিলেন।\n\nপ্রথম ম্যাচে নবীগঞ্জ যুব একাদশ দুর্দান্ত অলরাউন্ড পারফরম্যান্সে মাধবপুর দলকে ৩ উইকেটে হারিয়েছে। নবীগঞ্জের অলরাউন্ডার ফাহিম আহমেদ ৪২ রান করার পাশাপাশি ৩টি মূল্যবান উইকেট শিকার করে ম্যাচসেরা নির্বাচিত হন।',
                'category': cat_objs['sports'],
                'author': author_objs['শাকিল আহমেদ'],
                'image_url': 'https://images.unsplash.com/photo-1531415074868-036b1c57e3ce?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'বিজয়ী নবীগঞ্জ যুব একাদশের উল্লাস। ছবি: হ্যালো নবীগঞ্জ',
                'views': 9450,
                'tags': ['খেলাধুলা', 'ক্রিকেট', 'সিলেট', 'নবীগঞ্জ'],
                'published_at': now - timedelta(hours=6)
            },
            {
                'title': 'ওমানে প্রবাসী বাংলাদেশিদের কর্মসংস্থান ও কল্যাণে নতুন কনস্যুলার হেল্পডেস্ক',
                'slug': 'oman-bangladeshi-expatriates-new-embassy-helpdesk',
                'subtitle': 'মাস্কাটে প্রবাসী কর্মীদের জন্য ২৪ ঘণ্টা জরুরি হটলাইন ও আইনি সহায়তা সেবা',
                'excerpt': 'সুলতানাত অব ওমানে বসবাসরত প্রবাসী বাংলাদেশিদের পাসপোর্ট নবায়ন, কর্মসংস্থান সহায়তা এবং আইনি পরামর্শ প্রদানে দূতাবাসের বিশেষ হেল্পডেস্ক চালু হয়েছে...',
                'content': 'ওমানে বসবাসরত প্রবাসী বাংলাদেশি ভাই-বোনদের সুবিধা নিশ্চিত করতে রাজধানী মাস্কাটস্থ বাংলাদেশ দূতাবাসে একটি আধুনিক সমন্বিত ওয়ান-স্টপ কনস্যুলার সেবা চালু হয়েছে।\n\nনতুন এই উদ্যোগের ফলে সাধারণ কর্মীরা খুব সহজেই যে কোনো জটিলতায় তাৎক্ষণিক সমাধান পাবেন। বিশেষ করে সিলেট ও নবীগঞ্জ অঞ্চলের বহু প্রবাসী এই উদ্যোগকে স্বাগত জানিয়েছেন। প্রবাসীদের রক্ত-ঘামে অর্জিত রেমিট্যান্স দেশের অর্থনীতির অন্যতম চালিকাশক্তি।',
                'category': cat_objs['probash'],
                'author': author_objs['লন্ডন প্রতিনিধি'],
                'image_url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'মাস্কাটে বাংলাদেশ দূতাবাসের বিশেষ হেল্পডেস্কের সামনে প্রবাসীরা।',
                'views': 13600,
                'tags': ['প্রবাস', 'ওমান', 'রেমিট্যান্স', 'বাংলাদেশ দূতাবাস'],
                'published_at': now - timedelta(hours=7)
            },
            {
                'title': 'নবীগঞ্জের মেধাবী তরুণদের জন্য ফ্রিল্যান্সিং ও আইটি প্রশিক্ষণ একাডেমি চালু',
                'slug': 'nobigonj-freelancing-ai-training-lab-launched',
                'subtitle': 'দক্ষ মানবসম্পদ ও স্মার্ট কর্মসংস্থান গড়ে তুলতে নতুন পদক্ষেপ',
                'excerpt': 'নবীগঞ্জের শিক্ষিত বেকার তরুণ-তরুণীদের তথ্যপ্রযুক্তিতে দক্ষ করে গড়ে তুলতে আধুনিক কম্পিউটার ল্যাব ও ফ্রিল্যান্সিং প্রশিক্ষণ কেন্দ্রের যাত্রা শুরু হয়েছে...',
                'content': 'নবীগঞ্জ পৌর এলাকায় তরুণদের আন্তর্জাতিক আউটসোর্সিং ও ফ্রিল্যান্সিং বাজারে যুক্ত করার লক্ষ্যে একটি পূর্ণাঙ্গ আইটি প্রশিক্ষণ ল্যাব উদ্বোধন করা হয়েছে।\n\nএখানে ওয়েব ডেভেলপমেন্ট, গ্রাফিক্স ডিজাইন, ডিজিটাল মার্কেটিং এবং এআই টুলসের ওপর বিনামূল্যে বিশেষ কোর্স পরিচালনা করা হবে। উদ্বোধনী অনুষ্ঠানে বক্তারা বলেন, সঠিক দিকনির্দেশনা পেলে নবীগঞ্জের তরুণরা বৈশ্বিক বাজারে নিজেদের অবস্থান সুদৃঢ় করতে পারবে।',
                'category': cat_objs['technology'],
                'author': author_objs['মেহজাবিন চৌধুরী'],
                'image_url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'আধুনিক কম্পিউটার ল্যাবে প্রশিক্ষণে অংশ নিচ্ছেন স্থানীয় তরুণরা।',
                'views': 8230,
                'tags': ['প্রযুক্তি', 'ফ্রিল্যান্সিং', 'আইটি', 'নবীগঞ্জ'],
                'published_at': now - timedelta(hours=8)
            },
            {
                'title': 'হবিগঞ্জ জেলা প্রশাসকের সম্মেলন কক্ষে সর্বদলীয় শান্তি ও সম্প্রীতি সংলাপ',
                'slug': 'habiganj-all-party-political-dialogue-dc-office',
                'subtitle': 'আইনশৃঙ্খলা রক্ষা ও সামাজিক শান্তি বজায় রাখতে রাজনৈতিক নেতৃবৃন্দের যৌথ অঙ্গীকার',
                'excerpt': 'হবিগঞ্জ জেলায় সামাজিক সম্প্রীতি রক্ষা এবং আইনশৃঙ্খলার উন্নয়নে বিভিন্ন রাজনৈতিক দলের নেতৃবৃন্দের উপস্থিতিতে মতবিনিময় সভা অনুষ্ঠিত হয়েছে...',
                'content': 'হবিগঞ্জ জেলা প্রশাসকের সম্মেলন কক্ষে আজ সর্বদলীয় মতবিনিময় সভা অনুষ্ঠিত হয়েছে। সভায় নবীগঞ্জসহ জেলার সব উপজেলার রাজনৈতিক দলের নেতৃবৃন্দ, সুশীল সমাজের প্রতিনিধি এবং সাংবাদিকরা উপস্থিত ছিলেন।\n\nসভায় বক্তারা বলেন, জনগণের মৌলিক অধিকার প্রতিষ্ঠা, শান্তি ও শৃঙ্খলা রক্ষা এবং জনকল্যাণমূলক কাজে সবাইকে কাঁধে কাঁধ মিলিয়ে কাজ করতে হবে। কোনো অপশক্তি যেন সাম্প্রদায়িক সম্প্রীতি নষ্ট করতে না পারে সে ব্যাপারে প্রশাসন সর্বোচ্চ সতর্ক রয়েছে।',
                'category': cat_objs['politics'],
                'author': author_objs['শাকিল আহমেদ'],
                'image_url': 'https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'হবিগঞ্জ জেলা প্রশাসকের সম্মেলন কক্ষে অনুষ্ঠিত সংলাপ। ছবি: হ্যালো নবীগঞ্জ',
                'views': 9890,
                'tags': ['রাজনীতি', 'হবিগঞ্জ', 'সংলাপ', 'সম্প্রীতি'],
                'published_at': now - timedelta(hours=9)
            },
            {
                'title': 'সিলেটের তামাবিল ও শেওলা স্থলবন্দরে নতুন আধুনিক শেড চালু: বাণিজ্যে নতুন গতি',
                'slug': 'tamabil-sheola-land-ports-trade-boost-sylhet',
                'subtitle': 'আমদানি-রপ্তানি কার্যক্রমে গতিশীলতা আসবে, রাজস্ব আয় বৃদ্ধির সম্ভাবনা',
                'excerpt': 'সিলেট অঞ্চলের প্রধান দুটি স্থলবন্দর তামাবিল ও শেওলায় আধুনিক ওয়্যারহাউস ও ডিজিটাল ট্র্যাকিং সিস্টেম চালু হয়েছে, যা দ্বিপাক্ষিক বাণিজ্য প্রসারে ভূমিকা রাখবে...',
                'content': 'ভারত ও বাংলাদেশের মধ্যকার সীমান্ত বাণিজ্যে গতি ফেরাতে সিলেটের তামাবিল ও বিয়ানীবাজারের শেওলা স্থলবন্দরে নতুন অবকাঠামো উদ্বোধন করা হয়েছে।\n\nস্থলবন্দর কর্তৃপক্ষের চেয়ারম্যান জানান, ডিজিটাল অটোমেশন চালুর ফলে ট্রাকজট কমবে এবং পণ্যের দ্রুত ছাড় নিশ্চিত হবে। এতে সিলেট অঞ্চলের ব্যবসায়ীদের পরিবহন খরচ ও সময় অনেকাংশেই কমে যাবে।',
                'category': cat_objs['economy'],
                'author': author_objs['ডেস্ক রিপোর্ট'],
                'image_url': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'স্থলবন্দরে বাণিজ্যিক কার্যক্রমের দৃশ্য। ছবি: হ্যালো নবীগঞ্জ',
                'views': 6740,
                'tags': ['অর্থনীতি', 'সিলেট', 'স্থলবন্দর', 'বাণিজ্য'],
                'published_at': now - timedelta(hours=10)
            },
            {
                'title': 'হাওরের জীবন ও জীবিকা: এক অনবদ্য প্রামাণ্যচিত্র',
                'slug': 'haor-life-and-struggles-documentary-nobigonj',
                'subtitle': 'হবিগঞ্জ ও নবীগঞ্জের হাওরপাড়ের সংগ্রামী মানুষের জীবনগাঁথা',
                'excerpt': 'বর্ষায় অথৈ জলরাশি আর শুকনো মৌসুমে ফসলি মাঠ—হাওরের মানুষের জীবনসংগ্রাম নিয়ে তৈরি হয়েছে বিশেষ তথ্যচিত্র...',
                'content': 'নবীগঞ্জ ও পাশ্ববর্তী হাওরাঞ্চলের মানুষের জীবন, বৈচিত্র্য এবং জলবায়ু পরিবর্তনের প্রভাব তুলে ধরে একটি চমৎকার প্রামাণ্যচিত্র প্রকাশিত হয়েছে।\n\nভিডিওটিতে দেখানো হয়েছে কীভাবে জেলেরা উত্তাল হাওরে জীবন বাজি রেখে মাছ শিকার করেন এবং কৃষকরা একমাত্র বোরো ফসলের ওপর নির্ভর করে বেঁচে থাকেন। দর্শকমহলে তথ্যচিত্রটি ব্যাপক প্রশংসা কুড়িয়েছে।',
                'category': cat_objs['multimedia'],
                'author': author_objs['মেহজাবিন চৌধুরী'],
                'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'হাওরের দিগন্ত বিস্তৃত জলরাশি ও নৌকার দৃশ্য।',
                'views': 21450,
                'tags': ['মাল্টিমিডিয়া', 'হাওর', 'নবীগঞ্জ', 'প্রামাণ্যচিত্র'],
                'published_at': now - timedelta(hours=11)
            },
            {
                'title': 'লন্ডন প্রবাসী সিলেটি কমিউনিটির শেকড়ের টানে ফিরে আসা',
                'slug': 'london-sylheti-community-success-documentary',
                'subtitle': 'ব্রিটেনে সাফল্য পেলেও নবীগঞ্জ ও সিলেটের প্রতি ভালোবাসা অটুট',
                'excerpt': 'লন্ডনের ব্রিক লেন থেকে সিলেটের নবীগঞ্জ—প্রবাসীদের সাফল্যগাঁথা এবং নিজ মাটির উন্নয়নে তাদের আত্মনিয়োগের গল্প...',
                'content': 'যুক্তরাজ্যের অর্থনীতি ও রাজনীতিতে সিলেটি কমিউনিটির অবদান এখন সর্বজনবিদিত। নতুন প্রজন্মের ব্রিটিশ-বাংলাদেশিরা এখন নিজ শেকড় অনুসন্ধানে বারবার ফিরে আসছেন সিলেটে।\n\nশিক্ষা, স্বাস্থ্য এবং অবকাঠামো উন্নয়নে তাদের নানা মানবিক উদ্যোগ নবীগঞ্জের গ্রামীণ অর্থনীতিকে আরও গতিশীল করে তুলেছে।',
                'category': cat_objs['multimedia'],
                'author': author_objs['লন্ডন প্রতিনিধি'],
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'লন্ডনে সিলেটি কমিউনিটির মিলনমেলা।',
                'views': 16780,
                'tags': ['প্রবাস', 'যুক্তরাজ্য', 'লন্ডন', 'সিলেটি কমিউনিটি'],
                'published_at': now - timedelta(hours=12)
            },
            {
                'title': 'নবীগঞ্জের পরিবেশ সংরক্ষণ ও নদী রক্ষার এখনই সময়',
                'slug': 'nobigonj-environment-conservation-kushiyara-river',
                'subtitle': 'পরিবেশবান্ধব উন্নয়ন কৌশল বাস্তবায়ন এবং অবৈধ দখল রোধ জরুরি',
                'excerpt': 'উপজেলার নদী, খাল ও প্রাকৃতিক জলাশয়গুলো রক্ষায় অবিলম্বে নাগরিক সচেতনতা ও কঠোর প্রশাসনিক পদক্ষেপ গ্রহণ করা আবশ্যক...',
                'content': 'প্রাকৃতিক সম্পদে সমৃদ্ধ নবীগঞ্জ উপজেলা আজ পরিবেশগত নানা চ্যালেঞ্জের মুখোমুখি। কুশিয়ারা নদীসহ শাখা নদী ও খালগুলোতে পলি জমা এবং অবৈধ দখলের কারণে জলপ্রবাহ ব্যাহত হচ্ছে।\n\nটেকসই পরিবেশ নিশ্চিত করতে হলে স্থানীয় জনগণ ও প্রশাসনকে একযোগে কাজ করতে হবে। বনায়ন বাড়ানো এবং প্লাস্টিক বর্জ্য নিয়ন্ত্রণ ছাড়া ভবিষ্যৎ প্রজন্মের জন্য একটি বাসযোগ্য নবীগঞ্জ নিশ্চিত করা অসম্ভব।',
                'category': cat_objs['opinion'],
                'author': author_objs['মেহজাবিন চৌধুরী'],
                'image_url': 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'প্রাকৃতিক সৌন্দর্যে ঘেরা গ্রামীণ পরিবেশ।',
                'views': 5210,
                'tags': ['মতামত', 'পরিবেশ', 'নদী রক্ষা', 'নবীগঞ্জ'],
                'published_at': now - timedelta(hours=14)
            },
            {
                'title': 'সিলেটি লোকগান ও হাছন রাজার গানের সুরে মুগ্ধ দর্শক',
                'slug': 'sylheti-folk-song-hason-raja-cultural-festival-nobigonj',
                'subtitle': 'নবীগঞ্জে দুই দিনব্যাপী লোকজ ও সাংস্কৃতিক উৎসব সমাপ্ত',
                'excerpt': 'বাউল গান, হাছন রাজার গান ও রাধারমণের গানের সুরে মুখরিত হলো নবীগঞ্জ উপজেলা অডিটোরিয়াম প্রাঙ্গণ...',
                'content': 'নবীগঞ্জে শেষ হলো বর্ণাঢ্য লোকজ সঙ্গীত উৎসব। স্থানীয় শিল্পীদের পাশাপাশি সিলেট ও ঢাকা থেকে আগত প্রথিতযশা শিল্পীরা মঞ্চে সংগীত পরিবেশন করেন।\n\nহাছন রাজা ও শাহ আব্দুল করিমের কালজয়ী গানগুলো পরিবেশনার সময় দর্শকরা গভীর আবেগ ও উল্লাসে মেতে ওঠেন। আয়োজকরা প্রতি বছর এ ধরনের সাংস্কৃতিক আয়োজন অব্যাহত রাখার প্রত্যয় ব্যক্ত করেন।',
                'category': cat_objs['entertainment'],
                'author': author_objs['মাহমুদুল হাসান'],
                'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80',
                'image_caption': 'লোকজ সঙ্গীতানুষ্ঠানে শিল্পীদের পরিবেশনা।',
                'views': 8640,
                'tags': ['বিনোদন', 'লোকগান', 'হাছন রাজা', 'সাংস্কৃতিক উৎসব'],
                'published_at': now - timedelta(hours=16)
            }
        ]

        for art in articles_data:
            tags = art.pop('tags', [])
            art_obj, _ = Article.objects.update_or_create(
                slug=art['slug'],
                defaults={
                    **art,
                    'tags': tags,
                    'status': 'Published'
                }
            )

        self.stdout.write(self.style.SUCCESS(f'✓ {len(articles_data)} Articles created with full content & images!'))

        # 5. Site Settings
        SiteSetting.objects.update_or_create(
            id=1,
            defaults={
                'site_title': 'হ্যালো নবীগঞ্জ (Hello Nobigonj)',
                'tagline': 'নবীগঞ্জ ও সিলেটের নিরপেক্ষ ও সত্যনিষ্ঠ কণ্ঠস্বর',
                'logo_url': '/images/nobigonj-logo.svg',
                'favicon_url': '/favicon.svg',
                'contact_email': 'contact@hellonobigonj.com',
                'contact_phone': '+880 1711-223344',
                'office_address': 'নবীগঞ্জ বাজার, নবীগঞ্জ, হবিগঞ্জ, সিলেট',
                'facebook_url': 'https://facebook.com/hellonobigonj',
                'youtube_url': 'https://youtube.com/hellonobigonj',
                'meta_title': 'হ্যালো নবীগঞ্জ - সত্য খবর, সবার আগে',
                'meta_description': 'নবীগঞ্জ ও সিলেট অঞ্চলের সর্বশেষ ব্রেকিং নিউজ, প্রবাস সংবাদ, রাজনীতি, অর্থনীতি ও খেলাধুলার নির্ভরযোগ্য ডিজিটাল পোর্টাল।',
                'footer_copyright': '© ২০২৬ Hello Nobigonj. সর্বস্বত্ব সংরক্ষিত। সত্যের পক্ষে, মানুষের পাশে।',
            }
        )

        # 6. Sample Activity Logs
        ActivityLog.objects.create(
            user=admin_user,
            activity_type='publish',
            title='বন্যা সংক্রান্ত লিড নিউজ প্রকাশ করা হয়েছে',
            detail='নবীগঞ্জে ভয়াবহ বন্যায় ক্ষতিগ্রস্ত ৫০০ পরিবার সংক্রান্ত লিড আর্টিকেল প্রকাশ করা হয়েছে',
            ip_address='127.0.0.1'
        )

        self.stdout.write(self.style.SUCCESS('🎉 Hello Nobigonj database seeded successfully!'))
