import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_revenue_influence(numeric_results, categorical_results):

    if numeric_results:
        plt.figure(figsize=(10,6))
        attrs = [r['attribute'] for r in numeric_results]
        corrs = [r['pearson_corr'] for r in numeric_results]
        sns.barplot(x=attrs, y=corrs, palette='viridis')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Pearson korelacija sa Revenue 24h')
        plt.title('Uticaj numeričkih atributa na profitabilnost')
        plt.tight_layout()
        plt.show()

    if categorical_results:
        plt.figure(figsize=(8,5))
        attrs = [r['attribute'] for r in categorical_results]
        p_values = [r['p_value'] for r in categorical_results]
        neg_log_p = [-np.log10(p) if p>0 else 0 for p in p_values]
        sns.barplot(x=attrs, y=neg_log_p, palette='magma')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('-log10(p) vrednost ANOVA testa')
        plt.title('Uticaj kategorijskih atributa na profitabilnost')
        plt.tight_layout()
        plt.show()
