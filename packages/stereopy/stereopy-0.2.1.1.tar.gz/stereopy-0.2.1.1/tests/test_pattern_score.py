from stereo.core.stereo_exp_data import StereoExpData
from anndata import AnnData
import numpy as np
import time
import pandas as pd
import statistics
import scipy.stats as stats
from tqdm import tqdm


def get_enrichment_score(gene_expression):
    """
    calculate enrichment score E10 and C50.

    :param gene_expression: expression data for the input gene
    :return: list of gene name, E10 score, C50 score and total MID counts of input gene
    """
    gene_expression = gene_expression[gene_expression > 0]
    gene_expression = gene_expression.sort_values(ascending=False).reset_index(drop=True)
    count_list = gene_expression.values
    total_count = np.sum(count_list)
    e10 = np.around(100 * (np.sum(count_list[:int(len(count_list) * 0.1)]) / total_count), 2)
    cdf = np.cumsum(count_list)
    count_fraction_list = cdf / total_count
    c50 = np.around((next(idx for idx, count_fraction in enumerate(count_fraction_list) if count_fraction > 0.5)
                     / len(count_fraction_list)) * 100, 2)
    return e10, c50, total_count

test_exp = 'D:\projects\data\sem.csv'

data = pd.read_csv(test_exp, index_col=[0]).dropna()
data = data.loc[:, (data != 0).any(axis=0)]
se = StereoExpData(exp_matrix=data.values, cells=data.index, genes=data.columns)


print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# report = get_enrichment_score(se.exp_matrix.T)
d = pd.DataFrame(se.exp_matrix, columns=se.gene_names, index=se.cell_names)
tqdm.pandas(desc="calculating enrichment score")
report = d.progress_apply(get_enrichment_score, axis=0)
report = report.T.reset_index()
report.columns = ['gene', 'e10', 'c50', 'total_count']
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


