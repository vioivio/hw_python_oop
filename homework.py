from dataclasses import dataclass, asdict
from typing import Sequence, Dict, Tuple, List, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float,
                    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return (distance)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance()/self.duration
        return (mean_speed)

    def get_spent_calories(self) -> float:
        raise NotImplementedError("Определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        duration_min = self.duration * self.MIN_IN_H
        return((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * duration_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 heiht: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = heiht

    def get_spent_calories(self) -> float:
        duration_min = self.duration * self.MIN_IN_H
        height_m = self.height / self.SM_IN_M
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
             + (self.get_mean_speed() ** 2  / height_m)
             * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
             * duration_min
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_MEAN_SPEED: float = 1.1
    COEFF_WEIGHT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_MEAN_SPEED)
                * self.COEFF_WEIGHT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    training = training_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 2, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
