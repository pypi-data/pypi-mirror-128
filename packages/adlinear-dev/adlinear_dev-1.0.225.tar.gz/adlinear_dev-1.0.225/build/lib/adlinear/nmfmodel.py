import math
from nmtf import NMF
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# from .utilities import *
from . import utilities as utl
from typing import Union, Tuple
from sklearn.svm import SVC


class NmfModel:
    def __init__(
        self,
        mat: Union[np.ndarray, pd.DataFrame],
        ncomp: int,
        nblocks: int = 1,
        name: str = "",
        use_hals: bool = True,
        beta_loss: str = "frobenius",
        leverage: str = "standard",
        kernel: str = "linear",
        tol: float = 1e-6,
        max_iter: int = 150,
        max_iter_mult: int = 20,
        regularization: str = None,
        features_names: Tuple[str] = None,
        object_names: Tuple[str] = None,
    ):

        if object_names is None:
            object_names = []
        if features_names is None:
            features_names = []
        self._fnames = []
        self._objnames = []
        self._ncomp = ncomp
        self._hals = use_hals
        self._beta_loss = beta_loss
        self._tol = tol
        if isinstance(max_iter, str):
            self._max_iter = (max_iter,)
        else:
            self._max_iter = max_iter
        if isinstance(max_iter_mult, str):
            self._max_iter_mult = (max_iter_mult,)
        else:
            self._max_iter_mult = max_iter_mult
        self._regularization = regularization
        self._leverage = leverage
        if isinstance(kernel, str):
            self._kernel = (kernel,)
        else:
            self._kernel = kernel
        nblocks = 1
        self._nblocks = nblocks
        self._sparsity = 0
        self._n_bootstrap = 0
        self._estimator = None
        self._predictor = None
        self._error = 0
        self._volume = 0
        self._errors = None

        if type(mat) is not pd.DataFrame:
            self._nobj, self._nfeat = pd.DataFrame(mat).shape
            self._fnames = (
                features_names
                if len(features_names) == self._nfeat
                else list(["F" + str(x) for x in range(1, self._nfeat + 1)])
            )
            self._objnames = (
                object_names
                if len(object_names) == self._nobj
                else list(["O" + str(x) for x in range(1, self._nobj + 1)])
            )
            self._mat = pd.DataFrame(mat, index=self._objnames, columns=self._fnames)
        else:

            self._fnames = list([col for col in mat.columns])
            self._objnames = list(mat.index)
            self._mat = mat
            self._nobj, self._nfeat = mat.shape

        self._filledmat = self._mat.copy()

        if name == "":
            self._name = "NMF_" + str(self._ncomp) + "(O" + str(self._nobj) + ",F" + str(self._nfeat) + ")"
        else:
            self._name = name

        self._sortedmat = self._filledmat.copy()
        self._model = NMF(n_components=ncomp, use_hals=use_hals)
        self._estimator = None
        self._predictor = None
        self._error = None
        self._volume = None

    def _reset(self):
        if hasattr(self, "_estimator"):
            delattr(self, "_estimator")
        if hasattr(self, "_estimator"):
            delattr(self, "_predictor")

    def clone(self):
        model = NmfModel(
            mat=self._mat,
            ncomp=self._ncomp,
            name=self._name,
            use_hals=self._hals,
            beta_loss=self._beta_loss,
            leverage=self._leverage,
            kernel=self._kernel,
            tol=self._tol,
            max_iter=self._max_iter,
            max_iter_mult=self._max_iter_mult,
            regularization=self._regularization,
            features_names=self._fnames,
            object_names=self._objnames,
        )

        model.set_sparsity(self._sparsity)
        model.set_n_bootstrap(self._n_bootstrap)
        return model

    def set_sparsity(self, sparsity):
        sp = self._sparsity
        self._sparsity = sparsity
        if sp != sparsity:
            self._reset()

    def set_n_bootstrap(self, n_bootstrap):
        self._n_bootstrap = n_bootstrap

    def set_ncomp(self, ncomp):
        self.__init__(
            mat=self._mat,
            ncomp=ncomp,
            name=self._name,
            use_hals=self._hals,
            beta_loss=self._beta_loss,
            leverage=self._leverage,
            kernel=self._kernel,
            tol=self._tol,
            max_iter=self._max_iter,
            max_iter_mult=self._max_iter_mult,
            regularization=self._regularization,
            features_names=self._fnames,
            object_names=self._objnames,
        )
        self._reset()

    def test_model(self, nfill_iters=1, verbose=True) -> None:

        # n_fills = max(1, n_fills)
        self._errors = np.zeros(nfill_iters)
        # n_fills == 0: pas d'imputation des valeurs manquantes de la matrice
        if nfill_iters == 0:
            fill_trials = range(1)
            self._errors = np.zeros(1)
        # n_fills >= 1
        # première imputation décidée par l'utilisateur, par défaut: moyenne par colonne
        # imputations suivantes (si n_fills >= 2) en prenant pour chaque colonne, et pour chaque observation
        # la moyenne des valeurs de la colonne dans le cluster de cette observation

        else:
            fill_trials = range(1, nfill_iters + 1)
            self._errors = np.zeros(nfill_iters)
        for itrial in fill_trials:
            if itrial == 0:
                self._filledmat = self._mat
            # itrial = 1: imputation standard
            elif itrial == 1:
                self._filledmat = utl.fill_missing(self._mat, method="median")
            # itrial >= 2: imputation par les valeurs approchées obtenues à l'étape précédente
            else:
                w = self.get_w()
                h = self.get_h()
                self._filledmat = utl.fill_missing(self._mat, method=None, fill_values=w @ h.T)
            self._sortedmat = self._filledmat.copy()
            self._estimator = self._model.fit_transform(
                self._filledmat.astype(float).values,
                n_bootstrap=self._n_bootstrap,
                sparsity=self._sparsity,
                regularization=self._regularization,
            )
            self._predictor = self._model.predict(self._estimator)
            prec = self.get_precision()
            if verbose:
                print("Error: {0:.0f}%".format(prec))
            self._errors[max(0, itrial - 1)] = prec

        self._error = self._errors[-1]
        self._volume = self._estimator["volume"]

    def is_ok(self):
        return False if not hasattr(self, "_estimator") or not hasattr(self, "_predictor") \
            or self._predictor is None \
            or "H" not in list(self._predictor.keys()) \
            or self._predictor["H"].shape[1] != self._ncomp \
            else True

    @property
    def n_features(self):
        return self._nfeat

    @property
    def n_observations(self):
        return self._nobj

    @property
    def origin_mat(self):
        return self._filledmat

    @property
    def filled_mat(self):
        return self._filledmat

    @property
    def sorted_mat(self):
        return self._sortedmat

    def get_h(self):
        if not self.is_ok():
            self.test_model()
        h = pd.DataFrame(
            index=self._fnames,
            columns=list(["V" + str(x) for x in range(1, self._ncomp + 1)]),
            data=self._predictor["H"],
        )

        return h

    def get_w(self):
        if not self.is_ok():
            self.test_model()
        w = pd.DataFrame(
            index=self._objnames,
            columns=list(["V" + str(x) for x in range(1, self._ncomp + 1)]),
            data=self._predictor["W"],
        )

        return w

    def get_m_proxy(self):
        if not self.is_ok():
            self.test_model()
        whd = self.get_w() @ self.get_h().T
        whd.index = self._mat.index
        whd.columns = self._mat.columns
        return whd

    def get_w_hhi_1(self, do_sort=True):
        if not self.is_ok():
            self.test_model()
        w = self.get_w()
        res = utl.mat_hhi_1(w, axis=0)
        if do_sort:
            res = res.sort_values(by=res.columns[0], axis=0, ascending=False)
        return res

    def get_features_clustering_proba(self):
        if not self.is_ok():
            self.test_model()
        if "HB" in self._estimator:
            return self._estimator["HB"]
        else:
            return np.zeros(self._nfeat)

    def get_observations_clustering_proba(self):
        if not self.is_ok():
            self.test_model()
        if "WB" in self._estimator:
            return self._estimator["WB"]
        else:
            return np.zeros(self._ncomp)

    def get_null_features(self):
        ht = self.get_h().T
        _, to_drop_features = utl.drop_zero_columns(ht)
        return to_drop_features

    def get_fuzzy_features(self, rank=0):
        cols_hhi_1 = self.get_w_hhi_1(do_sort=True)
        # si rank fourni < 0, il est déterminé automatiquement
        # comme l'indice de la plus forte baisse de HHI_1
        if rank < 0:
            delta_hhi_1 = cols_hhi_1.diff(1).iloc[1:]
            rank = np.argmin(delta_hhi_1)
        comp_list = cols_hhi_1.index[:rank+1]
        fuzzy_features = []
        if len(comp_list) > 0:
            ht = self.get_h().T
            for feat in ht.columns:
                maincomp = ht.index[np.argmax(ht.loc[:, feat])]
                if maincomp in comp_list:
                    fuzzy_features.append(feat)
        return fuzzy_features

    def get_stability(self):
        if not self.is_ok():
            self.test_model()
        if "HB" in self._estimator:
            hb = self._estimator["HB"]
            plogp = pd.DataFrame(-np.log(hb) * hb)
            return np.mean(plogp.apply(np.nansum, axis=1)) / np.log(self._nfeat)
        else:
            return 0.0

    def get_precision(self) -> float:
        # if not self.is_ok():
        #         #     self.test_model()
        #         # if 'diff' in self._estimator:
        #         #     return self._estimator['diff'] / mean_square(self._filledmat)
        #         # else:
        #         #     return 0.0
        if not self.is_ok():
            self.test_model()
        m_proxy = self.get_m_proxy()
        m_delta = self._mat - m_proxy
        return utl.mean_square(m_delta) / utl.mean_square(self._mat)

    def get_volume(self) -> float:
        if not self.is_ok():
            self.test_model()
        if "volume" in self._estimator:
            return self._estimator["volume"]
        else:
            return np.nan

    def get_h_compression(self):
        if not self.is_ok():
            self.test_model()
        if "H" in self._estimator:
            h = self.get_h()
            feat_hhi = [utl.hhi_1(h[col]) for col in h.columns]
            mean_hhi = np.mean(feat_hhi)
            return float(self._ncomp) / self._nfeat * (1 + mean_hhi / self._nobj), mean_hhi / self._nfeat
        else:
            return 0.0, 0.0

    def get_dimension_score(self):
        if not self.is_ok():
            self.test_model()
        return self._ncomp / self._nfeat

    def get_parsimony(self) -> float:
        hcomp, _ = self.get_h_compression()
        return hcomp

    def get_target_sparsity(self) -> float:
        return self._sparsity

    def get_effective_dimension(self) -> int:
        _, null_components = utl.drop_zero_columns(self.get_h())
        return self._nfeat - len(null_components)

    def get_sorted_h(self) -> pd.DataFrame:
        h = self.get_h()
        sorted_h = pd.DataFrame(columns=h.columns, index=range(self._nfeat))
        for col in h.columns:
            sorted_h[col] = h.loc[:, col].sort_values(ascending=False).values
        return sorted_h

    def get_interpretability(self, wst=1 / 3.0, wpr=1 / 3.0, wpa=1 / 3.0) -> float:

        st = self.get_stability()
        pr = self.get_precision()
        pa = self.get_parsimony()

        return wst * st + wpr * pr + wpa * pa

    def sort_features_by_cluster(self) -> None:
        feat_clust = pd.DataFrame(columns=self._fnames, index=[1000000])
        if not self.is_ok():
            self.test_model()
        for ic, col in enumerate(feat_clust.columns):
            feat_clust.loc[:, col] = self._predictor["HC"][ic]
        mat_w_clust = pd.concat([self._sortedmat, feat_clust])
        mat_w_clust = mat_w_clust.sort_values(by=1000000, axis=1)
        self._sortedmat = mat_w_clust.drop(1000000, axis=0)

    def get_sorted_features(self):
        return list(self._sortedmat.columns)

    def get_obs_leverage_clusters(self):
        """
        Attribue à chaque ligne de W un cluster dans [1, self._ncomp], en prenant en compte le 'leverage'
        """
        if not self.is_ok():
            self.test_model()
        return pd.DataFrame(index=self._objnames, columns=["Observation Cluster"], data=self._predictor["WC"])

    def get_obs_kmeans_clusters(self, ngroups=0):
        """
        Attribue à chaque ligne de W un cluster dans [1, ngroups], à partir d'une décomposition en K-Means de W
        """
        if not self.is_ok():
            self.test_model()
        wmat = self.get_w()
        ngr = ngroups if ngroups > 0 else self._ncomp
        km = KMeans(ngr)
        return pd.DataFrame(index=self._objnames, columns=["Observation Cluster"], data=km.fit_predict(wmat)+1)

    def get_observations_clusters_incidence_matrix(self, method='leverage', df_clusters_priors=None):
        """
        computes an incidence matrix between the observations clusters given by NMF, and a list of priorly known
        clusters

        Parameters:
            method: ['leverage', 'kmeans']
            df_clusters_priors: a dataframe having the same index as the matrix of current model
        Returns:
            An incidence (c, c) matrix, c being the number of components of the model
        """
        clusters = self.get_obs_leverage_clusters() if method == 'leverage' else \
            self.get_obs_kmeans_clusters() if method == 'kmeans' else None

        if clusters is None or df_clusters_priors is None:
            return None

        return utl.get_clustering_incidence_matrix(clusters, df_clusters_priors)

    def get_nb_misclassified_obs(self, df_clusters_priors, method='leverage'):
        inc_mat = self.get_observations_clusters_incidence_matrix(df_clusters_priors, method)
        utl.make_diagonal_dominant(inc_mat, inplace=True)
        nmis = self._nobj - np.trace(inc_mat)
        return nmis, float(nmis) / self._nobj

    def get_sorted_observations(self):
        return list(self._sortedmat.index)

    def get_observations_clusters_hhi(self):
        df_obs_cl = self.get_obs_leverage_clusters()
        df_count_by_clust = df_obs_cl.groupby("Observation Cluster").size().reset_index(name="counts")
        return utl.hhi_1(df_count_by_clust["counts"].values)

    def get_features_clusters(self):
        if not self.is_ok():
            self.test_model()
        return pd.DataFrame(index=self._fnames, columns=["Feature Cluster"], data=self._predictor["HC"])

    def get_features_clusters_hhi(self):
        df_feat_cl = self.get_features_clusters()
        df_count_by_clust = df_feat_cl.groupby("Features Cluster").size().reset_index(name="counts")
        return utl.hhi_1(df_count_by_clust["counts"].values)

    def sort_observations_by_cluster(self):
        obj_clust = pd.DataFrame(index=self._objnames, columns=["OBJ_CLUSTER"])
        if not self.is_ok():
            self.test_model()
        for ir, row in enumerate(obj_clust.index):
            obj_clust.loc[row, :] = self._predictor["WC"][ir]
        # nf = self._nfeat
        mat_w_clust = pd.concat([self._sortedmat, obj_clust], axis=1)
        mat_w_clust = mat_w_clust.sort_values(by="OBJ_CLUSTER", axis=0)
        self._sortedmat = mat_w_clust.drop("OBJ_CLUSTER", axis=1)

    def get_entropies_by_cluster(self, nbins=10):
        l_clusters = self.get_obs_leverage_clusters()
        c_clusters = self.get_features_clusters()
        return utl.relative_entropy_by_cluster(self._sortedmat, l_clusters, c_clusters, nbins)

    def get_avg_diag_entropies(self, nbins: int = 3,
                               size_weighted: bool = True, relative: bool = False) -> pd.DataFrame:
        omat = self.origin_mat
        m_entropy = utl.normalized_entropy(omat, nbins) if relative else 0.0
        df_entropies, df_sizes = self.get_entropies_by_cluster(nbins)
        df_entropies -= m_entropy
        df_diag_entropies = pd.DataFrame([df_entropies.iloc[i, i] for i in range(len(df_entropies))])
        df_diag_sizes = pd.DataFrame([df_sizes.iloc[i, i] for i in range(len(df_sizes))])
        if size_weighted:
            avg_diag_entropies = (np.sum(df_diag_entropies * df_diag_sizes) /
                                  np.sum(df_diag_sizes)).iloc[0]
        else:
            avg_diag_entropies = np.mean(df_diag_entropies)

        df_avg_diag_entropies = pd.DataFrame(index=[self._name],
                                             data=avg_diag_entropies,
                                             columns=[("Size_weighted_" if size_weighted else "") +
                                                      "avg_diag_entropy"])
        return df_avg_diag_entropies

    def get_features_by_decreasing_loading(self, min_contribution=0.0):
        h = self.get_h()
        sorted_features = pd.DataFrame(columns=h.columns, index=range(self._nfeat))
        for col in h.columns:
            sorted_h = h.sort_values(by=col, ascending=False, inplace=False)
            if min_contribution == 0.0:
                sorted_features.loc[:, col] = h.sort_values(by=col, ascending=False, inplace=False).index.values
            else:
                max_of_loadings = sorted_h.loc[:, col].max()
                for ifeat, feat in enumerate(sorted_h.index):
                    loading = sorted_h.loc[feat, col]
                    contrib = loading / max_of_loadings
                    if loading == 0:
                        contrib = 0
                    elif max_of_loadings == 0.0:
                        contrib = 1000
                    if contrib >= min_contribution:
                        sorted_features.loc[ifeat, col] = feat
                    else:
                        break
        return sorted_features

    def get_row_proba_scores(self):
        w = self.get_w()
        wm = w.apply(np.nansum, axis=1)
        wp = w.div(wm, axis=0)
        nc = self._nfeat
        went = wp.applymap(lambda p: 0 if p == 0.0 else p * math.log(p, 2))
        return 1 + went.apply(np.nansum, axis=1) / math.log(nc, 2)

    def get_specific_cluster_contribution(self):
        row_scores = self.get_row_proba_scores()
        # non standard convention: 0 is the best score (perfect clustering)
        return 1 - np.mean(row_scores)

    def plot_data_heatmap(self, path=None):

        mat = self._sortedmat.astype(float)

        _, _ = plt.subplots(figsize=(int(self._nfeat / 10), int(self._nobj / 100)))
        _ = sns.heatmap(mat, annot=False, linewidths=0, yticklabels=False, cmap="bwr")
        if path is not None:
            plt.gcf().savefig(path)
        plt.show()

    def get_optimal_decomposition_graph(self, n_lower: int, n_upper: int):

        precisions = []
        volumes = []
        ratios = []

        for n in range(n_lower, n_upper+1):
            self.set_ncomp(n)
            self.test_model()
            precision = self.get_precision()
            volume = self.get_volume()
            ratio = precision / volume
            precisions.append(precision)
            volumes.append(volume)
            ratios.append(ratio)

        df = pd.DataFrame({'precision': precisions,
                           'volume': volumes,
                           'ratio': ratios}, index=range(n_lower, n_upper+1))
        return df


    @property
    def errors(self):
        return self._errors

    @property
    def ncomp(self):
        return self._ncomp


