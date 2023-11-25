from ninety_nine import graphical_main_game as graphics


def test_filename_from_card(ace_of_spades):
    assert graphics.get_image_filename_from_card(ace_of_spades) == "card_images/spades_ace.png"


