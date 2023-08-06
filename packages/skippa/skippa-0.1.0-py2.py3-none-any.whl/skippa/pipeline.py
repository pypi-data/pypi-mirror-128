"""
import numpy as np
import pandas as pd
import dill

from skippa import Skippa, columns


df = pd.DataFrame({
    'q': [2, 3, 4],
    'x': ['a', 'b', 'c'],
    'y': [1, 16, 1000],
    'z': [0.4, None, 8.7]
})
y = np.array([0, 0, 1])

pipe = (
    Skippa()
        .impute(columns(dtype_include='number'), strategy='median')
        .scale(columns(dtype_include='number'), type='standard')
        .onehot(columns(['x']))
        .rename(columns(pattern='x_*'), lambda c: c.replace('x', 'cat'))
        .select(columns(['y', 'z']) + columns(pattern='cat_*'))
        .build(verbose=True)
)

model = pipe.fit(X=df, y=y)
res = model.transform(df)

"""
from __future__ import annotations

from typing import Optional, Union, List, Callable, Type

import dill
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion, Pipeline

from skippa.transformers import (
    Transformation,
    ColumnExpression,
    XRenamer,
    XSelector,
    XSimpleImputer,
    XStandardScaler,
    XMinMaxScaler,
    XOneHotEncoder,
    XConcat,
    xmake_column_transformer,
    ColumnSelector,
    columns
)


class Skippa:

    def __init__(self) -> None:
        self.pipeline_steps = []
        self._step_idx: int = 0

    def build(self, **kwargs):
        return Pipeline(steps=self.pipeline_steps, **kwargs)

    def _step(self, name: str, transformer: Transformation) -> None:
        name = f'{name}_{self._step_idx}'
        self._step_idx += 1
        self.pipeline_steps.append((name, transformer))

    # def _transformer(self, cols, cls: Type[Transformation], **kwargs) -> Transformation:
    #     try:
    #         custom_class_name = eval(f'X{cls.__name__}')
    #         return custom_class_name(cols=cols, **kwargs)
    #     except NameError:
    #         raise NotImplementedError(f'No custom class implemented for {cls} transformer')

    @staticmethod
    def load_pipeline(path) -> Pipeline:
        with open(path, 'rb') as f:
            pipe = dill.loads(f.read())
            return pipe

    def impute(self, cols: ColumnSelector, **kwargs) -> Skippa:
        self._step('impute', XSimpleImputer(cols=cols, **kwargs))
        return self

    def scale(self, cols: ColumnSelector, type: str = 'standard', **kwargs) -> Skippa:
        if type == 'standard':
            transformation = XStandardScaler(cols=cols, **kwargs)
        elif type == 'minmax':
            transformation = XMinMaxScaler(cols=cols, **kwargs)
        else:
            raise ValueError(f'Invalid scaler type "{type}". Choose standard or minmax.')
        self._step(f'scale_{type}', transformation)
        return self

    def onehot(self, cols: ColumnSelector, **kwargs) -> Skippa:
        if cols is None:
            cols = columns(dtype_include='category')

        kwargs['sparse'] = False
        self._step('onehot', XOneHotEncoder(cols=cols, **kwargs))
        return self

    def rename(self, *args, **kwargs) -> Skippa:
        if len(args) == 2:
            cols_to_rename = columns(args[0])
            renamer = args[1]
            assert isinstance(renamer, Callable), 'new names should be a function'
            mapping = (cols_to_rename, renamer)
        elif len(args) == 1 and isinstance(args[0], dict):
            mapping = args[0]
        else:
            mapping = kwargs
        self._step('rename', XRenamer(mapping=mapping))
        return self

    def select(self, cols: ColumnSelector) -> Skippa:
        self._step('select', XSelector(cols))
        return self

    def __add__(self, pipe: Skippa) -> Skippa:
        """Append two Skippas -> does this make sense????

        Args:
            pipe: Skippa: [description]

        Returns:
            Skippa: [description]
        """
        self.pipeline_steps.extend(pipe.pipeline_steps)
        return self

    def concat(self, pipe: Skippa) -> Skippa:
        """Concatenate output of this pipeline to another

        Args:
            pipe (Skippa): [description]

        Returns:
            Skippa: [description]
        """
        new_pipe = Skippa()
        new_pipe._step(
            'concat', 
            XConcat(
                left=('part1', self.build()),
                right=('part2', pipe.build())
            )
        )
        return new_pipe
