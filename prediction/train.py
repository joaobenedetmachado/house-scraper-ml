import pandas as pd
from utils import train_price_models

df = pd.read_csv('data/processed/data.csv')

X = df[['nquartos','nbanheiros','ngaragem']]
y = df['preco']


models = train_price_models(X, y)

print("\nas dos modelos:")
print(f"- Linear Regression -> R²: {models['linear_regression']['r2']:.2f}, MSE: {models['linear_regression']['mse']:.2f}")
print(f"- Random Forest    -> R²: {models['random_forest']['r2']:.2f}, MSE: {models['random_forest']['mse']:.2f}")

while True:
    try:
        nquartos = int(input("n quartos: "))
        nbanheiros = int(input("n banheiros: "))
        ngaragem = int(input("n garagem: "))
    except ValueError:
        print("somente numeros validos!\n")
        continue

    features = [[nquartos, nbanheiros, ngaragem]]

    lr_price = models['linear_regression']['model'].predict(features)[0]
    rf_price = models['random_forest']['model'].predict(features)[0]

    print(f"\precos estimado:")
    print(f"- Linear Regression: R$ {lr_price:,.2f}")
    print(f"- Random Forest:    R$ {rf_price:,.2f}\n")
