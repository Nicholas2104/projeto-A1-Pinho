import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ler o arquivo CSV
crashes = pd.read_csv("dados/Motor_Vehicle_Collisions_-_Crashes_20241008.csv")

# Converter a coluna de datas para o formato datetime
crashes["CRASH DATE"] = pd.to_datetime(crashes["CRASH DATE"], format="%m/%d/%Y")

# Criar uma nova coluna para o mês (apenas o mês, sem o ano)
crashes["MONTH"] = crashes["CRASH DATE"].dt.month_name()

# Filtrar os dados para acidentes causados por álcool e drogas
drugs = ["Drugs (Illegal)", "Drugs (illegal)"]
alcohol = ["Alcohol Involvement"]

crashes_by_drugs = crashes[crashes["CONTRIBUTING FACTOR VEHICLE 1"].isin(drugs)]
crashes_by_alcohol = crashes[crashes["CONTRIBUTING FACTOR VEHICLE 1"].isin(alcohol)]

# Agrupar os dados por mês e contar o número de acidentes para cada categoria
drug_accidents = crashes_by_drugs.groupby("MONTH").size().reset_index(name='Drug Accidents')
alcohol_accidents = crashes_by_alcohol.groupby("MONTH").size().reset_index(name='Alcohol Accidents')

# Mesclar os DataFrames
merged = drug_accidents.merge(alcohol_accidents, on="MONTH", how="outer")
merged = merged.fillna(0)  # Substituir NaN por 0

# Ordenar os meses cronologicamente
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
merged["MONTH"] = pd.Categorical(merged["MONTH"], categories=month_order, ordered=True)
merged = merged.sort_values(by="MONTH")

# Reorganizar os dados para o gráfico de barras lado a lado
melted = pd.melt(merged, id_vars=["MONTH"], value_vars=["Drug Accidents", "Alcohol Accidents"], var_name="Type", value_name="Count")

# Plotar o gráfico de barras lado a lado
f, ax = plt.subplots(figsize=(12, 6))

# Plotar as barras lado a lado
sns.barplot(x="MONTH", y="Count", hue="Type", data=melted, palette={"Drug Accidents": "r", "Alcohol Accidents": "g"})

# Ajustar o gráfico
ax.legend(ncol=1, loc="upper right", frameon=True)
sns.despine(left=True, bottom=True)
plt.xticks(rotation=45)
plt.title("Number of Accidents by Month (Drugs and Alcohol)")
plt.xlabel("Month")
plt.ylabel("Number of Accidents")
plt.show()