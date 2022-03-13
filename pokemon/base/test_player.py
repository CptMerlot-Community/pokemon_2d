from .player import Player


def test_init_player():
    p = Player()

    assert p.name == ""
    p.name = "CptMerlot"
    assert p.name == "CptMerlot"
    p.name = "Phexeye"
    assert p.name == "CptMerlot"

    p = Player(name="Phexeye")
    assert p.name == "Phexeye"
    p.name = "CptMerlot"
    assert p.name == "Phexeye"
