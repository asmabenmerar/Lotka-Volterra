import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Charger les données réelles à partir du fichier CSV
csv_path = "C:/Users/asmab/Documents/projets_hetic/Mathematique/test/populations_lapins_renards.csv"
csv = pd.read_csv(csv_path)

# Vérifier les colonnes du CSV
print("Colonnes disponibles :", csv.columns)

# Extraire les colonnes nécessaires
time_real = csv['date'].values  # La colonne pour le temps
lapin_real = csv['lapin'].values  # La colonne pour les lapins
renard_real = csv['renard'].values  # La colonne pour les renards

# Définir la fonction MSE
def mse(real, predicted):
    return np.mean((real - predicted) ** 2)

# Fonction de simulation du modèle Lotka-Volterra
def simulate_lotka_volterra(alpha, beta, delta, gamma, step, iterations):
    time = [0]
    lapin = [1]
    renard = [2]

    for _ in range(iterations):
        new_time = time[-1] + step
        new_lapin = lapin[-1] + step * (lapin[-1] * (alpha - beta * renard[-1]))
        new_renard = renard[-1] + step * (renard[-1] * (delta * lapin[-1] - gamma))
        
        time.append(new_time)
        lapin.append(new_lapin)
        renard.append(new_renard)

    return np.array(time), np.array(lapin) * 1000, np.array(renard) * 1000

# Paramètres à tester
param_values = [1 / 3, 2 / 3, 1, 4 / 3]
best_mse = float('inf')
best_params = None

# Grid search pour trouver les meilleurs paramètres
for alpha_try in param_values:
    for beta_try in param_values:
        for delta_try in param_values:
            for gamma_try in param_values:
                # Simulation
                time, lapin_pred, renard_pred = simulate_lotka_volterra(
                    alpha_try, beta_try, delta_try, gamma_try, step=0.001, iterations=100_000
                )

                # Calcul des erreurs
                mse_lapin = mse(lapin_real, lapin_pred[:len(lapin_real)])
                mse_renard = mse(renard_real, renard_pred[:len(renard_real)])
                total_mse = mse_lapin + mse_renard

                # Mise à jour des meilleurs paramètres
                if total_mse < best_mse:
                    best_mse = total_mse
                    best_params = (alpha_try, beta_try, delta_try, gamma_try)

# Résultats optimaux
alpha_opt, beta_opt, delta_opt, gamma_opt = best_params
print(f"Meilleurs paramètres : alpha={alpha_opt}, beta={beta_opt}, delta={delta_opt}, gamma={gamma_opt}")
print(f"Erreur quadratique moyenne totale : {best_mse:.4f}")

# Simulation avec les meilleurs paramètres
time, lapin, renard = simulate_lotka_volterra(alpha_opt, beta_opt, delta_opt, gamma_opt, step=0.001, iterations=100_000)

# Affichage des données réelles et des prédictions
plt.figure(figsize=(15, 6))
plt.plot(time, lapin, "b-", label="Lapins (Modèle)")
plt.plot(time, renard, "r-", label="Renards (Modèle)")
plt.scatter(time_real, lapin_real, color="blue", label="Lapins (Données réelles)", s=10)
plt.scatter(time_real, renard_real, color="red", label="Renards (Données réelles)", s=10)
plt.xlabel('Temps (Mois)')
plt.ylabel('Population')
plt.legend()
plt.title("Simulation du modèle Lotka-Volterra avec paramètres optimisés")
plt.show()
