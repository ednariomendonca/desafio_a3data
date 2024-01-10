import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

class MyFunctions:
    
    # Função para obtenção do gráfico de barras simples
    
    def bar_plot(self, var, df, title = None, xlabel = None):
        if xlabel == None:
            xlabel = var

        pct = df[var].value_counts(normalize = True) * 100

        plt.figure(figsize = (6, 4))
        sns.barplot(x = pct.index, y = pct.values)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel('%')
        plt.ylim(0, 100)

        for i, percentage in enumerate(pct):
            plt.text(i, percentage + 1, f'{percentage:.2f}%', ha = 'center', va = 'bottom')

        plt.show()
        
    # Função para obtenção do gráfico de barras empilhado
        
    def stacked_bar(self, var, group, df, title = None, ylabel = '', legend_title = None, position = (1.2, 1)):
        ct = pd.crosstab(df[var], df[group], normalize = 'index') * 100
        ct = ct.reset_index().set_index(var).rename_axis(None, axis = 1).reset_index()

        ax = ct.plot( 
            x = var,  
            kind = 'barh',  
            stacked = True,  
            title = title,  
            mark_right = True, 
            ylabel = ylabel, 
            xlabel = '%'
        ) 

        df_freq = ct[ct.columns[1:]].div(100, 0) * 100

        for n in df_freq: 
            for i, (cs, ab, pc) in enumerate(zip(ct.iloc[:, 1:].cumsum(1)[n], ct[n], df_freq[n])): 
                plt.text(cs - ab / 2, i, str(np.round(pc, 1)) + '%', va = 'center', ha = 'center')

        ax.get_legend().remove()

        handles, labels = ax.get_legend_handles_labels()

        if legend_title != None:
            legend = ax.legend(handles, labels, loc = 'upper right', bbox_to_anchor = position, title = legend_title)
        else:
            leggend = ax.legend(handles, labels, loc = 'upper right', bbox_to_anchor = position, title = group)
            
    # Função para realização do teste Qui-Quadrado
            
    def chi2_test(self, var1, var2, df):
        contingency_table = pd.crosstab(df[var1], df[var2])
        chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
        chi2 = round(chi2, 3)
        p_value = round(p_value, 3)

        if p_value < 0.001:
            p_value = '< 0.001'

        return print(f'########## Resultados do Teste ########## \n\nEstatística Chi2: {chi2} \np-valor: {p_value}')
    
    # Função para realização do teste t considerando amostras independentes

    def t_test(self, df, quantitative_col, categorical_col):
        category_name_0 = df[categorical_col].unique()[0]
        category_name_1 = df[categorical_col].unique()[1]

        x1 = df[df[categorical_col] == category_name_0][quantitative_col].dropna()
        x2 = df[df[categorical_col] == category_name_1][quantitative_col].dropna()

        descriptives = pd.DataFrame({ 
            'n': [len(x1), len(x2)], 
            'min': [round(x1.min(), 3), round(x2.min(), 3)], 
            'q1': [round(x1.quantile(0.25), 3), round(x2.quantile(0.25), 3)],
            'mean': [round(x1.mean(), 3), round(x2.mean(), 3)], 
            'median': [round(x1.quantile(0.5), 3), round(x2.quantile(0.5), 3)], 
            'q3': [round(x1.quantile(0.75), 3), round(x2.quantile(0.75), 3)],
            'sd': [round(x1.std(), 3), round(x2.std(), 3)], 
            'max': [round(x1.max(), 3), round(x2.max(), 3)],
        }, index = [category_name_0, category_name_1])

        t_stat, p_value = stats.ttest_ind(x1, x2)
        t_stat = round(t_stat, 3)
        p_value = round(p_value, 3)

        if p_value < 0.001:
            p_value = '< 0.001'

        return print(f'########## Medidas Descritivas ########## \n\n {descriptives} \n\n\n########## Resultados do Teste ########## \n\nEstatística t: {t_stat} \np-valor: {p_value}')