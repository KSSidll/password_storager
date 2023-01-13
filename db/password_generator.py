import math
import string
from random import choices
from random import random


class PasswordGenerator:
    @staticmethod
    def generate(length=13, letters=True, digits=True, special_characters=True,
                 min_entropy=60.0, max_tries=100000) -> str | None:
        """
        Generates and returns a random string with minimum entropy as benchmark of randomness, returns None if no
        satisfactory string is generated within max_tries tries
        :param length: int, Length of the string, default 13
        :param letters: bool, Whether to include letters in generation, default True
        :param digits: bool, Whether to include digits in generation, default True
        :param special_characters: bool, Whether to include special characters in generation, default True
        :param min_entropy: float, Minimal entrophy of generated password, if higher than max possible entropy,
        first generated string is returned, default 60.0
        :param max_tries: int, Max tries before None is returned if no satisfactory string is generated , default 100000
        :return: Random string or None if no satisfactory string is generated within max_tries tries
        """
        available_characters = ""
        if letters:
            available_characters += string.ascii_letters
        if digits:
            available_characters += string.digits
        if special_characters:
            available_characters += string.punctuation

        max_entropy = PasswordGenerator.calculate_max_entropy(length, available_characters)

        # generate first string
        weights = [random() for _ in range(len(available_characters))]
        result = ''.join(choices(available_characters, weights=weights, k=length))
        tried = 1

        # repeat generation until satisfactory entropy is reached
        if max_entropy >= min_entropy:
            while PasswordGenerator.calculate_entropy(result) < min_entropy:
                weights = [random() for _ in range(len(available_characters))]
                result = ''.join(choices(available_characters, weights=weights, k=length))
                tried += 1
                if tried == max_tries:
                    return None

        return result

    @staticmethod
    def calculate_entropy(password) -> float:
        letters = False
        digits = False
        punctuation = False

        for char in password:
            if char in string.ascii_letters:
                letters = True
            if char in string.digits:
                digits = True
            if char in string.punctuation:
                punctuation = True

        # E = L * log2(R)
        # E - entropy
        # L - string length
        # R - character pool

        length = len(password)
        pool = 0
        if letters:
            pool += len(string.ascii_letters)
        if digits:
            pool += len(str(string.digits))
        if punctuation:
            pool += len(str(string.punctuation))

        entropy = length * math.log2(pool)

        return entropy

    @staticmethod
    def calculate_max_entropy(length, character_pool):
        return length * math.log2(len(character_pool))
