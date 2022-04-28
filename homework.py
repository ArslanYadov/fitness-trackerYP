import inspect
from dataclasses import dataclass, asdict
from typing import Dict, List, Type


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
    RUNNING_MULT_COEFF_LOW: float = 18
    RUNNING_MULT_COEFF_HIGH: float = 20

    def get_spent_calories(self) -> float:
        """Получить кол-во потраченных калорий во время бега"""
        return (
            (
                self.RUNNING_MULT_COEFF_LOW * self.get_mean_speed()
                - self.RUNNING_MULT_COEFF_HIGH
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

    SPORTS_WALKING_MULT_COEFF_HIGH: float = 0.035
    SPORTS_WALKING_MULT_COEFF_LOW: float = 0.029
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
        """Получить кол-во потраченных калорий во время спортивной ходьбы"""
        return (
            (
                self.SPORTS_WALKING_MULT_COEFF_HIGH * self.weight
                + (self.get_mean_speed()**self.SQUARE // self.height)
                * self.SPORTS_WALKING_MULT_COEFF_LOW * self.weight
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
    SWIMMING_MULT_COEFF_LOW: float = 1.1
    SWIMMING_MULT_COEFF_HIGH: float = 2

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
        """Получить среднюю скоросость во время плавания"""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить кол-во потраченных калорий во время плавания"""
        return (
            (self.get_mean_speed() + self.SWIMMING_MULT_COEFF_LOW)
            * self.SWIMMING_MULT_COEFF_HIGH * self.weight
        )


def get_inspect(training: Type[Training], data: list):
    """Проверка количества аргументов"""
    training_signature: inspect.Signature = inspect.signature(training)
    training_signature_list: List[str] = list(training_signature.parameters)

    length_training_arg = len(training_signature_list)
    length_from_input = len(data)

    ARGUMENTS_INFO_FORMAT = (
        f'Allowed number of argument: {length_training_arg}; '
        f'Received number of argument: {length_from_input}; '
        f'Allowed arguments: {training_signature_list}'
    )

    if len(data) != length_training_arg:
        raise TypeError(ARGUMENTS_INFO_FORMAT)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    DICT_FROM_PARAM: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    acceptable_workout_type: str = ", ".join(DICT_FROM_PARAM)

    if workout_type not in DICT_FROM_PARAM:
        raise KeyError(
            f'Entered training type: {workout_type}, '
            f'Procceed only: {acceptable_workout_type}.'
        )
    get_inspect(DICT_FROM_PARAM[workout_type], data)
    return DICT_FROM_PARAM[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
