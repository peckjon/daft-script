import daft

# Print Daft version for information
print(f"Using Daft version: {daft.__version__}")

# Create a simple DataFrame
df = daft.from_pydict({
    "product": ["Laptop", "Phone", "Tablet", "Monitor", "Headphones"],
    "price": [1200, 800, 350, 400, 150],
    "in_stock": [True, False, True, True, True],
    "rating": [4.5, 4.8, 3.9, 4.2, 4.7],
})

# Filter for products that are in stock
in_stock_df = df.where(daft.col("in_stock") == True)

# Sort by price in descending order
sorted_df = in_stock_df.sort(daft.col("price"), desc=True)

# Select columns of interest and add a discount column
result_df = sorted_df.with_column(
    "discounted_price", 
    daft.col("price") * 0.9
).select("product", "price", "discounted_price", "rating")

# Show the results
print("Products in stock (sorted by price):")
result_df.show()

# Simple statistics without using rating ranges
print("\nPrice Statistics:")
try:
    stats = df.select([
        daft.col("price").min().alias("min_price"),
        daft.col("price").max().alias("max_price"),
        daft.col("price").mean().alias("avg_price"),
        daft.col("price").count().alias("count")
    ])
    stats.show()
except Exception as e:
    print(f"Error calculating statistics: {e}")
    
    # Fallback to simpler statistics
    min_price = df.select(daft.col("price").min()).collect()[0][0]
    max_price = df.select(daft.col("price").max()).collect()[0][0]
    avg_price = df.select(daft.col("price").mean()).collect()[0][0]
    count = df.select(daft.col("price").count()).collect()[0][0]
    
    print(f"Min price: {min_price}")
    print(f"Max price: {max_price}")
    print(f"Avg price: {avg_price}")
    print(f"Count: {count}")
