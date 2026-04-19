from collections import deque
import statistics

class SensorProcessor:
    def __init__(self, window_size=5):
        self.temps = deque(maxlen=window_size)

    def process(self, data):
        temp = data["temperature"]
        self.temps.append(temp)

        result = {
            "current": temp,
            "moving_avg": None,
            "z_score": None,
            "status": "NORMAL"
        }

        if len(self.temps) >= 2:
            avg = sum(self.temps) / len(self.temps)
            std = statistics.stdev(self.temps)

            result["moving_avg"] = round(avg, 2)

            if std != 0:
                z = (temp - avg) / std
                result["z_score"] = round(z, 2)

                if abs(z) > 2:
                    result["status"] = "ANOMALY"

        if temp > 100:
            result["status"] = "CRITICAL"

        return result