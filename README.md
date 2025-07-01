# Daft.ai GitHub Action

A GitHub Action for running [Daft.ai](https://daft.ai/) scripts. Daft is a fast and scalable data engine for complex data processing across any modality.

## What is Daft.ai?

Daft is a modern, Python-native library designed for complex and multi-modal datasets. It's built to handle various data types including text, images, audio, and videos with high performance. Daft supports lazy evaluation and is optimized for distributed computing and data processing, with SQL and Python DataFrame interfaces as first-class citizens.

### Example workflow

```yaml
name: Run Daft Data Processing

on: [push]

jobs:
  process-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Daft script from file
        uses: peckjon/daft-script@v1
        with:
          script_file: 'scripts/process_data.py'
          # Optional: specify a specific Daft version
          # daft_version: '0.5.7'
      - name: Optionally, show script output in Job Summary (always shown in log)
        run: |
          echo "${{ steps.run_script.outputs.result }}" >> $GITHUB_STEP_SUMMARY
```

## Inputs

### `script_file`

**Required** Path to a Python script file that imports and uses the Daft library.

### `daft_version`

**Optional** Version of Daft to install (e.g., '0.2.0'). If not specified, the latest version will be installed.

> **Note:** Only the `script_file` parameter is supported. Inline script content via a `script` parameter is no longer available.

## Example Scripts

### Example script file (`process_data.py`)

```python
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
in_stock_counts = df.groupby("in_stock").count()
in_stock_counts.show()
```

## Additional Resources

- [Daft Documentation](https://docs.getdaft.io/)
- [Quickstart Guide](https://docs.getdaft.io/en/stable/quickstart/)
- [Core Concepts](https://docs.getdaft.io/en/stable/core_concepts/)
- [API Reference](https://docs.getdaft.io/en/stable/api/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details