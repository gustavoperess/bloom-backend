from datetime import date

from lib.models.extended_help_offer import ExtendedHelpOffer
from lib.repositories.extended_help_offer_repository import ExtendedHelpOfferRepository


# def test_get_all_received_extended_help_offers(db_connection):
#     db_connection.seed("seeds/bloom.sql")
#     extended_help_repo = ExtendedHelpOfferRepository(db_connection)
#     help_offers = extended_help_repo.get_all_received_extended_help_offers(3)

#     assert help_offers == [
#         ExtendedHelpOffer(
#             8,
#             date(2023, 9, 10),
#             date(2023, 9, 15),
#             "Plant care help needed urgently.",
#             3,
#             3,
#             "I can provide immediate help with watering your plants.",
#             "pending",
#             4,
#             60.0,
#             "Barbra",
#             "Banes",
#             "barn-owl58",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
#             "Jilly",
#             "Smith",
#             "sm1thi",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
#         ),
#         ExtendedHelpOffer(
#             3,
#             date(2023, 4, 15),
#             date(2023, 4, 20),
#             "Need assistance with gardening.",
#             3,
#             8,
#             "I have gardening experience and can help with your garden.",
#             "pending",
#             4,
#             90.0,
#             "Barbra",
#             "Banes",
#             "barn-owl58",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
#             "Jilly",
#             "Smith",
#             "sm1thi",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
#         ),
#         ExtendedHelpOffer(
#             8,
#             date(2023, 9, 10),
#             date(2023, 9, 15),
#             "Plant care help needed urgently.",
#             3,
#             13,
#             "I am experienced in caring for indoor plants and can help.",
#             "pending",
#             4,
#             75.0,
#             "Barbra",
#             "Banes",
#             "barn-owl58",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
#             "Jilly",
#             "Smith",
#             "sm1thi",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
#         ),
#         ExtendedHelpOffer(
#             3,
#             date(2023, 4, 15),
#             date(2023, 4, 20),
#             "Need assistance with gardening.",
#             3,
#             18,
#             "I have gardening experience and can help with your garden.",
#             "pending",
#             4,
#             90.0,
#             "Barbra",
#             "Banes",
#             "barn-owl58",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
#             "Jilly",
#             "Smith",
#             "sm1thi",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
#         ),
#     ]


# def test_get_all_received_extended_help_offers(db_connection):
#     db_connection.seed("seeds/bloom.sql")
#     extended_help_repo = ExtendedHelpOfferRepository(db_connection)
#     help_offers = extended_help_repo.get_all_outgoing_extended_help_offers(1)

#     assert help_offers == [
#         ExtendedHelpOffer(
#             10,
#             date(2023, 11, 22),
#             date(2023, 11, 27),
#             "Garden watering assistance required.",
#             5,
#             5,
#             "I can assist you with watering your garden.",
#             "pending",
#             1,
#             65.0,
#             "Tom",
#             "Jones",
#             "tee-jay",
#             "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
#             "Alice",
#             "Lane",
#             "laney",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
#         ),
#         ExtendedHelpOffer(
#             5,
#             date(2023, 6, 12),
#             date(2023, 6, 18),
#             "Assistance needed with garden maintenance.",
#             5,
#             10,
#             "I can take care of your plants while you are on holiday.",
#             "pending",
#             1,
#             70.0,
#             "Tom",
#             "Jones",
#             "tee-jay",
#             "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
#             "Alice",
#             "Lane",
#             "laney",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
#         ),
#         ExtendedHelpOffer(
#             10,
#             date(2023, 11, 22),
#             date(2023, 11, 27),
#             "Garden watering assistance required.",
#             5,
#             15,
#             "I am available to help with your garden maintenance.",
#             "pending",
#             1,
#             80.0,
#             "Tom",
#             "Jones",
#             "tee-jay",
#             "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
#             "Alice",
#             "Lane",
#             "laney",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
#         ),
#         ExtendedHelpOffer(
#             5,
#             date(2023, 6, 12),
#             date(2023, 6, 18),
#             "Assistance needed with garden maintenance.",
#             5,
#             20,
#             "I am available to assist with your gardening needs.",
#             "pending",
#             1,
#             85.0,
#             "Tom",
#             "Jones",
#             "tee-jay",
#             "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
#             "Alice",
#             "Lane",
#             "laney",
#             "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
#         ),
#     ]