def compare_nmf_fs_to_random(train_set: Union[np.ndarray, pd.DataFrame],
                             train_labels: Union[np.ndarray, pd.DataFrame],
                             test_set: Union[np.ndarray, pd.DataFrame],
                             test_labels: Union[np.ndarray, pd.DataFrame],
                             set_name: str = "",
                             ncomp: int = 2,
                             **kwargs
                             ):
    """
    Compares SVC prediction results before and after NMF feature selection
    :param train_set:
    :param train_labels:
    :param test_set:
    :param test_labels:
    :param set_name:
    :param ncomp_range:
    :param kwargs:
    :return:
    """
    svc_model_full = SVC(**kwargs)
    svc_model_full.fit(train_set, train_labels)
    score_train_full = svc_model_full.score(train_set, train_labels)
    score_test_full = svc_model_full.score(test_set, test_labels)

    nmf_model = NmfModel(mat=train_set, ncomp=ncomp, name=set_name, regularization="components")
    nmf_model.set_sparsity(1.0)
    ht = nmf_model.get_h().T
    _, null_features = utl.drop_zero_columns(ht)

    df_x_train_reduced = train_set.drop(null_features, axis=1) \
        if null_features \
        else train_set

    df_x_test_reduced = test_set.drop(null_features, axis=1) \
        if null_features \
        else test_set

    svc_model_reduced = SVC(**kwargs)
    svc_model_reduced.fit(df_x_train_reduced, train_labels)
    score_train_reduced = svc_model_reduced.score(df_x_train_reduced, train_labels)
    score_test_reduced = svc_model_reduced.score(df_x_test_reduced, test_labels)





