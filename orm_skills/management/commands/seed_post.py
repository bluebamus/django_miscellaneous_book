from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from orm_skills.models import Blog, Category, Post
import random
import pytz


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤함 테스트 유저 데이터를 만듭니다"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=10,
            type=int,
            help="몇 명의 유저 데이터를 만드나.",
        )

    def handle(self, *args, **options):
        total = options.get("total")
        category = Category.objects.all()
        seeder = Seed.seeder()
        fake = Faker(["ko_KR"])
        seeder.add_entity(
            Post,
            total,
            {
                "category": lambda x: random.choice(category),
                "writer": lambda x: fake.name(),
                "address": lambda x: fake.address(),
                "ip_address": lambda x: fake.ipv4_private(),
                "title": lambda x: fake.sentence(),
                "content": lambda x: fake.text(),
                "created_at": lambda x: fake.date_time(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total} posts created!"))
