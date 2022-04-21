from dataclasses import dataclass
<<<<<<< HEAD
from typing import Callable, Dict
=======
>>>>>>> ea89dd8636c2c3d193265468da9911b628f8cd18


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод сообщения"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CALORIE_COEFFICIENT_1: float = 18
    CALORIE_COEFFICIENT_2: float = 20
    MIN_IN_HOUR: int = 60
<<<<<<< HEAD
    DURATION_MIN: float
=======
>>>>>>> ea89dd8636c2c3d193265468da9911b628f8cd18

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Subclasses should implement this!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
<<<<<<< HEAD
        self.DURATION_MIN: float = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIE_COEFFICIENT_1 * self.get_mean_speed()
                - self.CALORIE_COEFFICIENT_2)
                * self.weight / self.M_IN_KM
                * self.DURATION_MIN)
=======
        return ((type(self).CALORIE_COEFFICIENT_1 * self.get_mean_speed()
                - type(self).CALORIE_COEFFICIENT_2)
                * self.weight / self.M_IN_KM
                * (self.duration * type(self).MIN_IN_HOUR))
>>>>>>> ea89dd8636c2c3d193265468da9911b628f8cd18


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_COEFFICIENT_1: float = 0.035
    CALORIE_COEFFICIENT_2: float = 0.029
    SQUARE: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
<<<<<<< HEAD
        self.DURATION_MIN: float = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIE_COEFFICIENT_1 * self.weight
                + (self.get_mean_speed()**self.SQUARE // self.height)
                * self.CALORIE_COEFFICIENT_2 * self.weight)
                * self.DURATION_MIN)
=======
        return ((self.CALORIE_COEFFICIENT_1 * self.weight
                + (self.get_mean_speed()**self.SQUARE // self.height)
                * self.CALORIE_COEFFICIENT_2 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))
>>>>>>> ea89dd8636c2c3d193265468da9911b628f8cd18


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
<<<<<<< HEAD
    CALORIE_COEFFICIENT_1: float = 1.1
    CALORIE_COEFFICIENT_2: float = 2
=======
>>>>>>> ea89dd8636c2c3d193265468da9911b628f8cd18

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIE_COEFFICIENT_1)
                * self.CALORIE_COEFFICIENT_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
<<<<<<< HEAD
    dict_from_param: Dict[str, Callable[..., Training]] = {
=======
    dict_from_param = {
>>>>>>> ea89dd8636c2c3d193265468da9911b628f8cd18
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict_from_param.keys():
        return dict_from_param[workout_type](*data)
    return Training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
