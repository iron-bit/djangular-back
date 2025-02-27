from django.db.models.signals import post_migrate
from django.dispatch import receiver
from api.models import Tag, Community


@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
    default_tags = [
        {"name": "social", "description": "All about social interactions."},
        {"name": "health", "description": "Health and wellness discussions."},
        {"name": "technology", "description": "All about tech."},
        {"name": "science", "description": "Scientific discussions."},
        {"name": "art", "description": "Artistic expressions and discussions."},
    ]
    for tag in default_tags:
        Tag.objects.get_or_create(name=tag["name"], defaults={"description": tag["description"]})


@receiver(post_migrate)
def create_default_communities(sender, **kwargs):
    default_communities = [
        {
            "community_picture": "https://media.licdn.com/dms/image/v2/C5612AQFjboZ3ggD-uQ/article-cover_image-shrink_423_752/article-cover_image-shrink_423_752/0/1645833122523?e=1746057600&v=beta&t=_-LzVnTSuvFEUIK5ibo3ZL5Qr_VyzJ2B-ZkaOsOnSMo",
            "name": "Tech Geeks", "is_adult": True
        }, {
            "community_picture": "https://www.euroschoolindia.com/wp-content/uploads/2023/10/advantages-of-taking-science-jpg.webp",
            "name": "Science Explorers", "is_adult": False
        }, {
            "community_picture": "https://www.billboard.com/wp-content/uploads/2024/07/Lomiiel-cr-Rafael-Javier-BOGA-PR-Agency-press-2024-billboard-1548.jpg?w=942&h=623&crop=1",
            "name": "Music Fans", "is_adult": False
        }, {
            "community_picture": "https://s.cafebazaar.ir/images/icons/co.ad.suppermario-31e4e7c4-042b-4b94-9f2b-a01f125270df_512x512.png?x-img=v1/format,type_webp,lossless_false/resize,h_256,w_256,lossless_false/optimize",
            "name": "Movie Buffs", "is_adult": True
        }, {
            "community_picture": "https://www.gamingzion.com/wp-content/uploads/t750/2022/05/Dumbest-Sports-To-Bet-On.jpg.jpg?c=1",
            "name": "Sports Enthusiasts", "is_adult": False
        },
    ]
    for community in default_communities:
        Community.objects.get_or_create(name=community["name"], community_picture=community["community_picture"],
                                        defaults={"is_adult": community["is_adult"]})
