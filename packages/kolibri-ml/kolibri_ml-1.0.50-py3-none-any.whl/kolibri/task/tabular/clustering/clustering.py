import datetime, time
import numpy as np
import warnings
from kolibri.backend.base.estimator import BaseEstimator
from kolibri.backend.models import get_unsupervised_model
from kolibri.evaluators.clustering_evaluator import ClusteringEvaluator
from kolibri.logger import get_logger
import pandas as pd
from kolibri.config import TaskType
from kdmt.dict import update


logger = get_logger(__name__)
warnings.filterwarnings("ignore")


class ClusteringEstimator(BaseEstimator):

    defaults={
        "fixed":{
            "log_plot": False,
            "n_clusters": 4,
            "round": 4,
            "verbose": False,
            "ground-truth":None,
            "model": None,
            "seed": 42,
            'task-type': TaskType.CLUSTERING
        },
        "model": {

            }
    }
    def __init__(self, configs={}):
        super().__init__(configs)
        self.hyperparameters["tunable"]["model"]=get_unsupervised_model(self.get_parameter("model"))
        self.update_model_parameters()
        self.model=self.load_model_from_parameters(get_unsupervised_model(self.get_parameter("model")))[1]

        self.evaluator=ClusteringEvaluator()
    def reload_model(self, new_config=None):
        if new_config is not None:
            for c in new_config:
                if c in self.hyperparameters["tunable"]["model"]["parameters"]:
                    self.hyperparameters["tunable"]["model"]["parameters"][c]["value"]= new_config[c]

        self.model=self.load_model_from_parameters(get_unsupervised_model(self.get_parameter("model")))[1]

    def fit( self, X: None, y=None, **kwargs):

            logger.info("Start model estimation")

            # general dependencies
            seed=self.get_parameter("seed")
            np.random.seed(seed)

            logger.info("Fitting Model")
            model_fit_start = time.time()
            self.model.fit(X, **kwargs)
            model_fit_end = time.time()

            model_fit_time = np.array(model_fit_end - model_fit_start).round(2)

            print("fit time: ", model_fit_time)

            if y is not None:
                gt = y
            else:
                gt = None


            metrics = self.evaluator.calculate_unsupervised_metrics(X, self.model.labels_, ground_truth=gt)


            logger.info(str(self.model))
            logger.info(
                "create_models() succesfully completed......................................"
            )

            logger.info("Uploading results into container")

            self.model_results = pd.DataFrame(metrics, index=[0])
            self.model_results =self.model_results.round(self.get_parameter("round"))

            return self.model

from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(ClusteringEstimator.name, ClusteringEstimator)

