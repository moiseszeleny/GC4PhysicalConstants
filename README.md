# GC4PhysicalConstants

**Genetic Computing for Physical Constants**

This repository contains analytic snippets generated through generic computation for future AI-based analysis. The goal is to identify patterns and relationships between fundamental physical constants.

The data are stored in `.txt` and `.json` file formats.

If you use these data with analytic functions, please cite the following work:

> **"Discovering the Underlying Analytic Structure within Standard Model Constants Using Artificial Intelligence"**  
> S. V. Chekanov and H. Kjellerstrand, HEP-ANL-197373, June 26, 2025.  
> *arXiv* (link will be provided)

---

## Instructions

### How to Use the Files in This Repository

All analytic expressions up to rank 70 are organized in a dictionary and stored in a compressed JSON file. Here's an example of how to read such files:

```python
import gzip
import json

jsonfilename = "standard_model_snippets.json.gz"
with gzip.open(jsonfilename, 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))
```


Here "data" is a dictionary with the key=6 ... 70 representing analytic ranks. The dictionary values for a given key are lists which are orginized like this:

```
[equation,error,predicted,target]
```
where "equation" is a symbolic equation, "error" is uncertainty (expressed in  percent), "predicted" is the predicted value and "target" is the target value. 
All duplicate entries have been removed. There are no precision constraints applied, i.e., |predicted - target| is always within the uncertainty of the target value as defined by the Standard Model.


S. V. Chekanov nad H.Kjellerstrand

