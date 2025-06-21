# Caricare le librerie necessarie
library(igraph)
library(graphkernels)
library(ggplot2)

folder <- "/Users/ele/Desktop/codici_finali/pcmci+"
files <- list.files(folder, full.names = TRUE)
filtered_subfolders <- files[grepl("^0y1_count_.*\\.csv$", basename(files))]

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
groups <- list()
for (file_name in filtered_subfolders) {
  group <- substr(file_name,51,57)
  #group <- substr(file_name,73,79)
  groups[[group]] <- group
  if (file.exists(file_name)) {
    adj <- read.csv(file_name)
    adj <- adj[ , -which(names(adj) == "X")]
    adj[is.na(adj)] <- 0
    cat("Elaborazione del file:", file_name, "\n")
    colnames(adj) <- var_names
    g_name <- group
    graph_list[[g_name]] <- graph_from_adjacency_matrix(as.matrix(adj), mode = "directed", weighted = TRUE)
  }}
# Ordina i grafi in base a un ordine personalizzato (per esempio, puoi usare una lista di etichette personalizzate)
ordered_groups <- c("GAD.csv", "MDD.csv", "GAD_MDD")  # Lista personalizzata di individui in ordine desiderato

# Riordina la lista dei grafi in base all'ordine di `ordered_individuals`
ordered_graph_list <- graph_list[ordered_groups]

# Calcolare la matrice di similarità per i grafi ordinati
kernel_mat <- CalculateWLKernel(ordered_graph_list, 500)
#kernel_mat <- CalculateVertexHistKernel(ordered_graph_list)
# degree_vectors <- lapply(graph_list, degree)
# n_graphs <- length(graph_list)
# kernel_mat <- matrix(0, n_graphs, n_graphs)
# for (i in 1:n_graphs) {
#   for (j in 1:n_graphs) {
#     kernel_mat[i, j] <- sum(degree_vectors[[i]] * degree_vectors[[j]])
#   }
# }
normas <- sqrt(diag(kernel_mat))
kernel_mat_norm <- kernel_mat / outer(normas, normas)
print(kernel_mat_norm)
groups_list <- c("GAD", "MDD", "GAD_MDD")
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
    geom_tile() +
    scale_fill_gradient(low = "white", high = "blue", limits = c(-0.01, 1.01)) +
    scale_x_continuous(breaks = c(1, 2, 3), labels = c("GAD", "MDD", "Comorbidity")) +
    scale_y_continuous(breaks = c(1, 2, 3), labels = c("GAD", "MDD", "Comorbidity")) +
    labs(title = paste(''), x = "Diagnoses", y = "Diagnoses") +
    theme_minimal() +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      axis.ticks = element_blank()
    )
  
    #theme(axis.text.x = element_text(angle = 90, hjust = 1))  # Ruota le etichette per chiarezza
}

# Visualizzare le heatmap per ogni gruppo
plot_kernel_heatmap(kernel_mat_norm, "fusion")
