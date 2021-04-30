# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/111b_models.MINIROCKET.ipynb (unless otherwise specified).

__all__ = ['MiniRocketClassifier', 'load_minirocket', 'MiniRocketRegressor', 'load_minirocket',
           'MiniRocketVotingClassifier', 'get_minirocket_preds', 'MiniRocketVotingRegressor']

# Cell
from ..imports import *
from ..utils import *
from ..data.external import *
from .layers import *

# Cell
from sktime.transformations.panel.rocket._minirocket import _fit as minirocket_fit
from sktime.transformations.panel.rocket._minirocket import _transform as minirocket_transform
from sktime.transformations.panel.rocket._minirocket_multivariate import _fit_multi as minirocket_fit_multi
from sktime.transformations.panel.rocket._minirocket_multivariate import _transform_multi as minirocket_transform_multi
from sktime.transformations.panel.rocket import MiniRocketMultivariate
from sklearn.linear_model import RidgeCV, RidgeClassifierCV
from sklearn.ensemble import VotingClassifier, VotingRegressor

# Cell
class MiniRocketClassifier(sklearn.pipeline.Pipeline):
    """Time series classification using MINIROCKET features and a linear classifier"""
    def __init__(self, num_features=10_000, max_dilations_per_kernel=32, random_state=None,
                 alphas=np.logspace(-3, 3, 7), normalize_features=True, memory=None, verbose=False, scoring=None, class_weight=None, **kwargs):
        """
        MiniRocketClassifier is recommended for up to 10k time series.
        For a larger dataset, you can use MINIROCKET (in Pytorch).
        scoring = None --> defaults to accuracy.
        """
        self.steps = [('minirocketmultivariate', MiniRocketMultivariate(num_features=num_features,
                                                                        max_dilations_per_kernel=max_dilations_per_kernel,
                                                                        random_state=random_state)),
                      ('ridgeclassifiercv', RidgeClassifierCV(alphas=alphas,
                                                              normalize=normalize_features,
                                                              scoring=scoring,
                                                              class_weight=class_weight,
                                                              **kwargs))]
        store_attr()
        self._validate_steps()

    def __repr__(self):
        return f'Pipeline(steps={self.steps.copy()})'

    def save(self, fname=None, path='./models'):
        fname = ifnone(fname, 'MiniRocketClassifier')
        path = Path(path)
        filename = path/fname
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(f'{filename}.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

# Cell
def load_minirocket(fname, path='./models'):
    path = Path(path)
    filename = path/fname
    with open(f'{filename}.pkl', 'rb') as input:
        output = pickle.load(input)
    return output

# Cell
class MiniRocketRegressor(sklearn.pipeline.Pipeline):
    """Time series regression using MINIROCKET features and a linear regressor"""
    def __init__(self, num_features=10000, max_dilations_per_kernel=32, random_state=None,
                 alphas=np.logspace(-3, 3, 7), *, normalize_features=True, memory=None, verbose=False, scoring=None, **kwargs):
        """
        MiniRocketRegressor is recommended for up to 10k time series.
        For a larger dataset, you can use MINIROCKET (in Pytorch).
        scoring = None --> defaults to r2.
        """
        self.steps = [('minirocketmultivariate', MiniRocketMultivariate(num_features=num_features,
                                                                        max_dilations_per_kernel=max_dilations_per_kernel,
                                                                        random_state=random_state)),
                      ('ridgecv', RidgeCV(alphas=alphas, normalize=normalize_features, scoring=scoring, **kwargs))]
        store_attr()
        self._validate_steps()

    def __repr__(self):
        return f'Pipeline(steps={self.steps.copy()})'

    def save(self, fname=None, path='./models'):
        fname = ifnone(fname, 'MiniRocketRegressor')
        path = Path(path)
        filename = path/fname
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(f'{filename}.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

# Cell
def load_minirocket(fname, path='./models'):
    path = Path(path)
    filename = path/fname
    with open(f'{filename}.pkl', 'rb') as input:
        output = pickle.load(input)
    return output

# Cell
class MiniRocketVotingClassifier(VotingClassifier):
    """Time series classification ensemble using MINIROCKET features, a linear classifier and majority voting"""
    def __init__(self, n_estimators=5, weights=None, n_jobs=-1, num_features=10_000, max_dilations_per_kernel=32, random_state=None,
                 alphas=np.logspace(-3, 3, 7), normalize_features=True, memory=None, verbose=False, scoring=None, class_weight=None, **kwargs):
        store_attr()
        estimators = [(f'est_{i}', MiniRocketClassifier(num_features=num_features, max_dilations_per_kernel=max_dilations_per_kernel,
                                                       random_state=random_state, alphas=alphas, normalize_features=normalize_features, memory=memory,
                                                       verbose=verbose, scoring=scoring, class_weight=class_weight, **kwargs))
                    for i in range(n_estimators)]
        super().__init__(estimators, voting='hard', weights=weights, n_jobs=n_jobs, verbose=verbose)

    def __repr__(self):
        return f'MiniRocketVotingClassifier(n_estimators={self.n_estimators}, \nsteps={self.estimators[0][1].steps})'

    def save(self, fname=None, path='./models'):
        fname = ifnone(fname, 'MiniRocketVotingClassifier')
        path = Path(path)
        filename = path/fname
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(f'{filename}.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

# Cell
def get_minirocket_preds(X, fname, path='./models', model=None):
    if X.ndim == 1: X = X[np.newaxis][np.newaxis]
    elif X.ndim == 2: X = X[np.newaxis]
    if model is None:
        model = load_minirocket(fname=fname, path=path)
    return model.predict(X)

# Cell
class MiniRocketVotingRegressor(VotingRegressor):
    """Time series regression ensemble using MINIROCKET features, a linear regressor and a voting regressor"""
    def __init__(self, n_estimators=5, weights=None, n_jobs=-1, num_features=10_000, max_dilations_per_kernel=32, random_state=None,
                 alphas=np.logspace(-3, 3, 7), normalize_features=True, memory=None, verbose=False, scoring=None, **kwargs):
        store_attr()
        estimators = [(f'est_{i}', MiniRocketRegressor(num_features=num_features, max_dilations_per_kernel=max_dilations_per_kernel,
                                                      random_state=random_state, alphas=alphas, normalize_features=normalize_features, memory=memory,
                                                      verbose=verbose, scoring=scoring, **kwargs))
                      for i in range(n_estimators)]
        super().__init__(estimators, weights=weights, n_jobs=n_jobs, verbose=verbose)

    def __repr__(self):
        return f'MiniRocketVotingRegressor(n_estimators={self.n_estimators}, \nsteps={self.estimators[0][1].steps})'

    def save(self, fname=None, path='./models'):
        fname = ifnone(fname, 'MiniRocketVotingRegressor')
        path = Path(path)
        filename = path/fname
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(f'{filename}.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)