import logging
from banks import meta
from banks import banks, networkmanager, calc
import asyncio

logging.basicConfig(level=logging.INFO)


class Monitor(metaclass=meta.SingletonMeta):

    last_sended_message_id = 0
    current_status = False

    def __init__(self, i_bank, i_calc, i_network_manager):
        self.tks = i_bank
        self.calc = i_calc
        self.network_manager = i_network_manager

    async def __update_rates(self):
        try:
            for item in self.tks.urls.items():
                key_buy = item[0] + "_BUY"
                key_sell = item[0] + "_SELL"
                data = await self.network_manager.fetch_tinkoff_data(item)
                self.tks.currencies_rates[key_buy] = data['payload']['rates'][0]['buy']
                self.tks.currencies_rates[key_sell] = data['payload']['rates'][0]['sell']
        except Exception as error:
            logging.info(error)

    async def __check_left(self, left_h: float, central_h: float, right_h: float) -> [float]:
        l_left_hand_rate = self.tks.currencies_rates[left_h]
        l_central_hand_rate = self.tks.currencies_rates[central_h]
        l_right_hand_rate = self.tks.currencies_rates[right_h]

        calc_left = await self.calc.calc_left_right(l_left_hand_rate, l_central_hand_rate, l_right_hand_rate)
        data = [l_left_hand_rate, l_central_hand_rate, l_right_hand_rate, calc_left]
        return data

    async def __check_right(self, left_h: float, central_h: float, right_h: float) -> [float]:
        r_left_hand_rate = self.tks.currencies_rates[left_h]
        r_central_hand_rate = self.tks.currencies_rates[central_h]
        r_right_hand_rate = self.tks.currencies_rates[right_h]

        calc_right = await self.calc.calc_right_left(r_left_hand_rate, r_central_hand_rate, r_right_hand_rate)
        data = [r_left_hand_rate, r_central_hand_rate, r_right_hand_rate, calc_right]
        return data

    async def check_data(self):
        await self.__update_rates()

        for chain in self.tks.chains.items():
            left_right_array = await self.__check_left(chain[1][0], chain[1][1], chain[1][2])
            right_left_array = await self.__check_right(chain[1][3], chain[1][4], chain[1][5])

            if not self.current_status:
                if left_right_array[3] > 0 or right_left_array[3] > 0:
                    await self.send_new_message(chain[0], left_right_array, right_left_array)
            else:
                if left_right_array[3] > 0 or right_left_array[3] > 0:
                    await self.send_update_message()

    async def send_new_message(self, chain, left_rate_array, right_rate_array):
        alert = "...\n"
        if left_rate_array[3] > 1 or right_rate_array[3] > 1:
            alert = "🔥\n"

        left_rates_data = "left rates: " + str(left_rate_array[0]) + " :: " + str(left_rate_array[1]) + " :: " + str(left_rate_array[2]) + "\n"
        right_rates_data = "right rates: " + str(right_rate_array[0]) + " :: " + str(right_rate_array[1]) + " :: " + str(right_rate_array[2]) + "\n"

        message = alert + chain + "\n\n" + left_rates_data + "left " + str(left_rate_array[3]) + "\n\n" + right_rates_data + "right " + str(right_rate_array[3])
        data = await self.network_manager.send_create(message)
        logging.info(data)

    async def send_update_message(self):
        message = "updates =)"
        data = await self.network_manager.send_create(message)
        logging.info(data)

    def send_end_message(self):
        pass


monitor = Monitor(banks.Tinkoff(), calc.Calc(), networkmanager.NetworkManager())


async def main():
    await monitor.check_data()
    await asyncio.sleep(100)

while __name__ == "__main__":
    asyncio.run(main())
