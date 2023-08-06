import datetime
import logging
import typing


class DatePick:
    """Pick date by conditions and re-like wildcards"""

    def __init__(self, lookup: int = 365) -> None:
        """
        Initialize DatePick instance

        Params
        ------

        :param lookup: days to look up when searching for appropriate date
        """
        self._lookup = lookup

    def _parse_wildcard(self, wildcard: str) -> typing.Dict[str, int]:
        """
        Return dict with datetime-like fields given wildcard

        Params
        ------

        :param wildcard: wildcard to parse
        :return: a dict with datetime-like fields
        """
        date, time = wildcard.split(" ")
        year, month, day, weekday = date.split("-")
        hour, minute, second = time.split(":")
        return {
            "year": None if year == "*" else int(year),
            "month": None if month == "*" else int(month),
            "day": None if day == "*" else int(day),
            "weekday": None if weekday == "*" else int(weekday),
            "hour": None if hour == "*" else int(hour),
            "minute": None if minute == "*" else int(minute),
            "second": None if second == "*" else int(second),
        }

    def pick(self, wildcards: typing.List[str]) -> str:
        """
        Pick nearest date to datetime.datetime.now() given re-like wildcard conditions

        Params
        ------

        :param wildcards: list of re-like wildcards representing conditions
        """

        out = []

        for wildcard in wildcards:
            conditions = self._parse_wildcard(wildcard)

            hour = conditions.pop("hour")
            minute = conditions.pop("minute")
            second = conditions.pop("second")

            today = datetime.datetime.now()
            date1 = datetime.datetime(
                today.year,
                today.month,
                today.day,
                hour,
                minute,
                second,
            )

            if date1 < datetime.datetime.now():
                date1 += datetime.timedelta(days=1)

            date2 = date1 + datetime.timedelta(days=self._lookup)

            dates = [
                date1 + datetime.timedelta(days=x)
                for x in range((date2 - date1).days + 1)
            ]

            for key, value in conditions.items():
                if value is not None:
                    if key == "weekday":
                        dates = list(
                            filter(lambda x: getattr(x, key)() == value, dates)
                        )
                    else:
                        dates = list(filter(lambda x: getattr(x, key) == value, dates))

            try:
                out.append(dates[0])
            except IndexError:
                logging.warning(f"No dates matching conditions in wildcard {wildcard}.")

        try:
            return datetime.datetime.strftime(min(out), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.warning(
                f"No dates matching any of the given wildcards: {','.join(wildcards)}. Returning None."
            )
            return "None"
