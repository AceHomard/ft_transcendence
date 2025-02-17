import time

class Cooldown:
    def __init__(self, times, num):
        self.setCooldown(times, num)

    def getCooldown(self, interval, num, future_num):
        current_time = int(time.time() * 1000)
        if self._num == num and self._times + interval <= current_time:
            self.setCooldown(current_time, future_num)
            return 1
        return 0

    def setCooldown(self, times, num):
        self._times = times
        self._num = num
