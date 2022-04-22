from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    FORMAT_TEXT_MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Вывод сообщения"""
        return self.FORMAT_TEXT_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    action: float
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def duration_min(self) -> float:
        """Получить длительность в минутах"""
        return self.duration * self.MIN_IN_HOUR

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
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    RUNNING_MULT_COEFF_1: float = 18
    RUNNING_MULT_COEFF_2: float = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.RUNNING_MULT_COEFF_1 * self.get_mean_speed()
                - self.RUNNING_MULT_COEFF_2
            )
            * self.weight / self.M_IN_KM
            * self.duration_min()
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: float
    duration: float
    weight: float
    height: float
    SPORTS_WALKING_MULT_COEFF_1: float = 0.035
    SPORTS_WALKING_MULT_COEFF_2: float = 0.029
    SQUARE: float = 2

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.SPORTS_WALKING_MULT_COEFF_1 * self.weight
                + (self.get_mean_speed()**self.SQUARE // self.height)
                * self.SPORTS_WALKING_MULT_COEFF_2 * self.weight
            )
            * self.duration_min()
        )


class Swimming(Training):
    """Тренировка: плавание."""
    action: float
    duration: float
    weight: float
    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38
    SWIMMING_MULT_COEFF_1: float = 1.1
    SWIMMING_MULT_COEFF_2: float = 2

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIMMING_MULT_COEFF_1)
            * self.SWIMMING_MULT_COEFF_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_from_param: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in dict_from_param:
        try:
            return Training(*data)
        except TypeError:
            print(f'Type error in {Training.__name__}')
    try:
        return dict_from_param[workout_type](*data)
    except KeyError:
        print(f'Invalid training type: {workout_type}')
    except TypeError:
        print(f'Type error in {dict_from_param[workout_type].__name__}')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        print('Error in reading package')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
