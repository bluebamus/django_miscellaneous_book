from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from orm_skills.models import Blog, Category, Post
import random


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
        seeder = Seed.seeder()
        fake = Faker(["ko_KR"])
        blog = Blog.objects.all()
        seeder.add_entity(
            Category,
            total,
            {
                "blog": lambda x: random.choice(blog),
                "name": lambda x: fake.word(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total} categorys created!"))
