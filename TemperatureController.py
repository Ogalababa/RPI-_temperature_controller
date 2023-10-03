# Optimized TemperatureController.py
import os.path
import time
from RTC import RTC
from datetime import datetime
import pytz
import logging
from pathlib import Path


class TemperatureController:

    def __init__(self, target_temp=30, temp_range=5, timezone='Europe/Amsterdam'):

        self.rtc = RTC()
        self.target_temp_day = target_temp
        self.target_temp_night = target_temp - 3
        self.temp_range = temp_range
        self.timezone = pytz.timezone(timezone)
        self.datetime = datetime
        self.pytz = pytz

        # Logging setup
        current_dir = Path(__file__).parent
        logging.basicConfig(filename=os.path.join(current_dir, 'temperature_controller.log'),
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger()

    def update_equipment_status(self, equipment, desired_status):
        current_status = self.rtc.status[equipment]
        if current_status != desired_status:
            self.rtc.controller(equipment, desired_status)

    def control_temperature(self):
        counter = 0
        while True:
            self.rtc.get_room_temp()
            self.rtc.get_control_temp()
            current_temp = self.rtc.temp
            print(current_temp)
            current_hour = self.datetime.now(self.timezone).hour

            if 10 <= current_hour < 24:
                # check 陶瓷灯 status:
                self.update_equipment_status('陶瓷灯', self.rtc.OFF)

                if current_temp < self.target_temp_day - self.temp_range:  # It's too cold
                    self.update_equipment_status('日光灯', self.rtc.ON)
                    self.update_equipment_status('加温风扇', self.rtc.ON)
                    self.update_equipment_status('降温风扇', self.rtc.OFF)

                elif self.target_temp_day - 3 <= current_temp <= self.target_temp_day + 3:  # It's good temp
                    self.update_equipment_status('日光灯', self.rtc.OFF)
                    self.update_equipment_status('加温风扇', self.rtc.OFF)
                    self.update_equipment_status('降温风扇', self.rtc.OFF)

                elif current_temp > self.target_temp_day + self.temp_range:  # It's too hot
                    self.update_equipment_status('日光灯', self.rtc.OFF)
                    self.update_equipment_status('加温风扇', self.rtc.OFF)
                    self.update_equipment_status('降温风扇', self.rtc.ON)

            else:
                self.update_equipment_status('日光灯', self.rtc.OFF)

                if current_temp < self.target_temp_night - self.temp_range:  # It's too cold
                    self.update_equipment_status('陶瓷灯', self.rtc.ON)
                    self.update_equipment_status('加温风扇', self.rtc.ON)
                    self.update_equipment_status('降温风扇', self.rtc.OFF)

                elif self.target_temp_night - 3 <= current_temp <= self.target_temp_night + 3:  # It's good temp
                    self.update_equipment_status('陶瓷灯', self.rtc.OFF)
                    self.update_equipment_status('加温风扇', self.rtc.OFF)
                    self.update_equipment_status('降温风扇', self.rtc.OFF)

                elif current_temp > self.target_temp_night + self.temp_range:  # It's too hot
                    self.update_equipment_status('陶瓷灯', self.rtc.OFF)
                    self.update_equipment_status('加温风扇', self.rtc.OFF)
                    self.update_equipment_status('降温风扇', self.rtc.ON)
            self.rtc.save_to_json()
            counter += 1
            if counter == 30:
                self.logger.info(
                    f"Time：{datetime.now(self.timezone)}, Temperature: {current_temp}, Status: {self.rtc.status}")
                counter = 0
            time.sleep(60)  # Adjust this value as per your requirement


if __name__ == '__main__':
    temp_controller = TemperatureController(target_temp=30, temp_range=5, timezone='Europe/Amsterdam')
    temp_controller.control_temperature()
