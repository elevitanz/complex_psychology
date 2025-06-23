# complex_psychology
This repository is related to the study: Vitanza, E., De Lellis, P., Mocenni, C., Marin, M.R., Complex Dynamics in Psychological Data: Mapping Individual Symptom Trajectories to Group-Level Patterns. If you use this code please cite the article.

'dataset' folder contains:
- 'general_data.py', the python code used to merge and normalize the individual data collected from: Fisher, A. J., Reeves, J. W., Lawyer, G., Medaglia, J. D., & Rubel, J. A. (2017). Exploring the idiographic dynamics of mood and anxiety via network analysis. Journal of abnormal psychology, 126(8), 1044.
- 'general_data.csv', the final dataset used in the PCMCI+ application.
- 'diagnosis.txt', diagnosis list from Fisher et al., 2017.
- 'readme.docx', a read me file with some information on data collection from Fisher et al., 2017.

'PCMCI+' folder contains:
- 'pcmci+_parallelizzato.py', the python code used to obtain individual causal networks through PCMCI+ algorithm.
- Folder 'results', containing the individual adjacency matrices (either directed or weighted, lag-0 or lag-1).
- 'pcmci+_plots.py', the python code used to obtain the final layout of causal graphs.
- Folder 'results_plot', containing the final images of individual causal networks.
- Folder 'results_plot_2', containing the individual adjacency matrices considering both lag-0 and lag-1 at the same time (either directed or weighted).
- 'fusion.py', the python code used to aggregate individual networks by diagnosis.
- Foder 'results_fusion', containing the global adjacency matrices (either directed or undirected).
- Foder 'results_fusion_2', containing the final fusion networks for GAD, MDD and comorbidity.

'network_metrics' folder contains:
