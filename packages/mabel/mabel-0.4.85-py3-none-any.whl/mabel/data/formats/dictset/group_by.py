from typing import Callable, Iterator
from mabel.data.formats import dictset as ds


class Groups:

    __slots__ = "_groups"

    def __init__(self, dictset: Iterator, column: str, dedupe: bool = False):
        """
        Group By functionality for Iterables of Dictionaries
        Parameters:
            dictset: Iterable of dictionaries
                The dataset to perform the Group By on
            column: string
                The name of the field to group by
            dedupe: bool
                Remove duplicate values from the groups
        Returns:
            Groups
        Warning:
            The 'Groups' object holds the entire dataset in memory so is unsuitable
            for large datasets.
        """
        groups: dict = {}
        if dedupe:
            dictset = ds.drop_duplicates(dictset)
        for item in dictset:
            my_item = item.copy()
            key = my_item.pop(column, None)
            if not key in groups:
                groups[key] = []
            groups[key].append(my_item)
        if dedupe:
            for group in groups:
                groups[group] = {
                    frozenset(item.items()): item for item in groups[group]
                }.values()
        self._groups = groups

    def count(self, group=None):
        """
        Count the number of items in groups
        Parameters:
            group: string (optional)
                If provided, return the count of just this group
        Returns:
            if a group is provided, return an integer
            if no group is provided, return a dictionary
        """
        if group is None:
            return {x: len(y) for x, y in self._groups.items()}
        else:
            try:
                return [len(y) for x, y in self._groups.items() if x == group].pop()
            except IndexError:
                return 0

    def aggregate(self, column, method):
        """
        Applies an aggregation function by group.
        Parameters:
            column: string
                The name of the field to aggregate on
            method: callable
                The function to aggregate with
        Returns:
            dictionary
        Examples:
            maxes = grouped.aggregate('age', max)
            means = grouped.aggregate('age', maths.mean)
        """
        response = {}
        for key, items in self._groups.items():
            values = [
                item.get(column) for item in items if item.get(column) is not None
            ]
            response[key] = method(values)
        return response

    def apply(self, method: Callable):
        """
        Apply a function to all groups
        Parameters:
            method: callable
                The function to apply to the groups
        Returns:
            dictionary
        """
        return {key: method(items) for key, items in self._groups.items()}

    def __len__(self):
        """
        Returns the number of groups in the set.
        """
        return len(self._groups)

    def __repr__(self):
        """
        Returns the group names
        """
        return f"Group of {len(self)} items"

    def __getitem__(self, item):
        """
        Selector access to groups, e.g. Groups["Group Name"]
        Note that Groups["Group 1", "Group 2"] creates a group with just those items
        """
        if isinstance(item, (tuple, list)):
            newg = Groups([], None)
            for entry in item:
                if entry in self._groups:
                    newg._groups[entry].append(self._groups[entry])
            return newg
        else:
            return SubGroup(self._groups.get(item))


class SubGroup:

    __slots__ = "values"

    def __init__(self, values):
        self.values = values or []

    def __getitem__(self, item):
        """
        Selector access to a value in a group, support arrays
        """
        if isinstance(item, tuple):
            return list(ds.select_from(self.values, columns=item))
        else:
            return ds.extract_column(self.values, item)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return f"SubGroup of {len(self)} items"
