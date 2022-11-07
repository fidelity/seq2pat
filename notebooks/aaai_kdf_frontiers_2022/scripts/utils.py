import os
from datetime import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def log_msg(message):
    """
    Print message with timestamp.
    """
    print(datetime.now(), ": ", message)
    
    
def precision_reall_f1_report(precision, recall, thresholds, 
                              plot=True, 
                              figsize=(12,8),
                              font_scale=2,
                              linewidth=2):
    reports = pd.DataFrame()
    reports['precision'] = precision[0:-1]
    reports['recall'] = recall[0:-1]
    reports['threshold'] = thresholds
    reports['f1'] = 2 * reports['precision'] * reports['recall'] / (reports['precision'] + reports['recall'])
    
    results = []
    for i, row in reports.iterrows():
        for metric in ['precision', 'recall', 'f1']:
            results.append({'threshold': row['threshold'],
                            'metric': metric,
                            'value': row[metric]})
    
    df = pd.DataFrame(results)
    # Plot
    if plot:
        plt.figure(figsize=figsize)

        rc={'font.weight' : 'bold',
            'axes.linewidth' : linewidth,
            'axes.edgecolor' : 'k'}
        sns.set(style='whitegrid', font_scale=font_scale, rc=rc) 
        
        ax = sns.lineplot(data=df, x="threshold", y="value", hue="metric", 
                          style='metric', linewidth=linewidth)
        ax.set_xlabel('threshold', fontweight='bold')
        ax.set_ylabel('value', fontweight='bold')
        
    return reports