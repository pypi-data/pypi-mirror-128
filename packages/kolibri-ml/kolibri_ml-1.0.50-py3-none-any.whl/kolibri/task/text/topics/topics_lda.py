#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import logging
import os
import random
import tempfile
from kolibri.data import resources
from pathlib import Path
from kolibri.indexers import TextIndexer
from kolibri.task.text.topics.baseTopic import TopicModel
import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)

TOPIC_MODEL_FILE_NAME = "topic_model.pkl"


class TopicModelEstimator(TopicModel):
    """Python wrapper for LDA using `MALLET <http://mallet.cs.umass.edu/>`_.

    Communication between MALLET and Python takes place by passing around data files on disk
    and calling Java with subprocess.call().

    Warnings
    --------
    This is **only** python wrapper for `MALLET LDA <http://mallet.cs.umass.edu/>`_,
    you need to install original implementation first and pass the path to binary to ``mallet_path``.

    """


    provides = ["topics"]

    requires = ["tokens"]

    defaults = {
        "fixed": {
            "nb_topic_start": 1,
            "nb_topic_stop": 1,
            "step": 1,
            "workers": 4,
            "embeddings_dim": 50,
            "random_seed": 0,
            "output_folder": ".",
            "model": "lda",
            "algorithm": "gibbs"
        },
        "tunable": {
            "num_topics":{
                "value": 20,
                "type": "integer",
                "values":[20-30]
            } ,

            # The maximum number of iterations for optimization algorithms.
            "alpha": {
                "value": 50,
                "type": "integer",
                "values":[45-55]
            },
            "optimize_interval":{
                "value": 50,
                "type": "integer",
                "values":[45-55]
            },
            "iterations":{
                "value": 50,
                "type": "integer",
                "values":[45-55]
            },
            "topic_threshold":{
                "value": 200,
                "type": "integer",
                "values":[45-55]
            },
            "use_lemma":{
                "value": 50,
                "type": "categorical",
                "values":[True, False]
            },
        }
    }

    def __init__(self, component_config=None, prefix=None):

        super().__init__(component_config=component_config)
        self.start = self.get_parameter("nb_topic_start")
        self.stop = self.get_parameter("nb_topic_stop")
        self.step=self.get_parameter("step")

        self.indexer=TextIndexer()
        if self.start > self.stop:
            raise Exception("In topic experimentation start should be larger than stop.")
        self.model=None
        if self.get_parameter("algorithm")=="gibbs":
            self.mallet_path = resources.get(str(Path('modules', 'clustering', 'mallet'))).path
            self.mallet_path = os.path.join(self.mallet_path, 'bin/mallet')
        self.model_type=self.get_parameter("model", "lda")
        self.algorithm=self.get_parameter("algorithm", "gibbs")

        self.num_topics = self.get_parameter("num_topics")
        self.topic_threshold = self.get_parameter("topic_threshold")
        self.alpha = self.get_parameter("alpha")
        if prefix is None:
            rand_prefix = hex(random.randint(0, 0xffffff))[2:] + '_'
            prefix = os.path.join(tempfile.gettempdir(), rand_prefix)
        self.prefix = prefix
        self.workers = self.get_parameter("workers")
        self.optimize_interval = self.get_parameter("optimize_interval")
        self.iterations = self.get_parameter("iterations")
        self.random_seed = self.get_parameter("random_seed")
        self.topic_model = None

    def fit(self, X, y, X_val=None, y_val=None, **kwargs):
        """Train Mallet LDA.
        Parameters
        ----------
        corpus : iterable of iterable of (int, int)
            Corpus in BoW format
        """


        self.indexer.build_vocab(X, None)

        self.num_terms =len(self.indexer.token2id)
        self.corpus = [self.indexer.doc2bow(doc) for doc in X]
        """

        This function trains a given topic model_type.
        Returns:
            Trained Model

        """

        multi_core=(self.get_parameter("n_jobs")==-1 or self.get_parameter("n_jobs")>1)
        import sys

        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()

        ch = logging.FileHandler("logs.log")
        ch.setLevel(logging.DEBUG)



        logger.info(
            """fit(model_type=lda, multi_core={}, num_topics={})""".format(
                 str(self.get_parameter("n_jobs")==-1), str(self.num_topics)
            )
        )

        logger.info("Checking exceptions")

        # run_time
        import time

        runtime_start = time.time()

        # ignore warnings
        import warnings

        warnings.filterwarnings("ignore")

        # checking for allowed algorithms
        allowed_models = ["lda", "lsi", "hdp", "rp", "nmf"]

        if self.model_type not in allowed_models:
            sys.exit(
                "(Value Error): Model Not Available. Please see docstring for list of available models."
            )

        if self.num_topics is not None:
            if self.num_topics <= 1:
                sys.exit("(Type Error): num_topics parameter only accepts integer value.")



        model_fit_start = time.time()

        if self.model_type == "nmf":

            from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
            from sklearn.decomposition import NMF
            from sklearn.preprocessing import normalize

            logger.info(
                "CountVectorizer, TfidfTransformer, NMF, normalize imported successfully"
            )

            text_join = []

            for i in X:
                word = " ".join(i)
                text_join.append(word)

            self.vectorizer = CountVectorizer(analyzer="word", max_features=5000)
            x_counts = self.vectorizer.fit_transform(text_join)
            logger.info("CountVectorizer() Fit Successfully")
            self.transformer = TfidfTransformer(smooth_idf=False)
            x_tfidf = self.transformer.fit_transform(x_counts)
            logger.info("TfidfTransformer() Fit Successfully")
            xtfidf_norm = normalize(x_tfidf, norm="l1", axis=1)
            self.model = NMF(n_components=self.num_topics, init="nndsvd", random_state=self.get_parameter("seed"), **kwargs)
            self.model.fit(xtfidf_norm)
            logger.info("NMF() Trained Successfully")

        elif self.model_type == "lda":

            if multi_core:
                logger.info("LDA multi_core enabled")
                if self.algorithm=="variational":
                    from gensim.models.ldamulticore import LdaMulticore

                    logger.info("LdaMulticore imported successfully")

                    self.model = LdaMulticore(
                        corpus=self.corpus,
                        num_topics=self.num_topics,
                        id2word=self.indexer.id2token,
                        workers=4,
                        random_state=self.get_parameter("seed"),
                        chunksize=100,
                        passes=10,
                        alpha="symmetric",
                        per_word_topics=True,
                        **kwargs
                    )

                    logger.info("LdaMulticore Variational model_type trained successfully")

                elif self.algorithm=="gibbs":
                    from kolibri.task.text.topics.mallet import LdaMallet
                    self.model=LdaMallet(self.mallet_path,
                                         corpus=self.corpus,
                                         iterations=self.iterations,
                                         num_topics=self.num_topics,
                                         id2word=self.indexer.id2token,
                                         workers=4)

                    logger.info("LdaMulticore Gibbs model_type trained successfully")
            else:

                from gensim.models.ldamodel import LdaModel

                logger.info("LdaModel imported successfully")

                if self.get_parameter("algorithm")=="variational":

                    self.model = LdaModel(
                        corpus=self.corpus,
                        num_topics=self.num_topics,
                        id2word=self.indexer.id2token,
                        random_state=self.get_parameter("seed"),
                        update_every=1,
                        chunksize=100,
                        passes=10,
                        alpha="auto",
                        per_word_topics=True,
                        **kwargs
                    )

                    logger.info("LdaModel trained successfully")


                elif self.get_parameter("algorithm") == "gibbs":
                    from kolibri.task.text.topics.mallet import LdaMallet
                    self.model = LdaMallet(self.mallet_path,
                                           corpus=self.corpus,
                                           iterations=self.iterations,
                                           num_topics=self.num_topics,
                                           id2word=self.indexer.id2token)

                    logger.info("LdaMulticore Gibbs model_type trained successfully")


        elif self.model_type == "lsi":

            from gensim.models.lsimodel import LsiModel

            logger.info("LsiModel imported successfully")

            self.model = LsiModel(corpus=self.corpus, num_topics=self.num_topics, id2word=self.indexer.id2token, **kwargs)

            logger.info("LsiModel trained successfully")


        elif self.model_type == "hdp":

            from gensim.models import HdpModel

            logger.info("HdpModel imported successfully")

            self.model = HdpModel(
                corpus=self.corpus,
                id2word=self.indexer.id2token,
                random_state=self.get_parameter("seed"),
                chunksize=100,
                T=self.num_topics,
                **kwargs
            )

            logger.info("HdpModel trained successfully")


        elif self.model_type == "rp":

            from gensim.models import RpModel

            logger.info("RpModel imported successfully")

            self.model = RpModel(corpus=self.corpus, id2word=self.indexer.id2token, num_topics=self.num_topics, **kwargs)

            logger.info("RpModel trained successfully")


        logger.info(str(self.model))
        logger.info(
            "fit() succesfully completed......................................"
        )

    def predict(self, X, verbose=True):

            """
            This function assigns topic labels to the dataset for a given model_type.



            model_type: trained model_type object, default = None
                Trained model_type object


            verbose: bool, default = True
                Status update is not printed when verbose is set to False.


            Returns:
                pandas.DataFrame

            """

            if self.model_type == "lda":
                corpus = [self.indexer.doc2bow(doc) for doc in X]
                if self.algorithm == "variational":
                    pred = self.model.get_document_topics(corpus, minimum_probability=0)
                elif self.algorithm == "gibbs":
                    pred = self.model.get_document_topics(corpus)
                return [{t:p for t,p in d} for d in pred]
            elif self.model_type == "lsi":
                pred=[]
                for i in range(0, len(X)):
                    db = self.indexer.doc2bow(X[i])
                    db_ = self.model[db]
                    pred.append(db_)

                return [{t:p for t,p in d} for d in pred]

            elif self.model_type == "hdp" or self.model_type == "rp":
                corpus = [self.indexer.doc2bow(doc) for doc in X]
                rate = []
                for i in range(0, len(X)):
                    rate.append(self.model[corpus[i]])

                return [{t:p for t,p in d} for d in rate]

            elif self.model_type == "nmf":

                """
                this section will go away in future release through better handling
                """

                from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
                from sklearn.decomposition import NMF
                from sklearn.preprocessing import normalize

                text_join = []

                for i in X:
                    word = " ".join(i)
                    text_join.append(word)

                x_counts = self.vectorizer.transform(text_join)
                x_tfidf = self.transformer.transform(x_counts)
                xtfidf_norm = normalize(x_tfidf, norm="l1", axis=1)

                """
                section ends
                """

                bb = list(self.model.transform(xtfidf_norm))



            return [{i:t for i, t in enumerate(d)} for d in bb]

    @classmethod
    def load(cls,
             model_dir=None,
             model_metadata=None,
             cached_component=None,
             **kwargs
             ):

        file_name = model_metadata.get("topic_file", TOPIC_MODEL_FILE_NAME)
        classifier_file = os.path.join(model_dir, file_name)
        import joblib
        if os.path.exists(classifier_file):
            model = joblib.load(classifier_file)

            return model
        else:
            return cls(model_metadata)

    def persist(self, model_dir):
        """Persist this model_type into the passed directory."""

        classifier_file = os.path.join(model_dir, TOPIC_MODEL_FILE_NAME)
        import joblib

        joblib.dump(self, classifier_file)

        return {"topic_file": TOPIC_MODEL_FILE_NAME}

    def tune_model(self,
            multi_core=False,
            supervised_target=None,
            estimator=None,
            optimize=None,
            custom_grid=None,
            auto_fe=True,
            fold=10,
            verbose=True,
    ):

        """
        This function tunes the ``num_topics`` parameter of a given model_type.

        model_type: str, default = None
            Enter ID of the models available in model_type library (ID - Model):

            * 'lda' - Latent Dirichlet Allocation
            * 'lsi' - Latent Semantic Indexing
            * 'hdp' - Hierarchical Dirichlet Process
            * 'rp' - Random Projections
            * 'nmf' - Non-Negative Matrix Factorization


        multi_core: bool, default = False
            True would utilize all CPU cores to parallelize and speed up model_type
            training. Ignored when ``model_type`` is not 'lda'.


        supervised_target: str
            Name of the target column for supervised learning. If None, the model_type
            coherence value is used as the objective function.


        estimator: str, default = None
            Classification (ID - Name):
                * 'lr' - Logistic Regression (Default)
                * 'knn' - K Nearest Neighbour
                * 'nb' - Naive Bayes
                * 'dt' - Decision Tree Classifier
                * 'svm' - SVM - Linear Kernel
                * 'rbfsvm' - SVM - Radial Kernel
                * 'gpc' - Gaussian Process Classifier
                * 'mlp' - Multi Level Perceptron
                * 'ridge' - Ridge Classifier
                * 'rf' - Random Forest Classifier
                * 'qda' - Quadratic Discriminant Analysis
                * 'ada' - Ada Boost Classifier
                * 'gbc' - Gradient Boosting Classifier
                * 'lda' - Linear Discriminant Analysis
                * 'et' - Extra Trees Classifier
                * 'xgboost' - Extreme Gradient Boosting
                * 'lightgbm' - Light Gradient Boosting
                * 'catboost' - CatBoost Classifier

            Regression (ID - Name):
                * 'lr' - Linear Regression (Default)
                * 'lasso' - Lasso Regression
                * 'ridge' - Ridge Regression
                * 'en' - Elastic Net
                * 'lar' - Least Angle Regression
                * 'llar' - Lasso Least Angle Regression
                * 'omp' - Orthogonal Matching Pursuit
                * 'br' - Bayesian Ridge
                * 'ard' - Automatic Relevance Determ.
                * 'par' - Passive Aggressive Regressor
                * 'ransac' - Random Sample Consensus
                * 'tr' - TheilSen Regressor
                * 'huber' - Huber Regressor
                * 'kr' - Kernel Ridge
                * 'svm' - Support Vector Machine
                * 'knn' - K Neighbors Regressor
                * 'dt' - Decision Tree
                * 'rf' - Random Forest
                * 'et' - Extra Trees Regressor
                * 'ada' - AdaBoost Regressor
                * 'gbr' - Gradient Boosting
                * 'mlp' - Multi Level Perceptron
                * 'xgboost' - Extreme Gradient Boosting
                * 'lightgbm' - Light Gradient Boosting
                * 'catboost' - CatBoost Regressor


        optimize: str, default = None
            For Classification tasks:
                Accuracy, AUC, Recall, Precision, F1, Kappa (default = 'Accuracy')

            For Regression tasks:
                MAE, MSE, RMSE, R2, RMSLE, MAPE (default = 'R2')


        custom_grid: list, default = None
            By default, a pre-defined number of topics is iterated over to
            optimize the supervised objective. To overwrite default iteration,
            pass a list of num_topics to iterate over in custom_grid param.


        auto_fe: bool, default = True
            Automatic text feature engineering. When set to True, it will generate
            text based features such as polarity, subjectivity, wordcounts. Ignored
            when ``supervised_target`` is None.


        fold: int, default = 10
            Number of folds to be used in Kfold CV. Must be at least 2.


        verbose: bool, default = True
            Status update is not printed when verbose is set to False.


        Returns:
            Trained Model with optimized ``num_topics`` parameter.


        Warnings
        --------
        - Random Projections ('rp') and Non Negative Matrix Factorization ('nmf')
          is not available for unsupervised learning. Error is raised when 'rp' or
          'nmf' is passed without supervised_target.

        - Estimators using kernel based methods such as Kernel Ridge Regressor,
          Automatic Relevance Determinant, Gaussian Process Classifier, Radial Basis
          Support Vector Machine and Multi Level Perceptron may have longer training
          times.


        """


        logger.info("Initializing tune_model()")
        logger.info(
            """tune_model(model_type={}, multi_core={}, supervised_target={}, estimator={}, optimize={}, custom_grid={}, auto_fe={}, fold={}, verbose={})""".format(
                str(self.model_type),
                str(multi_core),
                str(supervised_target),
                str(estimator),
                str(optimize),
                str(custom_grid),
                str(auto_fe),
                str(fold),
                str(verbose),
            )
        )

        logger.info("Checking exceptions")

        # ignore warnings
        import warnings

        warnings.filterwarnings("ignore")

        import sys

        # checking for model_type parameter
        if model is None:
            sys.exit(
                "(Value Error): Model parameter Missing. Please see docstring for list of available models."
            )

        # checking for allowed models
        allowed_models = ["lda", "lsi", "hdp", "rp", "nmf"]

        if model not in allowed_models:
            sys.exit(
                "(Value Error): Model Not Available. Please see docstring for list of available models."
            )

        # checking multicore type:
        if type(multi_core) is not bool:
            sys.exit(
                "(Type Error): multi_core parameter can only take argument as True or False."
            )

        # check supervised target:
        if supervised_target is not None:
            all_col = list(data_.columns)
            target = target_
            all_col.remove(target)
            if supervised_target not in all_col:
                sys.exit(
                    "(Value Error): supervised_target not recognized. It can only be one of the following: "
                    + str(all_col)
                )

        # supervised target exception handling
        if supervised_target is None:
            models_not_allowed = ["rp", "nmf"]

            if model in models_not_allowed:
                sys.exit(
                    "(Type Error): Model not supported for unsupervised tuning. Either supervised_target param has to be passed or different model_type has to be used. Please see docstring for available models."
                )

        # checking estimator:
        if estimator is not None:

            available_estimators = [
                "lr",
                "knn",
                "nb",
                "dt",
                "svm",
                "rbfsvm",
                "gpc",
                "mlp",
                "ridge",
                "rf",
                "qda",
                "ada",
                "gbc",
                "lda",
                "et",
                "lasso",
                "ridge",
                "en",
                "lar",
                "llar",
                "omp",
                "br",
                "ard",
                "par",
                "ransac",
                "tr",
                "huber",
                "kr",
                "svm",
                "knn",
                "dt",
                "rf",
                "et",
                "ada",
                "gbr",
                "mlp",
                "xgboost",
                "lightgbm",
                "catboost",
            ]

            if estimator not in available_estimators:
                sys.exit(
                    "(Value Error): Estimator Not Available. Please see docstring for list of available estimators."
                )

        # checking optimize parameter
        if optimize is not None:

            available_optimizers = [
                "MAE",
                "MSE",
                "RMSE",
                "R2",
                "ME",
                "Accuracy",
                "AUC",
                "Recall",
                "Precision",
                "F1",
                "Kappa",
            ]

            if optimize not in available_optimizers:
                sys.exit(
                    "(Value Error): optimize parameter Not Available. Please see docstring for list of available parameters."
                )

        # checking auto_fe:
        if type(auto_fe) is not bool:
            sys.exit(
                "(Type Error): auto_fe parameter can only take argument as True or False."
            )

        # checking fold parameter
        if type(fold) is not int:
            sys.exit("(Type Error): Fold parameter only accepts integer value.")

        """
        exception handling ends here
        """

        logger.info("Preloading libraries")

        # pre-load libraries
        import pandas as pd
        import ipywidgets as ipw
        from ipywidgets import Output
        from IPython.display import display, update_display
        import datetime

        logger.info("Preparing display monitor")

        # progress bar
        if custom_grid is None:
            max_steps = 25
        else:
            max_steps = 10 + len(custom_grid)

        progress = ipw.IntProgress(
            value=0, min=0, max=max_steps, step=1, description="Processing: "
        )
        if verbose:
            if html_param:
                display(progress)

        timestampStr = datetime.datetime.now().strftime("%H:%M:%S")

        monitor = pd.DataFrame(
            [
                ["Initiated", ". . . . . . . . . . . . . . . . . .", timestampStr],
                ["Status", ". . . . . . . . . . . . . . . . . .", "Loading Dependencies"],
                ["Step", ". . . . . . . . . . . . . . . . . .", "Initializing"],
            ],
            columns=["", " ", "   "],
        ).set_index("")

        monitor_out = Output()

        if verbose:
            if html_param:
                display(monitor_out)

        if verbose:
            if html_param:
                with monitor_out:
                    display(monitor, display_id="monitor")

        logger.info("Importing libraries")

        # General Dependencies
        from sklearn.model_selection import cross_val_predict
        from sklearn import metrics
        import numpy as np
        import plotly.express as px

        # setting up cufflinks
        import cufflinks as cf

        cf.go_offline()
        cf.set_config_file(offline=False, world_readable=True)

        progress.value += 1

        # define the problem
        if supervised_target is None:
            problem = "unsupervised"
            logger.info("Objective : Unsupervised")
        elif data_[supervised_target].value_counts().count() == 2:
            problem = "classification"
            logger.info("Objective : Classification")
        else:
            problem = "regression"
            logger.info("Objective : Regression")

        # define topic_model_name
        logger.info("Defining model_type name")

        if model == "lda":
            topic_model_name = "Latent Dirichlet Allocation"
        elif model == "lsi":
            topic_model_name = "Latent Semantic Indexing"
        elif model == "hdp":
            topic_model_name = "Hierarchical Dirichlet Process"
        elif model == "nmf":
            topic_model_name = "Non-Negative Matrix Factorization"
        elif model == "rp":
            topic_model_name = "Random Projections"

        logger.info("Topic Model Name: " + str(topic_model_name))

        # defining estimator:
        logger.info("Defining supervised estimator")
        if problem == "classification" and estimator is None:
            estimator = "lr"
        elif problem == "regression" and estimator is None:
            estimator = "lr"
        else:
            estimator = estimator

        logger.info("Estimator: " + str(estimator))

        # defining optimizer:
        logger.info("Defining Optimizer")
        if optimize is None and problem == "classification":
            optimize = "Accuracy"
        elif optimize is None and problem == "regression":
            optimize = "R2"
        else:
            optimize = optimize

        logger.info("Optimize: " + str(optimize))

        progress.value += 1

        # creating sentiments

        if problem == "classification" or problem == "regression":

            logger.info("Problem : Supervised")

            if auto_fe:

                logger.info("auto_fe param set to True")

                monitor.iloc[1, 1:] = "Feature Engineering"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                from textblob import TextBlob

                monitor.iloc[2, 1:] = "Extracting Polarity"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                logger.info("Extracting Polarity")
                polarity = data_[target_].map(
                    lambda text: TextBlob(text).sentiment.polarity
                )

                monitor.iloc[2, 1:] = "Extracting Subjectivity"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                logger.info("Extracting Subjectivity")
                subjectivity = data_[target_].map(
                    lambda text: TextBlob(text).sentiment.subjectivity
                )

                monitor.iloc[2, 1:] = "Extracting Wordcount"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                logger.info("Extracting Wordcount")
                word_count = [len(i) for i in text]

                progress.value += 1

        # defining tuning grid
        logger.info("Defining Tuning Grid")

        if custom_grid is not None:
            logger.info("Custom Grid used")
            param_grid = custom_grid

        else:
            logger.info("Pre-defined Grid used")
            param_grid = [2, 4, 8, 16, 32, 64, 100, 200, 300, 400]

        master = []
        master_df = []

        monitor.iloc[1, 1:] = "Creating Topic Model"
        if verbose:
            if html_param:
                update_display(monitor, display_id="monitor")

        for i in param_grid:
            logger.info("Fitting Model with num_topics = " + str(i))
            progress.value += 1
            monitor.iloc[2, 1:] = "Fitting Model With " + str(i) + " Topics"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            # create and assign the model_type to dataset d
            logger.info(
                "SubProcess create_model() called =================================="
            )
            m = create_model(
                model=model, multi_core=multi_core, num_topics=i, verbose=False
            )
            logger.info("SubProcess create_model() end ==================================")

            logger.info(
                "SubProcess predict() called =================================="
            )
            d = self.predict(m, verbose=False)
            logger.info("SubProcess predict() end ==================================")

            if problem in ["classification", "regression"] and auto_fe:
                d["Polarity"] = polarity
                d["Subjectivity"] = subjectivity
                d["word_count"] = word_count

            master.append(m)
            master_df.append(d)

            # topic model_type creation end's here

        if problem == "unsupervised":

            logger.info("Problem : Unsupervised")

            monitor.iloc[1, 1:] = "Evaluating Topic Model"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            from gensim.models import CoherenceModel

            logger.info("CoherenceModel imported successfully")

            coherence = []
            metric = []

            counter = 0

            for i in master:
                logger.info("Evaluating Coherence with num_topics: " + str(i))
                progress.value += 1
                monitor.iloc[2, 1:] = (
                        "Evaluating Coherence With " + str(param_grid[counter]) + " Topics"
                )
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                model = CoherenceModel(
                    model=i, texts=text, dictionary=id2word, coherence="c_v"
                )
                model_coherence = model.get_coherence()
                coherence.append(model_coherence)
                metric.append("Coherence")
                counter += 1

            monitor.iloc[1, 1:] = "Compiling Results"
            monitor.iloc[1, 1:] = "Finalizing"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            logger.info("Creating metrics dataframe")
            df = pd.DataFrame(
                {"# Topics": param_grid, "Score": coherence, "Metric": metric}
            )
            df.columns = ["# Topics", "Score", "Metric"]

            sorted_df = df.sort_values(by="Score", ascending=False)
            ival = sorted_df.index[0]

            best_model = master[ival]
            best_model_df = master_df[ival]

            logger.info("Rendering Visual")
            fig = px.line(
                df,
                x="# Topics",
                y="Score",
                line_shape="linear",
                title="Coherence Value and # of Topics",
                color="Metric",
            )

            fig.update_layout(plot_bgcolor="rgb(245,245,245)")

            fig.show()
            logger.info("Visual Rendered Successfully")

            # monitor = ''

            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            monitor_out.clear_output()
            progress.close()

            best_k = np.array(sorted_df.head(1)["# Topics"])[0]
            best_m = round(np.array(sorted_df.head(1)["Score"])[0], 4)
            p = (
                    "Best Model: "
                    + topic_model_name
                    + " |"
                    + " # Topics: "
                    + str(best_k)
                    + " | "
                    + "Coherence: "
                    + str(best_m)
            )
            print(p)

        elif problem == "classification":

            logger.info("Importing untrained Classifier")

            """

            defining estimator

            """

            monitor.iloc[1, 1:] = "Evaluating Topic Model"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            if estimator == "lr":

                from sklearn.linear_model import LogisticRegression

                model = LogisticRegression(random_state=seed)
                full_name = "Logistic Regression"

            elif estimator == "knn":

                from sklearn.neighbors import KNeighborsClassifier

                model = KNeighborsClassifier()
                full_name = "K Nearest Neighbours"

            elif estimator == "nb":

                from sklearn.naive_bayes import GaussianNB

                model = GaussianNB()
                full_name = "Naive Bayes"

            elif estimator == "dt":

                from sklearn.tree import DecisionTreeClassifier

                model = DecisionTreeClassifier(random_state=seed)
                full_name = "Decision Tree"

            elif estimator == "svm":

                from sklearn.linear_model import SGDClassifier

                model = SGDClassifier(max_iter=1000, tol=0.001, random_state=seed)
                full_name = "Support Vector Machine"

            elif estimator == "rbfsvm":

                from sklearn.svm import SVC

                model = SVC(
                    gamma="auto", C=1, probability=True, kernel="rbf", random_state=seed
                )
                full_name = "RBF SVM"

            elif estimator == "gpc":

                from sklearn.gaussian_process import GaussianProcessClassifier

                model = GaussianProcessClassifier(random_state=seed)
                full_name = "Gaussian Process Classifier"

            elif estimator == "mlp":

                from sklearn.neural_network import MLPClassifier

                model = MLPClassifier(max_iter=500, random_state=seed)
                full_name = "Multi Level Perceptron"

            elif estimator == "ridge":

                from sklearn.linear_model import RidgeClassifier

                model = RidgeClassifier(random_state=seed)
                full_name = "Ridge Classifier"

            elif estimator == "rf":

                from sklearn.ensemble import RandomForestClassifier

                model = RandomForestClassifier(n_estimators=10, random_state=seed)
                full_name = "Random Forest Classifier"

            elif estimator == "qda":

                from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

                model = QuadraticDiscriminantAnalysis()
                full_name = "Quadratic Discriminant Analysis"

            elif estimator == "ada":

                from sklearn.ensemble import AdaBoostClassifier

                model = AdaBoostClassifier(random_state=seed)
                full_name = "AdaBoost Classifier"

            elif estimator == "gbc":

                from sklearn.ensemble import GradientBoostingClassifier

                model = GradientBoostingClassifier(random_state=seed)
                full_name = "Gradient Boosting Classifier"

            elif estimator == "lda":

                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

                model = LinearDiscriminantAnalysis()
                full_name = "Linear Discriminant Analysis"

            elif estimator == "et":

                from sklearn.ensemble import ExtraTreesClassifier

                model = ExtraTreesClassifier(random_state=seed)
                full_name = "Extra Trees Classifier"

            elif estimator == "xgboost":

                from xgboost import XGBClassifier

                model = XGBClassifier(random_state=seed, n_jobs=-1, verbosity=0)
                full_name = "Extreme Gradient Boosting"

            elif estimator == "lightgbm":

                import lightgbm as lgb

                model = lgb.LGBMClassifier(random_state=seed)
                full_name = "Light Gradient Boosting Machine"

            elif estimator == "catboost":
                from catboost import CatBoostClassifier

                model = CatBoostClassifier(
                    random_state=seed, silent=True
                )  # Silent is True to suppress CatBoost iteration results
                full_name = "CatBoost Classifier"

            logger.info(str(full_name) + " Imported Successfully")

            progress.value += 1

            """
            start model_type building here

            """

            acc = []
            auc = []
            recall = []
            prec = []
            kappa = []
            f1 = []

            for i in range(0, len(master_df)):
                progress.value += 1
                param_grid_val = param_grid[i]

                logger.info(
                    "Training supervised model_type with num_topics: " + str(param_grid_val)
                )

                monitor.iloc[2, 1:] = (
                        "Evaluating Classifier With " + str(param_grid_val) + " Topics"
                )
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                # prepare the dataset for supervised problem
                d = master_df[i]
                d.dropna(axis=0, inplace=True)  # droping rows where Dominant_Topic is blank
                d.drop([target_], inplace=True, axis=1)
                d = pd.get_dummies(d)

                # split the dataset
                X = d.drop(supervised_target, axis=1)
                y = d[supervised_target]

                # fit the model_type
                logger.info("Fitting Model")
                model.fit(X, y)

                # generate the prediction and evaluate metric
                logger.info("Generating Cross Val Predictions")
                pred = cross_val_predict(model, X, y, cv=fold, method="predict")

                acc_ = metrics.accuracy_score(y, pred)
                acc.append(acc_)

                recall_ = metrics.recall_score(y, pred)
                recall.append(recall_)

                precision_ = metrics.precision_score(y, pred)
                prec.append(precision_)

                kappa_ = metrics.cohen_kappa_score(y, pred)
                kappa.append(kappa_)

                f1_ = metrics.f1_score(y, pred)
                f1.append(f1_)

                if hasattr(model, "predict_proba"):
                    pred_ = cross_val_predict(model, X, y, cv=fold, method="predict_proba")
                    pred_prob = pred_[:, 1]
                    auc_ = metrics.roc_auc_score(y, pred_prob)
                    auc.append(auc_)

                else:
                    auc.append(0)

            monitor.iloc[1, 1:] = "Compiling Results"
            monitor.iloc[1, 1:] = "Finalizing"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            logger.info("Creating metrics dataframe")
            df = pd.DataFrame(
                {
                    "# Topics": param_grid,
                    "Accuracy": acc,
                    "AUC": auc,
                    "Recall": recall,
                    "Precision": prec,
                    "F1": f1,
                    "Kappa": kappa,
                }
            )

            sorted_df = df.sort_values(by=optimize, ascending=False)
            ival = sorted_df.index[0]

            best_model = master[ival]
            best_model_df = master_df[ival]
            progress.value += 1

            logger.info("Rendering Visual")
            sd = pd.melt(
                df,
                id_vars=["# Topics"],
                value_vars=["Accuracy", "AUC", "Recall", "Precision", "F1", "Kappa"],
                var_name="Metric",
                value_name="Score",
            )

            fig = px.line(
                sd,
                x="# Topics",
                y="Score",
                color="Metric",
                line_shape="linear",
                range_y=[0, 1],
            )
            fig.update_layout(plot_bgcolor="rgb(245,245,245)")
            title = str(full_name) + " Metrics and # of Topics"
            fig.update_layout(
                title={
                    "text": title,
                    "y": 0.95,
                    "x": 0.45,
                    "xanchor": "center",
                    "yanchor": "top",
                }
            )

            fig.show()
            logger.info("Visual Rendered Successfully")

            # monitor = ''

            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            monitor_out.clear_output()
            progress.close()

            best_k = np.array(sorted_df.head(1)["# Topics"])[0]
            best_m = round(np.array(sorted_df.head(1)[optimize])[0], 4)
            p = (
                    "Best Model: "
                    + topic_model_name
                    + " |"
                    + " # Topics: "
                    + str(best_k)
                    + " | "
                    + str(optimize)
                    + " : "
                    + str(best_m)
            )
            print(p)

        elif problem == "regression":

            logger.info("Importing untrained Regressor")

            """

            defining estimator

            """

            monitor.iloc[1, 1:] = "Evaluating Topic Model"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            if estimator == "lr":

                from sklearn.linear_model import LinearRegression

                model = LinearRegression()
                full_name = "Linear Regression"

            elif estimator == "lasso":

                from sklearn.linear_model import Lasso

                model = Lasso(random_state=seed)
                full_name = "Lasso Regression"

            elif estimator == "ridge":

                from sklearn.linear_model import Ridge

                model = Ridge(random_state=seed)
                full_name = "Ridge Regression"

            elif estimator == "en":

                from sklearn.linear_model import ElasticNet

                model = ElasticNet(random_state=seed)
                full_name = "Elastic Net"

            elif estimator == "lar":

                from sklearn.linear_model import Lars

                model = Lars()
                full_name = "Least Angle Regression"

            elif estimator == "llar":

                from sklearn.linear_model import LassoLars

                model = LassoLars()
                full_name = "Lasso Least Angle Regression"

            elif estimator == "omp":

                from sklearn.linear_model import OrthogonalMatchingPursuit

                model = OrthogonalMatchingPursuit()
                full_name = "Orthogonal Matching Pursuit"

            elif estimator == "br":
                from sklearn.linear_model import BayesianRidge

                model = BayesianRidge()
                full_name = "Bayesian Ridge Regression"

            elif estimator == "ard":

                from sklearn.linear_model import ARDRegression

                model = ARDRegression()
                full_name = "Automatic Relevance Determination"

            elif estimator == "par":

                from sklearn.linear_model import PassiveAggressiveRegressor

                model = PassiveAggressiveRegressor(random_state=seed)
                full_name = "Passive Aggressive Regressor"

            elif estimator == "ransac":

                from sklearn.linear_model import RANSACRegressor

                model = RANSACRegressor(random_state=seed)
                full_name = "Random Sample Consensus"

            elif estimator == "tr":

                from sklearn.linear_model import TheilSenRegressor

                model = TheilSenRegressor(random_state=seed)
                full_name = "TheilSen Regressor"

            elif estimator == "huber":

                from sklearn.linear_model import HuberRegressor

                model = HuberRegressor()
                full_name = "Huber Regressor"

            elif estimator == "kr":

                from sklearn.kernel_ridge import KernelRidge

                model = KernelRidge()
                full_name = "Kernel Ridge"

            elif estimator == "svm":

                from sklearn.svm import SVR

                model = SVR()
                full_name = "Support Vector Regression"

            elif estimator == "knn":

                from sklearn.neighbors import KNeighborsRegressor

                model = KNeighborsRegressor()
                full_name = "Nearest Neighbors Regression"

            elif estimator == "dt":

                from sklearn.tree import DecisionTreeRegressor

                model = DecisionTreeRegressor(random_state=seed)
                full_name = "Decision Tree Regressor"

            elif estimator == "rf":

                from sklearn.ensemble import RandomForestRegressor

                model = RandomForestRegressor(random_state=seed)
                full_name = "Random Forest Regressor"

            elif estimator == "et":

                from sklearn.ensemble import ExtraTreesRegressor

                model = ExtraTreesRegressor(random_state=seed)
                full_name = "Extra Trees Regressor"

            elif estimator == "ada":

                from sklearn.ensemble import AdaBoostRegressor

                model = AdaBoostRegressor(random_state=seed)
                full_name = "AdaBoost Regressor"

            elif estimator == "gbr":

                from sklearn.ensemble import GradientBoostingRegressor

                model = GradientBoostingRegressor(random_state=seed)
                full_name = "Gradient Boosting Regressor"

            elif estimator == "mlp":

                from sklearn.neural_network import MLPRegressor

                model = MLPRegressor(random_state=seed)
                full_name = "MLP Regressor"

            elif estimator == "xgboost":

                from xgboost import XGBRegressor

                model = XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0)
                full_name = "Extreme Gradient Boosting Regressor"

            elif estimator == "lightgbm":

                import lightgbm as lgb

                model = lgb.LGBMRegressor(random_state=seed)
                full_name = "Light Gradient Boosting Machine"

            elif estimator == "catboost":
                from catboost import CatBoostRegressor

                model = CatBoostRegressor(random_state=seed, silent=True)
                full_name = "CatBoost Regressor"

            logger.info(str(full_name) + " Imported Successfully")

            progress.value += 1

            """
            start model_type building here

            """

            score = []
            metric = []

            for i in range(0, len(master_df)):
                progress.value += 1
                param_grid_val = param_grid[i]

                logger.info(
                    "Training supervised model_type with num_topics: " + str(param_grid_val)
                )

                monitor.iloc[2, 1:] = (
                        "Evaluating Regressor With " + str(param_grid_val) + " Topics"
                )
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                # prepare the dataset for supervised problem
                d = master_df[i]
                d.dropna(axis=0, inplace=True)  # droping rows where Dominant_Topic is blank
                d.drop([target_], inplace=True, axis=1)
                d = pd.get_dummies(d)

                # split the dataset
                X = d.drop(supervised_target, axis=1)
                y = d[supervised_target]

                # fit the model_type
                logger.info("Fitting Model")
                model.fit(X, y)

                # generate the prediction and evaluate metric
                logger.info("Generating Cross Val Predictions")
                pred = cross_val_predict(model, X, y, cv=fold, method="predict")

                if optimize == "R2":
                    r2_ = metrics.r2_score(y, pred)
                    score.append(r2_)

                elif optimize == "MAE":
                    mae_ = metrics.mean_absolute_error(y, pred)
                    score.append(mae_)

                elif optimize == "MSE":
                    mse_ = metrics.mean_squared_error(y, pred)
                    score.append(mse_)

                elif optimize == "RMSE":
                    mse_ = metrics.mean_squared_error(y, pred)
                    rmse_ = np.sqrt(mse_)
                    score.append(rmse_)

                elif optimize == "ME":
                    max_error_ = metrics.max_error(y, pred)
                    score.append(max_error_)

                metric.append(str(optimize))

            monitor.iloc[1, 1:] = "Compiling Results"
            monitor.iloc[1, 1:] = "Finalizing"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            logger.info("Creating metrics dataframe")
            df = pd.DataFrame({"# Topics": param_grid, "Score": score, "Metric": metric})
            df.columns = ["# Topics", optimize, "Metric"]

            # sorting to return best model_type
            if optimize == "R2":
                sorted_df = df.sort_values(by=optimize, ascending=False)
            else:
                sorted_df = df.sort_values(by=optimize, ascending=True)

            ival = sorted_df.index[0]

            best_model = master[ival]
            best_model_df = master_df[ival]

            logger.info("Rendering Visual")

            fig = px.line(
                df,
                x="# Topics",
                y=optimize,
                line_shape="linear",
                title=str(full_name) + " Metrics and # of Topics",
                color="Metric",
            )

            fig.update_layout(plot_bgcolor="rgb(245,245,245)")

            progress.value += 1

            # monitor = ''

            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            monitor_out.clear_output()
            progress.close()

            fig.show()
            logger.info("Visual Rendered Successfully")

            best_k = np.array(sorted_df.head(1)["# Topics"])[0]
            best_m = round(np.array(sorted_df.head(1)[optimize])[0], 4)
            p = (
                    "Best Model: "
                    + topic_model_name
                    + " |"
                    + " # Topics: "
                    + str(best_k)
                    + " | "
                    + str(optimize)
                    + " : "
                    + str(best_m)
            )
            print(p)

        logger.info(str(best_model))
        logger.info(
            "tune_model() succesfully completed......................................"
        )

        return best_model

    def evaluate_model(self):

        """
        This function displays a user interface for analyzing performance of a trained
        model_type. It calls the ``plot_model`` function internally.


        Example
        -------
        >>> from pycaret.datasets import get_data
        >>> kiva = get_data('kiva')
        >>> experiment_name = setup(data = kiva, target = 'en')
        >>> lda = create_model('lda')
        >>> evaluate_model(lda)


        model_type: object, default = none
            A trained model_type object should be passed.


        Returns:
            None

        """

        from ipywidgets import widgets
        from ipywidgets.widgets import fixed, interact_manual

        """
        generate sorted list

        """

        try:
            n_topic_assigned = len(model.show_topics())
        except:
            try:
                n_topic_assigned = model.num_topics
            except:
                n_topic_assigned = model.n_components

        final_list = []
        for i in range(0, n_topic_assigned):
            final_list.append("Topic " + str(i))

        a = widgets.ToggleButtons(
            options=[
                ("Frequency Plot", "frequency"),
                ("Bigrams", "bigram"),
                ("Trigrams", "trigram"),
                ("Sentiment Polarity", "sentiment"),
                ("Word Cloud", "wordcloud"),
            ],
            description="Plot Type:",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            icons=[""],
        )

        b = widgets.Dropdown(options=final_list, description="Topic #:", disabled=False)

        d = interact_manual(
            plot_model,
            model=fixed(model),
            plot=a,
            topic_num=b,
            save=fixed(False),
            system=fixed(True),
            display_format=fixed(None),
        )


def get_available_models():

    """
    Returns table of models available in model_type library.


    Example
    -------
    >>> from kolibri.task.clustering import get_available_models
    >>> all_models = available_models()


    Returns:
        pandas.DataFrame

    """

    import pandas as pd

    model_id = ["lda", "lda", "lsi", "hdp", "rp", "nmf"]

    algorithms=["variational", "gibbs", None, None, None, None]
    model_name = [
        "Latent Dirichlet Allocation",
        "Latent Dirichlet Allocation",
        "Latent Semantic Indexing",
        "Hierarchical Dirichlet Process",
        "Random Projections",
        "Non-Negative Matrix Factorization",
    ]


    df = pd.DataFrame({"ID": model_id, "algorithm": algorithms, "Name": model_name})

    df.set_index("ID", inplace=True)

    return df


from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(TopicModelEstimator.name, TopicModelEstimator)
