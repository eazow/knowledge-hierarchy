from scipy import constants


def test_pi():
    assert constants.pi == 3.141592653589793
    assert constants.pound == 0.45359236999999997
    assert constants.speed_of_sound == 340.5
    assert constants.speed_of_light == 299792458
    assert constants.horsepower == 745.6998715822701


def test_dir():
    assert (
        set(
            [
                "pi",
                "speed_of_light",
                "speed_of_sound",
            ]
        )
        < set(dir(constants))
    )
