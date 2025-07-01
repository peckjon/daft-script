# Daft.ai Script Runner

A GitHub Action for running [Daft.ai](https://daft.ai/) scripts. Daft is a fast and scalable data engine for complex data processing across any modality.

## What is Daft.ai?

Daft is a modern, Python-native library designed for complex and multi-modal datasets. It's built to handle various data types including text, images, audio, and videos with high performance. Daft supports lazy evaluation and is optimized for distributed computing and data processing, with SQL and Python DataFrame interfaces as first-class citizens.

## Usage

This action sets up a Python environment with the Daft.ai library and runs your script. You can provide either a script file path or the script content directly.

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
          scriptfile: 'scripts/process_data.py'
```

## Inputs

### `scriptfile`

**Optional** Path to a Python script file that imports and uses the Daft library.

### `script`

**Optional** Content of a Python script that imports and uses the Daft library.

**Note:** You must provide either `scriptfile` OR `script`, but not both.

## Example Scripts

### Example script file (process_data.py)

```python
import daft

# Create a DataFrame from a dictionary
df = daft.from_pydict({
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "age": [25, 30, 35, 40, 45],
    "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "active": [True, False, True, True, False],
})

# Perform some operations
result = df.where(daft.col("age") > 30).select("name", "age", "city")

# Show the results
print("Results:")
result.show()
```

### Example using script content input

```yaml
- name: Run Daft script
  uses: your-username/daft-script@v1
  with:
    script: |
      import daft
      
      # Set up anonymous access to demo data
      daft.set_planning_config(default_io_config=daft.io.IOConfig(s3=daft.io.S3Config(anonymous=True)))
      
      # Read a sample dataset
      df = daft.read_parquet("s3://daft-public-data/tutorials/10-min/sample-data-dog-owners-partitioned.pq/**")
      
      # Process data
      result = df.where(daft.col("has_dog") == True).select("first_name", "last_name", "country")
      
      # Show results
      print("Dog owners:")
      result.show()
```

## Additional Resources

- [Daft Documentation](https://docs.getdaft.io/)
- [Quickstart Guide](https://docs.getdaft.io/en/stable/quickstart/)
- [Core Concepts](https://docs.getdaft.io/en/stable/core_concepts/)
- [API Reference](https://docs.getdaft.io/en/stable/api/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
