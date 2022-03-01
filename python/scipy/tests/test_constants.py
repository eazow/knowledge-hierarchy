from scipy import constants


def test_pi():
    assert constants.pi == 3.141592653589793
    assert constants.pound == 0.45359236999999997


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
