from .meta import SingletonMeta


class Calc(metaclass=SingletonMeta):

    async def calc_left_right(self, lh: float, ch: float, rh: float) -> float:
        lh_action = 1 / lh
        ch_action = lh_action / ch
        rh_action = ch_action * rh
        return rh_action

    async def calc_right_left(self, lh: float, ch: float, rh: float) -> float:
        rh_action = 1 / lh
        ch_action = rh_action * ch
        result = rh * ch_action
        return result

