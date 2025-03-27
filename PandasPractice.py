import pandas as pd

fruits = []
colors = []

print("Enter 5 fruits and their colors\n")

for i in range(1, 6):
    fruit = input(f"Enter fruit {i} name: ")
    color = input(f"Enter color of {fruit}: ")
    fruits.append(fruit)
    colors.append(color)
    print()

df = pd.DataFrame({
    'Fruit': fruits,
    'Color': colors
})

clean_df = df.dropna()

clean_df.to_csv('fruits.csv', index=False)

print("Data saved to 'fruits.csv'")
print("\nYour data:")
print(df)