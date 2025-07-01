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

# Simple statistics - using the appropriate method for aggregations
print("\nPrice Statistics:")
stats_df = df.agg(
    [daft.col("price").min().alias("min_price"),
     daft.col("price").max().alias("max_price"),
     daft.col("price").mean().alias("avg_price"),
     daft.col("price").count().alias("count")]
)
stats_df.show()

# Show count of products by in-stock status
print("\nProduct count by in-stock status:")
in_stock_counts = df.groupby("in_stock").agg(daft.col("product").count().alias("count"))
in_stock_counts.show()
