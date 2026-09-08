import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from apps.departments.models import Department
from apps.news.models import NewsCategory, NewsItem
from apps.schemes.models import Scheme
from apps.events.models import Event
from apps.resources.models import Resource
from apps.ads.models import AdSlot
from apps.announcements.models import Announcement
from apps.market.models import MarketPrice
from apps.weather.models import WeatherCity
from apps.faqs.models import FAQ
from apps.testimonials.models import Testimonial
from apps.about.models import AboutContent, AboutHighlight
from apps.epaper.models import EPaperIssue
from apps.sitesettings.models import SiteSettings
from apps.pages.models import StaticPage

SEED_MEDIA = Path(settings.BASE_DIR) / "seed_media"


def _file(*parts):
    return File(open(SEED_MEDIA.joinpath(*parts), "rb"))


class Command(BaseCommand):
    help = "Populates the database with the real Krishi Manthan content (matches the original frontend) so the site is never blank after setup."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Krishi Manthan data...")

        self.seed_site_settings()
        self.seed_departments()
        categories = self.seed_categories()
        self.seed_news(categories)
        self.seed_schemes()
        self.seed_events()
        self.seed_resources()
        self.seed_ad_slots()
        self.seed_announcements()
        self.seed_market_prices()
        self.seed_weather()
        self.seed_faqs()
        self.seed_testimonials()
        self.seed_about()
        self.seed_epaper()
        self.seed_static_pages()

        self.stdout.write(self.style.SUCCESS("Seeding complete."))

    # ------------------------------------------------------------------
    def seed_site_settings(self):
        s = SiteSettings.load()
        if not s.site_name or s.site_name == "Krishi Manthan":
            s.tagline_hi = "कृषि एवं ग्रामीण विकास से जुड़ी महत्वपूर्ण जानकारी का मंच"
            s.tagline_en = "A trusted source for agriculture and rural development updates"
            s.address_hi = "कृषि मंथन कार्यालय, कृषि भवन, नई दिल्ली - 110001"
            s.address_en = "Krishi Manthan Office, Krishi Bhawan, New Delhi - 110001"
            s.email = "info@krishimanthan.in"
            s.phone = "+91 11-2338-XXXX"
            s.default_meta_title = "कृषि मंथन | Agriculture News, Schemes & Farmer Updates"
            s.default_meta_description = "कृषि मंथन पर कृषि समाचार, सरकारी योजनाएं, मंडी भाव, कृषि तकनीक, ग्रामीण विकास, कार्यक्रम और ई-पेपर की विश्वसनीय जानकारी पाएं।"
            s.default_meta_keywords = "कृषि समाचार, किसान योजना, सरकारी कृषि योजनाएं, मंडी भाव, कृषि तकनीक, ग्रामीण विकास"
            if not s.logo:
                s.logo.save("logo.png", _file("logo.png"), save=False)
            if not s.og_image:
                s.og_image.save("og-image.jpg", _file("og-image.jpg"), save=False)
            s.save()
        self.stdout.write("  site settings OK")

    def seed_departments(self):
        data = [
            ("कृषि", "Agriculture", "agriculture", "Wheat", "bg-green-100 text-green-700"),
            ("सहकारिता", "Cooperation", "cooperation", "Building2", "bg-amber-100 text-amber-700"),
            ("पंचायत", "Panchayat", "panchayat", "CircleDot", "bg-blue-100 text-blue-700"),
            ("वन", "Forest", "forest", "TreePine", "bg-emerald-100 text-emerald-700"),
            ("पशुपालन", "Animal Husbandry", "animal-husbandry", "PawPrint", "bg-orange-100 text-orange-700"),
        ]
        for i, (hi, en, slug, icon, tone) in enumerate(data):
            Department.objects.get_or_create(slug=slug, defaults={
                "name_hi": hi, "name_en": en, "icon": icon, "color_tone": tone, "order": i,
            })
        self.stdout.write(f"  departments: {Department.objects.count()}")

    def seed_categories(self):
        data = [
            ("कृषि", "Agriculture", "agriculture"),
            ("सहकारिता", "Cooperation", "cooperation"),
            ("बैंकिंग", "Banking", "banking"),
            ("समसामयिकी", "Current Affairs", "current-affairs"),
            ("कृषि तकनीक", "Technology in Farming", "technology-in-farming"),
            ("मंडी भाव", "Market Prices", "market-prices"),
        ]
        cats = {}
        for i, (hi, en, slug) in enumerate(data):
            cat, _ = NewsCategory.objects.get_or_create(slug=slug, defaults={"name_hi": hi, "name_en": en, "order": i})
            cats[en] = cat
        self.stdout.write(f"  news categories: {NewsCategory.objects.count()}")
        return cats

    def seed_news(self, categories):
        if NewsItem.objects.exists():
            self.stdout.write("  news: already seeded, skipping")
            return
        items = [
            dict(title_hi="खरीफ सीजन 2026 के लिए MSP में 5% की बढ़ोतरी", title_en="MSP increased by 5% for Kharif Season 2026",
                 summary_hi="केंद्र सरकार ने खरीफ फसलों के न्यूनतम समर्थन मूल्य में वृद्धि की घोषणा की है।",
                 summary_en="The central government has announced an increase in minimum support prices for kharif crops.",
                 category="Agriculture", date="2026-03-28", author="राजेश शर्मा", img="images/news/news-1-msp-kharif.jpg"),
            dict(title_hi="किसान क्रेडिट कार्ड की ब्याज दर में कमी", title_en="Interest rate reduced on Kisan Credit Card",
                 summary_hi="सरकार ने KCC पर ब्याज दर 4% से घटाकर 3% करने का निर्णय लिया।",
                 summary_en="Government decides to reduce KCC interest rate from 4% to 3%.",
                 category="Banking", date="2026-03-25", author="प्रीति वर्मा", img="images/news/news-2-kcc-banking.jpg"),
            dict(title_hi="जैविक खेती को बढ़ावा देने के लिए नई योजना शुरू", title_en="New scheme launched to promote organic farming",
                 summary_hi="कृषि मंत्रालय ने जैविक खेती को प्रोत्साहित करने हेतु ₹500 करोड़ की योजना शुरू की।",
                 summary_en="Ministry of Agriculture launches ₹500 crore scheme to encourage organic farming.",
                 category="Agriculture", date="2026-03-22", author="अमित पटेल", img="images/news/news-3-organic-farming.jpg"),
            dict(title_hi="NABARD ने ग्रामीण बुनियादी ढांचे के लिए ₹1000 करोड़ मंजूर किए", title_en="NABARD approves ₹1000 crore for rural infrastructure",
                 summary_hi="राष्ट्रीय कृषि और ग्रामीण विकास बैंक ने ग्रामीण सड़कों और सिंचाई के लिए फंड जारी किया।",
                 summary_en="NABARD releases funds for rural roads and irrigation infrastructure.",
                 category="Cooperation", date="2026-03-20", author="सुनील कुमार", img="images/news/news-4-nabard-rural.jpg"),
            dict(title_hi="ड्रोन तकनीक से कीटनाशक छिड़काव में क्रांति", title_en="Drone technology revolutionizes pesticide spraying",
                 summary_hi="आधुनिक ड्रोन तकनीक के उपयोग से किसानों की कीटनाशक लागत में 40% की कमी आई।",
                 summary_en="Modern drone technology reduces farmers' pesticide costs by 40%.",
                 category="Technology in Farming", date="2026-03-18", author="विकास गुप्ता", img="images/news/news-5-drone-farming.jpg"),
            dict(title_hi="गेहूं की रिकॉर्ड पैदावार की उम्मीद", title_en="Record wheat production expected this year",
                 summary_hi="कृषि विभाग के अनुसार इस वर्ष गेहूं उत्पादन 115 मिलियन टन तक पहुंच सकता है।",
                 summary_en="According to agriculture department, wheat production may reach 115 million tonnes.",
                 category="Agriculture", date="2026-03-15", author="नीलम सिंह", img="images/news/news-6-wheat-record.jpg"),
            dict(title_hi="मंडी भाव: टमाटर के दाम में तेज गिरावट", title_en="Market prices: Sharp decline in tomato prices",
                 summary_hi="प्रमुख मंडियों में टमाटर का भाव ₹40 प्रति किलो से घटकर ₹15 पर आया।",
                 summary_en="Tomato prices drop from ₹40/kg to ₹15/kg in major markets.",
                 category="Market Prices", date="2026-03-12", author="राहुल यादव", img="images/news/news-7-tomato-mandi.jpg"),
            dict(title_hi="लोकसभा में कृषि सुधार बिल पास", title_en="Agriculture reform bill passed in Lok Sabha",
                 summary_hi="संसद ने नए कृषि सुधार विधेयक को बहुमत से पारित किया।",
                 summary_en="Parliament passes new agriculture reform bill with majority.",
                 category="Current Affairs", date="2026-03-10", author="अनुराग मिश्रा", img="images/news/news-8-agri-bill.jpg"),
        ]
        from django.utils.text import slugify
        for it in items:
            n = NewsItem(
                title_hi=it["title_hi"], title_en=it["title_en"],
                summary_hi=it["summary_hi"], summary_en=it["summary_en"],
                content_hi=it["summary_hi"], content_en=it["summary_en"],
                category=categories.get(it["category"]),
                author=it["author"], published_date=it["date"],
                slug=slugify(it["title_en"])[:200],
                meta_title=it["title_en"], meta_description=it["summary_en"],
            )
            n.image.save(Path(it["img"]).name, _file(it["img"]), save=False)
            n.save()
        self.stdout.write(f"  news items: {NewsItem.objects.count()}")

    def seed_schemes(self):
        if Scheme.objects.exists():
            self.stdout.write("  schemes: already seeded, skipping")
            return
        from django.utils.text import slugify
        items = [
            dict(name_hi="प्रधानमंत्री फसल बीमा योजना", name_en="PM Fasal Bima Yojana",
                 overview_hi="फसल नुकसान की स्थिति में किसानों को बीमा कवर प्रदान करती है।", overview_en="Provides insurance coverage to farmers in case of crop loss.",
                 benefits_hi="प्राकृतिक आपदा, कीट रोग से फसल नुकसान पर बीमा राशि।", benefits_en="Insurance amount for crop loss due to natural disasters and pest diseases.",
                 eligibility_hi="सभी किसान जो अधिसूचित क्षेत्र में अधिसूचित फसल उगाते हैं।", eligibility_en="All farmers growing notified crops in notified areas.",
                 process_hi="नजदीकी बैंक या CSC केंद्र पर आवेदन करें।", process_en="Apply at nearest bank or CSC center.",
                 img="images/schemes/scheme-1-pm-fasal-bima.jpg", apply_url="https://pmfby.gov.in/"),
            dict(name_hi="किसान क्रेडिट कार्ड", name_en="Kisan Credit Card",
                 overview_hi="किसानों को कम ब्याज दर पर ऋण उपलब्ध कराता है।", overview_en="Provides loans to farmers at low interest rates.",
                 benefits_hi="3% ब्याज दर, ₹3 लाख तक का ऋण, फसल बीमा।", benefits_en="3% interest rate, loan up to ₹3 lakh, crop insurance.",
                 eligibility_hi="सभी किसान, शेयरक्रॉपर, किरायेदार किसान।", eligibility_en="All farmers, sharecroppers, tenant farmers.",
                 process_hi="किसी भी राष्ट्रीयकृत बैंक में आवेदन करें।", process_en="Apply at any nationalized bank.",
                 img="images/schemes/scheme-2-kcc.jpg", apply_url=""),
            dict(name_hi="मृदा स्वास्थ्य कार्ड योजना", name_en="Soil Health Card Scheme",
                 overview_hi="किसानों की मिट्टी की जांच कर स्वास्थ्य कार्ड प्रदान करती है।", overview_en="Provides health cards after testing farmers' soil.",
                 benefits_hi="मिट्टी की गुणवत्ता की जानकारी, उर्वरक सिफारिश।", benefits_en="Soil quality information, fertilizer recommendations.",
                 eligibility_hi="भारत के सभी किसान।", eligibility_en="All farmers in India.",
                 process_hi="कृषि विभाग या KVK से संपर्क करें।", process_en="Contact agriculture department or KVK.",
                 img="images/schemes/scheme-3-soil-health.jpg", apply_url="https://soilhealth.dac.gov.in/"),
            dict(name_hi="प्रधानमंत्री कृषि सिंचाई योजना", name_en="PM Krishi Sinchai Yojana",
                 overview_hi="हर खेत को पानी पहुंचाने का लक्ष्य।", overview_en="Aims to provide water to every field.",
                 benefits_hi="सूक्ष्म सिंचाई पर 55% सब्सिडी, जल संरक्षण।", benefits_en="55% subsidy on micro irrigation, water conservation.",
                 eligibility_hi="सभी श्रेणी के किसान।", eligibility_en="All categories of farmers.",
                 process_hi="राज्य कृषि विभाग के माध्यम से आवेदन।", process_en="Apply through state agriculture department.",
                 img="images/schemes/scheme-4-pm-sinchai.jpg", apply_url="https://pmksy.gov.in/"),
            dict(name_hi="पीएम किसान सम्मान निधि", name_en="PM Kisan Samman Nidhi",
                 overview_hi="किसानों को प्रतिवर्ष ₹6000 की सहायता राशि।", overview_en="Annual assistance of ₹6000 to farmers.",
                 benefits_hi="₹2000 की 3 किस्तें सीधे बैंक खाते में।", benefits_en="3 installments of ₹2000 directly to bank account.",
                 eligibility_hi="2 हेक्टेयर तक भूमि वाले सभी किसान परिवार।", eligibility_en="All farmer families with up to 2 hectares of land.",
                 process_hi="पीएम किसान पोर्टल पर ऑनलाइन आवेदन।", process_en="Apply online on PM Kisan portal.",
                 img="images/schemes/scheme-5-pm-kisan.jpg", apply_url="https://pmkisan.gov.in/"),
        ]
        for i, it in enumerate(items):
            s = Scheme(
                name_hi=it["name_hi"], name_en=it["name_en"],
                overview_hi=it["overview_hi"], overview_en=it["overview_en"],
                benefits_hi=it["benefits_hi"], benefits_en=it["benefits_en"],
                eligibility_hi=it["eligibility_hi"], eligibility_en=it["eligibility_en"],
                process_hi=it["process_hi"], process_en=it["process_en"],
                apply_url=it["apply_url"], order=i,
                slug=slugify(it["name_en"])[:200],
                meta_title=it["name_en"], meta_description=it["overview_en"],
            )
            s.image.save(Path(it["img"]).name, _file(it["img"]), save=False)
            s.save()
        self.stdout.write(f"  schemes: {Scheme.objects.count()}")

    def seed_events(self):
        if Event.objects.exists():
            self.stdout.write("  events: already seeded, skipping")
            return
        from django.utils.text import slugify
        items = [
            dict(title_hi="राष्ट्रीय कृषि प्रशिक्षण कार्यशाला", title_en="National Agriculture Training Workshop", date="2026-10-15",
                 location_hi="IARI, नई दिल्ली", location_en="IARI, New Delhi", organizer_hi="कृषि मंत्रालय", organizer_en="Ministry of Agriculture",
                 desc_hi="आधुनिक खेती तकनीकों पर तीन दिवसीय प्रशिक्षण कार्यक्रम।", desc_en="Three-day training program on modern farming techniques.",
                 img="images/events/event-1-training-workshop.jpg"),
            dict(title_hi="किसान मेला 2026", title_en="Kisan Mela 2026", date="2026-11-10",
                 location_hi="कृषि विश्वविद्यालय, लुधियाना", location_en="Agriculture University, Ludhiana", organizer_hi="पंजाब कृषि विश्वविद्यालय", organizer_en="Punjab Agricultural University",
                 desc_hi="कृषि उपकरण प्रदर्शनी और बीज वितरण कार्यक्रम।", desc_en="Agriculture equipment exhibition and seed distribution program.",
                 img="images/events/event-2-kisan-mela.jpg"),
            dict(title_hi="जैविक खेती सेमिनार", title_en="Organic Farming Seminar", date="2026-10-25",
                 location_hi="KVK, भोपाल", location_en="KVK, Bhopal", organizer_hi="ICAR", organizer_en="ICAR",
                 desc_hi="जैविक प्रमाणीकरण और विपणन पर विशेषज्ञ सेमिनार।", desc_en="Expert seminar on organic certification and marketing.",
                 img="images/events/event-3-organic-seminar.jpg"),
            dict(title_hi="ड्रोन कृषि प्रदर्शन", title_en="Drone Agriculture Demonstration", date="2026-12-05",
                 location_hi="MANAGE, हैदराबाद", location_en="MANAGE, Hyderabad", organizer_hi="NABARD", organizer_en="NABARD",
                 desc_hi="ड्रोन आधारित कृषि तकनीक का लाइव प्रदर्शन।", desc_en="Live demonstration of drone-based agriculture technology.",
                 img="images/events/event-4-drone-demo.jpg"),
            dict(title_hi="रबी फसल समीक्षा बैठक", title_en="Rabi Crop Review Meeting", date="2026-08-20",
                 location_hi="कृषि भवन, नई दिल्ली", location_en="Krishi Bhawan, New Delhi", organizer_hi="कृषि विभाग", organizer_en="Department of Agriculture",
                 desc_hi="रबी सीजन की फसल समीक्षा और आगामी योजनाओं पर चर्चा।", desc_en="Rabi season crop review and discussion on upcoming plans.",
                 img="images/events/event-5-rabi-meeting.jpg"),
            dict(title_hi="कृषि विज्ञान कांग्रेस", title_en="Agriculture Science Congress", date="2026-07-15",
                 location_hi="BHU, वाराणसी", location_en="BHU, Varanasi", organizer_hi="कृषि अनुसंधान परिषद", organizer_en="Agriculture Research Council",
                 desc_hi="कृषि विज्ञान में नवीनतम अनुसंधान पर राष्ट्रीय सम्मेलन।", desc_en="National conference on latest research in agriculture science.",
                 img="images/events/event-6-science-congress.jpg"),
        ]
        for it in items:
            e = Event(
                title_hi=it["title_hi"], title_en=it["title_en"], event_date=it["date"],
                location_hi=it["location_hi"], location_en=it["location_en"],
                organizer_hi=it["organizer_hi"], organizer_en=it["organizer_en"],
                desc_hi=it["desc_hi"], desc_en=it["desc_en"],
                slug=slugify(it["title_en"])[:200],
                meta_title=it["title_en"], meta_description=it["desc_en"],
            )
            e.image.save(Path(it["img"]).name, _file(it["img"]), save=False)
            e.save()
        self.stdout.write(f"  events: {Event.objects.count()}")

    def seed_resources(self):
        if Resource.objects.exists():
            self.stdout.write("  resources: already seeded, skipping")
            return
        items = [
            ("फसल कैलेंडर", "Crop Calendar", "मौसम अनुसार फसल बुवाई का कैलेंडर।", "Season-wise crop sowing calendar."),
            ("जैविक खेती गाइड", "Organic Farming Guide", "जैविक खेती की संपूर्ण जानकारी।", "Complete guide to organic farming."),
            ("मृदा परीक्षण मैनुअल", "Soil Testing Manual", "मिट्टी की जांच कैसे करें, विस्तृत मार्गदर्शिका।", "Detailed guide on how to test soil."),
            ("कृषि उपकरण उपयोग गाइड", "Farm Equipment Usage Guide", "आधुनिक कृषि उपकरणों का सही उपयोग।", "Proper usage of modern farm equipment."),
            ("प्रशिक्षण पुस्तिकाएं", "Training Booklets", "किसानों के लिए विभिन्न प्रशिक्षण सामग्री।", "Various training materials for farmers."),
        ]
        for i, (hi, en, dhi, den) in enumerate(items):
            r = Resource(name_hi=hi, name_en=en, desc_hi=dhi, desc_en=den, order=i)
            r.file.save("krishi-manthan-epaper.pdf", _file("krishi-manthan-epaper.pdf"), save=False)
            r.save()
        self.stdout.write(f"  resources: {Resource.objects.count()}")

    def seed_ad_slots(self):
        slots = [
            ("sidebar_top", "Sidebar — Top"),
            ("sidebar_bottom", "Sidebar — Bottom"),
            ("footer_banner", "Footer Banner"),
            ("news_inline", "News Listing — Inline"),
            ("home_banner", "Home Page — Banner"),
        ]
        for key, name in slots:
            AdSlot.objects.get_or_create(key=key, defaults={"name": name})
        self.stdout.write(f"  ad slots: {AdSlot.objects.count()}")

    def seed_announcements(self):
        if Announcement.objects.exists():
            self.stdout.write("  announcements: already seeded, skipping")
            return
        items = [
            ("कृषि एवं ग्रामीण विकास से जुड़ी महत्वपूर्ण जानकारी का मंच", "A trusted source for agriculture and rural development updates", True, False),
            ("PM किसान की 17वीं किस्त अप्रैल 2026 में जारी होगी", "PM Kisan 17th installment to be released in April 2026", True, True),
            ("खरीफ सीजन 2026 के लिए MSP में 5% की बढ़ोतरी", "MSP increased by 5% for Kharif Season 2026", True, False),
            ("किसान मेला 2026 के लिए पंजीकरण शुरू", "Registrations open for Kisan Mela 2026", True, False),
        ]
        for i, (hi, en, ticker, sidebar) in enumerate(items):
            Announcement.objects.create(text_hi=hi, text_en=en, show_in_ticker=ticker, show_in_sidebar=sidebar, order=i)
        self.stdout.write(f"  announcements: {Announcement.objects.count()}")

    def seed_market_prices(self):
        if MarketPrice.objects.exists():
            self.stdout.write("  market prices: already seeded, skipping")
            return
        items = [
            ("गेहूं", "Wheat", 2275, "up"),
            ("चावल", "Rice", 3100, "down"),
            ("सरसों", "Mustard", 5200, "up"),
            ("चना", "Gram", 5500, "flat"),
            ("सोयाबीन", "Soybean", 4800, "up"),
        ]
        for i, (hi, en, price, trend) in enumerate(items):
            MarketPrice.objects.create(crop_name_hi=hi, crop_name_en=en, price=price, trend=trend, order=i)
        self.stdout.write(f"  market prices: {MarketPrice.objects.count()}")

    def seed_weather(self):
        if not WeatherCity.objects.exists():
            WeatherCity.objects.create(
                city_name_hi="नई दिल्ली", city_name_en="New Delhi",
                latitude=28.6139, longitude=77.2090, is_default=True,
                manual_temp_c=32.0, manual_condition_hi="आंशिक बादल", manual_condition_en="Partly Cloudy",
                manual_humidity=45, manual_wind_kmh=12.0,
            )
        self.stdout.write("  weather city OK")

    def seed_faqs(self):
        if FAQ.objects.exists():
            self.stdout.write("  faqs: already seeded, skipping")
            return
        items = [
            ("PM किसान सम्मान निधि के लिए आवेदन कैसे करें?", "How do I apply for PM Kisan Samman Nidhi?",
             "आप pmkisan.gov.in पोर्टल पर जाकर ऑनलाइन आवेदन कर सकते हैं, या नजदीकी CSC केंद्र पर संपर्क करें।",
             "You can apply online at pmkisan.gov.in, or visit your nearest CSC center."),
            ("किसान क्रेडिट कार्ड बनवाने के लिए कौन से दस्तावेज़ चाहिए?", "What documents are needed for a Kisan Credit Card?",
             "पहचान प्रमाण, पता प्रमाण, भूमि दस्तावेज़ और पासपोर्ट साइज फोटो की आवश्यकता होती है।",
             "You need identity proof, address proof, land documents and a passport-size photo."),
            ("फसल बीमा का दावा कैसे करें?", "How do I file a crop insurance claim?",
             "फसल नुकसान की सूचना 72 घंटे के भीतर संबंधित बैंक या बीमा कंपनी को दें।",
             "Report crop loss to your bank or insurance company within 72 hours."),
        ]
        for i, (qhi, qen, ahi, aen) in enumerate(items):
            FAQ.objects.create(question_hi=qhi, question_en=qen, answer_hi=ahi, answer_en=aen, order=i)
        self.stdout.write(f"  faqs: {FAQ.objects.count()}")

    def seed_testimonials(self):
        if Testimonial.objects.exists():
            self.stdout.write("  testimonials: already seeded, skipping")
            return
        items = [
            ("रामलाल यादव", "किसान, उत्तर प्रदेश", "Farmer, Uttar Pradesh",
             "कृषि मंथन से मुझे सरकारी योजनाओं की सही जानकारी समय पर मिल जाती है।",
             "Krishi Manthan gives me timely, accurate information about government schemes."),
            ("सुनीता देवी", "किसान, हरियाणा", "Farmer, Haryana",
             "मंडी भाव की जानकारी से मुझे अपनी फसल बेचने में बहुत मदद मिली।",
             "Market price information here has really helped me sell my crops better."),
        ]
        for i, (name, rhi, ren, qhi, qen) in enumerate(items):
            Testimonial.objects.create(name=name, role_hi=rhi, role_en=ren, quote_hi=qhi, quote_en=qen, order=i)
        self.stdout.write(f"  testimonials: {Testimonial.objects.count()}")

    def seed_about(self):
        about = AboutContent.load()
        if not about.intro_hi:
            about.intro_hi = "कृषि मंथन एक डिजिटल मंच है जो भारतीय कृषि, सहकारिता, बैंकिंग और ग्रामीण विकास से जुड़ी विश्वसनीय और समय पर जानकारी प्रदान करता है। हमारा उद्देश्य किसानों, कृषि पेशेवरों, शोधकर्ताओं और नीति निर्माताओं को एक ही मंच पर सभी आवश्यक जानकारी उपलब्ध कराना है।"
            about.intro_en = "Krishi Manthan is a digital platform that provides reliable and timely information related to Indian agriculture, cooperation, banking and rural development. Our aim is to provide all essential information to farmers, agriculture professionals, researchers and policymakers on a single platform."
            about.save()
        if not AboutHighlight.objects.exists():
            highlights = [
                ("हमारा मिशन", "Our Mission", "कृषि क्षेत्र की सटीक और विश्वसनीय जानकारी हर किसान और कृषि हितधारक तक पहुंचाना।", "To deliver accurate and reliable agriculture information to every farmer and stakeholder.", "Target"),
                ("हमारे दर्शक", "Our Audience", "किसान, कृषि वैज्ञानिक, सहकारी संस्थाएं, बैंकिंग पेशेवर, छात्र और नीति निर्माता।", "Farmers, agricultural scientists, cooperative societies, banking professionals, students and policymakers.", "Users"),
                ("हमारा उद्देश्य", "Our Purpose", "कृषि नीतियों, योजनाओं, बाजार भावों और तकनीकी नवाचारों की जानकारी एक ही स्थान पर।", "Information about agricultural policies, schemes, market prices and technological innovations in one place.", "BookOpen"),
            ]
            for i, (thi, ten, dhi, den, icon) in enumerate(highlights):
                AboutHighlight.objects.create(title_hi=thi, title_en=ten, desc_hi=dhi, desc_en=den, icon=icon, order=i)
        self.stdout.write("  about content OK")

    def seed_epaper(self):
        if not EPaperIssue.objects.exists():
            issue = EPaperIssue(issue_date="2026-09-03")
            issue.pdf_file.save("krishi-manthan-epaper.pdf", _file("krishi-manthan-epaper.pdf"), save=False)
            issue.thumbnail.save("krishi-manthan-epaper-thumb.jpg", _file("krishi-manthan-epaper-thumb.jpg"), save=False)
            issue.save()
        self.stdout.write(f"  e-paper issues: {EPaperIssue.objects.count()}")

    def seed_static_pages(self):
        pages = [
            (
                "privacy-policy", "गोपनीयता नीति", "Privacy Policy",
                "<p>कृषि मंथन आपकी गोपनीयता का सम्मान करता है। जब आप हमारी सेवाओं (सदस्यता, संपर्क फॉर्म, विज्ञापन अनुरोध) का उपयोग करते हैं, तो हम केवल आवश्यक जानकारी (नाम, ईमेल, मोबाइल नंबर) एकत्र करते हैं।</p>"
                "<p><strong>हम क्या एकत्र करते हैं:</strong> नाम, ईमेल पता, मोबाइल नंबर, और आपके द्वारा भेजे गए संदेश।</p>"
                "<p><strong>हम इसका उपयोग कैसे करते हैं:</strong> केवल आपको अपडेट भेजने, आपके प्रश्नों का उत्तर देने और सेवा में सुधार के लिए।</p>"
                "<p><strong>डेटा साझाकरण:</strong> हम आपकी जानकारी किसी तीसरे पक्ष को नहीं बेचते।</p>"
                "<p>किसी भी प्रश्न के लिए हमसे संपर्क करें।</p>",
                "<p>Krishi Manthan respects your privacy. When you use our services (subscription, contact form, ad requests), we only collect information necessary to provide those services (name, email, mobile number).</p>"
                "<p><strong>What we collect:</strong> Name, email address, mobile number, and any message you send us.</p>"
                "<p><strong>How we use it:</strong> Only to send you updates, respond to your queries, and improve our service.</p>"
                "<p><strong>Data sharing:</strong> We do not sell your information to any third party.</p>"
                "<p>Contact us for any questions regarding this policy.</p>",
            ),
            (
                "terms-conditions", "नियम एवं शर्तें", "Terms & Conditions",
                "<p>कृषि मंथन वेबसाइट का उपयोग करके, आप निम्नलिखित नियमों और शर्तों से सहमत होते हैं।</p>"
                "<p><strong>सामग्री का उपयोग:</strong> इस वेबसाइट की जानकारी केवल सामान्य जानकारी के उद्देश्य से है। किसी भी सरकारी योजना में आवेदन से पहले आधिकारिक स्रोतों से पुष्टि करें।</p>"
                "<p><strong>विज्ञापन:</strong> प्रस्तुत सभी विज्ञापन समीक्षा और स्वीकृति के अधीन हैं। हम किसी भी विज्ञापन को बिना कारण बताए अस्वीकार करने का अधिकार सुरक्षित रखते हैं।</p>"
                "<p><strong>दायित्व की सीमा:</strong> कृषि मंथन इस वेबसाइट पर दी गई जानकारी के उपयोग से होने वाली किसी भी हानि के लिए उत्तरदायी नहीं होगा।</p>",
                "<p>By using the Krishi Manthan website, you agree to the following terms and conditions.</p>"
                "<p><strong>Use of content:</strong> Information on this website is for general informational purposes only. Please verify with official sources before applying to any government scheme.</p>"
                "<p><strong>Advertisements:</strong> All submitted advertisements are subject to review and approval. We reserve the right to reject any advertisement without stating a reason.</p>"
                "<p><strong>Limitation of liability:</strong> Krishi Manthan will not be liable for any loss arising from the use of information provided on this website.</p>",
            ),
        ]
        for slug, thi, ten, chi, cen in pages:
            if not StaticPage.objects.filter(slug=slug).exists():
                StaticPage.objects.create(slug=slug, title_hi=thi, title_en=ten, content_hi=chi, content_en=cen)
        self.stdout.write(f"  static pages: {StaticPage.objects.count()}")