#
# def assign_model(
#     model, transformation: bool = False, verbose: bool = True
# ) -> pd.DataFrame:
#
#     return pycaret.internal.tabular.assign_model(
#         model, transformation=transformation, verbose=verbose
#     )
#
#
# def plot_model(
#     model,
#     plot: str = "cluster",
#     feature: Optional[str] = None,
#     label: bool = False,
#     scale: float = 1,
#     save: bool = False,
#     display_format: Optional[str] = None,
# ):
#
#     return pycaret.internal.tabular.plot_model(
#         model,
#         plot=plot,
#         feature_name=feature,
#         label=label,
#         scale=scale,
#         save=save,
#         display_format=display_format,
#     )
#
#
# def evaluate_model(
#     model, feature: Optional[str] = None, fit_kwargs: Optional[dict] = None,
# ):
#
#     return pycaret.internal.tabular.evaluate_model(
#         estimator=model, feature_name=feature, fit_kwargs=fit_kwargs
#     )
#
#
# def tune_model(
#     model,
#     supervised_target: str,
#     supervised_type: Optional[str] = None,
#     supervised_estimator: Union[str, Any] = "lr",
#     optimize: Optional[str] = None,
#     custom_grid: Optional[List[int]] = None,
#     fold: int = 10,
#     fit_kwargs: Optional[dict] = None,
#     groups: Optional[Union[str, Any]] = None,
#     round: int = 4,
#     verbose: bool = True,
# ):
#
#     return pycaret.internal.tabular.tune_model_unsupervised(
#         model=model,
#         supervised_target=supervised_target,
#         supervised_type=supervised_type,
#         supervised_estimator=supervised_estimator,
#         optimize=optimize,
#         custom_grid=custom_grid,
#         fold=fold,
#         fit_kwargs=fit_kwargs,
#         groups=groups,
#         round=round,
#         verbose=verbose,
#     )
#
#
# def predict_model(model, data: pd.DataFrame) -> pd.DataFrame:
#
#     return pycaret.internal.tabular.predict_model_unsupervised(
#         estimator=model, data=data, ml_task=MLUsecase.CLUSTERING,
#     )
#
#
# def deploy_model(
#     model, model_name: str, authentication: dict, platform: str = "aws",
# ):
#
#     return pycaret.internal.tabular.deploy_model(
#         model=model,
#         model_name=model_name,
#         authentication=authentication,
#         platform=platform,
#     )
#
#
# def save_model(
#     model, model_name: str, model_only: bool = False, verbose: bool = True, **kwargs
# ):
#
#     return pycaret.internal.tabular.save_model(
#         model=model,
#         model_name=model_name,
#         model_only=model_only,
#         verbose=verbose,
#         **kwargs,
#     )
#
#
# def load_model(
#     model_name,
#     platform: Optional[str] = None,
#     authentication: Optional[Dict[str, str]] = None,
#     verbose: bool = True,
# ):
#
#     return pycaret.internal.tabular.load_model(
#         model_name=model_name,
#         platform=platform,
#         authentication=authentication,
#         verbose=verbose,
#     )
#
#
# def pull(pop: bool = False) -> pd.DataFrame:
#
#     return pycaret.internal.tabular.pull(pop=pop)
#
#
# def models(internal: bool = False, raise_errors: bool = True) -> pd.DataFrame:
#
#     return pycaret.internal.tabular.models(internal=internal, raise_errors=raise_errors)
#
#
# def get_metrics(
#     reset: bool = False, include_custom: bool = True, raise_errors: bool = True,
# ) -> pd.DataFrame:
#
#     return pycaret.internal.tabular.get_metrics(
#         reset=reset, include_custom=include_custom, raise_errors=raise_errors,
#     )
#
#
# def add_metric(
#     id: str,
#     name: str,
#     score_func: type,
#     target: str = "pred",
#     greater_is_better: bool = True,
#     multiclass: bool = True,
#     **kwargs
# ) -> pd.Series:
#
#     return pycaret.internal.tabular.add_metric(
#         id=id,
#         name=name,
#         score_func=score_func,
#         target=target,
#         greater_is_better=greater_is_better,
#         multiclass=multiclass,
#         **kwargs,
#     )
#
#
# def remove_metric(name_or_id: str):
#
#     return pycaret.internal.tabular.remove_metric(name_or_id=name_or_id)
#
#
# def get_logs(experiment_name: Optional[str] = None, save: bool = False) -> pd.DataFrame:
#
#     return pycaret.internal.tabular.get_logs(experiment_name=experiment_name, save=save)
#
#
# def get_config(variable: str):
#
#     return pycaret.internal.tabular.get_config(variable=variable)
#
#
# def set_config(variable: str, value):
#
#
#     return pycaret.internal.tabular.set_config(variable=variable, value=value)
#
#
# def save_config(file_name: str):
#
#     return pycaret.internal.tabular.save_config(file_name=file_name)
#
#
# def load_config(file_name: str):
#
#     return pycaret.internal.tabular.load_config(file_name=file_name)
#
# def get_available_models():
#     # *'kmeans' - K - Means
#     # Clustering
#     # *'ap' - Affinity
#     # Propagation
#     # *'meanshift' - Mean
#     # shift
#     # Clustering
#     # *'sc' - Spectral
#     # Clustering
#     # *'hclust' - Agglomerative
#     # Clustering
#     # *'dbscan' - Density - Based
#     # Spatial
#     # Clustering
#     # *'optics' - OPTICS
#     # Clustering
#     # *'birch' - Birch
#     # Clustering
#     # *'kmodes' - K - Modes
#     # Clustering
#     pass
#
# def get_clusters(
#     data,
#     model: Union[str, Any] = "kmeans",
#     num_clusters: int = 4,
#     ground_truth: Optional[str] = None,
#     round: int = 4,
#     fit_kwargs: Optional[dict] = None,
#     preprocess: bool = True,
#     imputation_type: str = "simple",
#     iterative_imputation_iters: int = 5,
#     categorical_features: Optional[List[str]] = None,
#     categorical_imputation: str = "mode",
#     categorical_iterative_imputer: Union[str, Any] = "lightgbm",
#     ordinal_features: Optional[Dict[str, list]] = None,
#     high_cardinality_features: Optional[List[str]] = None,
#     high_cardinality_method: str = "frequency",
#     numeric_features: Optional[List[str]] = None,
#     numeric_imputation: str = "mean",  # method 'zero' added in pycaret==2.1
#     numeric_iterative_imputer: Union[str, Any] = "lightgbm",
#     date_features: Optional[List[str]] = None,
#     ignore_features: Optional[List[str]] = None,
#     normalize: bool = False,
#     normalize_method: str = "zscore",
#     transformation: bool = False,
#     transformation_method: str = "yeo-johnson",
#     handle_unknown_categorical: bool = True,
#     unknown_categorical_method: str = "least_frequent",
#     pca: bool = False,
#     pca_method: str = "linear",
#     pca_components: Optional[float] = None,
#     ignore_low_variance: bool = False,
#     combine_rare_levels: bool = False,
#     rare_level_threshold: float = 0.10,
#     bin_numeric_features: Optional[List[str]] = None,
#     remove_multicollinearity: bool = False,
#     multicollinearity_threshold: float = 0.9,
#     remove_perfect_collinearity: bool = False,
#     group_features: Optional[List[str]] = None,
#     group_names: Optional[List[str]] = None,
#     n_jobs: Optional[int] = -1,
#     session_id: Optional[int] = None,
#     log_experiment: bool = False,
#     experiment_name: Optional[str] = None,
#     log_plots: Union[bool, list] = False,
#     log_profile: bool = False,
#     log_data: bool = False,
#     profile: bool = False,
#     **kwargs
# ) -> pd.DataFrame:
#
#     """
#     Callable from any external environment without requiring setup initialization.
#     """
#     setup(
#         data=data,
#         preprocess=preprocess,
#         imputation_type=imputation_type,
#         iterative_imputation_iters=iterative_imputation_iters,
#         categorical_features=categorical_features,
#         categorical_imputation=categorical_imputation,
#         categorical_iterative_imputer=categorical_iterative_imputer,
#         ordinal_features=ordinal_features,
#         high_cardinality_features=high_cardinality_features,
#         high_cardinality_method=high_cardinality_method,
#         numeric_features=numeric_features,
#         numeric_imputation=numeric_imputation,
#         numeric_iterative_imputer=numeric_iterative_imputer,
#         date_features=date_features,
#         ignore_features=ignore_features,
#         normalize=normalize,
#         normalize_method=normalize_method,
#         transformation=transformation,
#         transformation_method=transformation_method,
#         handle_unknown_categorical=handle_unknown_categorical,
#         unknown_categorical_method=unknown_categorical_method,
#         pca=pca,
#         pca_method=pca_method,
#         pca_components=pca_components,
#         ignore_low_variance=ignore_low_variance,
#         combine_rare_levels=combine_rare_levels,
#         rare_level_threshold=rare_level_threshold,
#         bin_numeric_features=bin_numeric_features,
#         remove_multicollinearity=remove_multicollinearity,
#         multicollinearity_threshold=multicollinearity_threshold,
#         remove_perfect_collinearity=remove_perfect_collinearity,
#         group_features=group_features,
#         group_names=group_names,
#         n_jobs=n_jobs,
#         html=False,
#         session_id=session_id,
#         log_experiment=log_experiment,
#         experiment_name=experiment_name,
#         log_plots=log_plots,
#         log_profile=log_profile,
#         log_data=log_data,
#         silent=True,
#         verbose=False,
#         profile=profile,
#     )
#
#     c = create_model(
#         model=model,
#         num_clusters=num_clusters,
#         ground_truth=ground_truth,
#         round=round,
#         fit_kwargs=fit_kwargs,
#         verbose=False,
#         **kwargs,
#     )
#     dataset = assign_model(c, verbose=False)
#     return dataset
