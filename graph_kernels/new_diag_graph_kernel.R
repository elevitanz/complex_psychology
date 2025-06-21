# Caricare le librerie necessarie
library(igraph)
library(graphkernels)
library(ggplot2)

folder <- "/Users/ele/Desktop/codici_finali/pcmci+/results_plot_2"
files <- list.files(folder, full.names = TRUE)
filtered_subfolders <- files[grepl("^adj.*_dir\\.csv$", basename(files))]
# Definizione di var_names
var_names <- c("Felt.energetic", "Felt.enthusiastic", "Felt.content", "Felt.irritable",
               "Felt.restless", "Felt.worried", "Felt.worthless.or.guilty",
               "Felt.frightened.or.afraid", "Experienced.loss.of.interest.or.pleasure", 
               "Felt.angry", "Felt.hopeless", "Felt.down.or.depressed",
               "Felt.positive", "Felt.fatigued", "Experienced.muscle.tension", 
               "Had.difficulty.concentrating", "Felt.accepted.or.supported", 
               "Felt.threatened..judged..or.intimidated", "Dwelled.on.the.past", 
               "Procrastinated", "Avoided.people", "Avoided.activities")
graph_list <- list()
individuals <- list()
for (file_name in filtered_subfolders) {
  ind <- substr(file_name, 60,63)
  individuals[[ind]] <- ind
  if (file.exists(file_name)) {
    adj <- read.csv(file_name)
    adj <- adj[ , -which(names(adj) == "X")]
    cat("Elaborazione del file:", file_name, "\n")
    colnames(adj) <- var_names
    g_name <- ind
    graph_list[[g_name]] <- graph_from_adjacency_matrix(as.matrix(adj), mode = "directed", weighted = TRUE)
  }}

# Definizione dei gruppi # HAI TOLTO IL P072
MDD <- c('P014', 'P019', 'P072','P074', 'P137', 'P139', 'P163', 'P169', 'P220', 'P223', 'P244')
GAD_MDD <- c('P001','P003', 'P006', 'P007', 'P008', 'P010', 'P013', 'P048', 'P115', 'P117', 'P203')
GAD <- individuals[!individuals %in% c(MDD, GAD_MDD)]

# Calcolare la matrice di kernel di Weisfeiler-Lehman separatamente per ciascun gruppo

calculate_group_kernel <- function(group, graph_list) {
  # Verifica che tutti gli individui nel gruppo siano presenti in graph_list
  group_graphs <- graph_list[names(graph_list) %in% group]
  
  # Controllo per assicurarci che ci siano grafi corrispondenti
  if (length(group_graphs) == 0) {
    stop("Nessun grafo trovato per il gruppo specificato.")
  }
  
  # Calcola il kernel per il gruppo
  # kernel_matrix <- CalculateWLKernel(group_graphs, 10000)
  degree_vectors <- lapply(group_graphs, degree)
  n_graphs <- length(group_graphs)
  kernel_matrix <- matrix(0, n_graphs, n_graphs)
  for (i in 1:n_graphs) {
    for (j in 1:n_graphs) {
      if (any(degree_vectors[[i]] != 0) || any(degree_vectors[[j]] != 0)) {
        kernel_matrix[i, j] <- sum(degree_vectors[[i]] * degree_vectors[[j]])
      }
    }
  }
  normas <- sqrt(diag(kernel_matrix))
  kernel_mat_norm <- ifelse(outer(normas, normas) == 0, 0, kernel_matrix / outer(normas, normas))
  return(kernel_mat_norm)
}

# Calcolare il kernel per ciascun gruppo
wl_kernel_MDD <- calculate_group_kernel(MDD, graph_list)
wl_kernel_GAD_MDD <- calculate_group_kernel(GAD_MDD, graph_list)
wl_kernel_GAD <- calculate_group_kernel(GAD, graph_list)

# Funzione per visualizzare la heatmap di ogni gruppo
plot_kernel_heatmap <- function(kernel_matrix, group_name) {
  group_size <- ncol(kernel_matrix)
  
  # Creare un data frame per ggplot
  df <- data.frame(
    x = rep(1:group_size, each = group_size),
    y = rep(1:group_size, group_size),
    Value = as.vector(kernel_matrix)
  )
  
  ggplot(df, aes(x = x, y = y, fill = Value)) +
    geom_tile() +  # Crea la mappa
    scale_fill_gradient(low = "white", high = "blue", limits = c(-0.01, 1.01)) +  # Colori per la similarità
    labs(title = paste(''), x = "Individuals", y = "Individuals") +
    theme_minimal() +
    theme(
      axis.text.x = element_blank(),  # Rimuove i numeri dall'asse x
      axis.text.y = element_blank(),  # Rimuove i numeri dall'asse y
      axis.ticks = element_blank()    # Rimuove anche i tick dagli assi (opzionale ma pulito)
    )
}

# Visualizzare le heatmap per ogni gruppo
plot_kernel_heatmap(wl_kernel_MDD, "MDD")
plot_kernel_heatmap(wl_kernel_GAD_MDD, "GAD_MDD")
plot_kernel_heatmap(wl_kernel_GAD, "GAD")

# ggsave(
#   filename = "/Users/ele/Desktop/napoli_acc/dati/4_fisher/Fisher/new_pcmci/gad.png",  # Può essere anche .pdf o .tiff
#   plot = last_plot(),                     # O metti il nome del tuo oggetto grafico se lo hai salvato
#   width = 8, height = 6,                  # Dimensioni in inch (puoi modificare)
#   dpi = 300                               # Alta qualità per stampa o presentazioni
# )

