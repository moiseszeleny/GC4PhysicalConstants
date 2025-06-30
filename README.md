# GC4PhysicalConstants

**Genetic Computing for Physical Constants**

This repository contains analytic snippets generated through generic computation for future AI-based analysis. The goal of this data is to identify patterns and relationships between fundamental physical constants. They data surve as the inputs for several AI techniques to be deployed for the analysis of the topological structure that may reflect the underlying connections in high-dimensional functional space.

> Note: The file will be public only after the paper will be visible in the public domain.


If you use these data with analytic functions, please cite the following work:

> **"Discovering the Underlying Analytic Structure within Standard Model Constants Using Artificial Intelligence"**  
> S. V. Chekanov and H. Kjellerstrand, HEP-ANL-197373, June 26, (2025).  
> *arXiv* (link will be provided)

---

## How to Use the Files in This Repository

All analytic expressions up to rank 70 are organized in a dictionary and stored in a compressed JSON file. Here's an example of how to read such files:

```python
import gzip
import json

jsonfilename = "standard_model_snippets.json.gz"
with gzip.open(jsonfilename, 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))
```
Here, ```data``` is a dictionary where the keys range from 6 to 70, representing analytic ranks. Each value associated with a key is a list structured as follows:

```
[equation,error,predicted,target]
```
where "equation" is the symbolic equation (using the notation close to LaTeX), "error" is the obtained uncertainty (expressed as a percentage), "predicted" is the predicted value, and 
"target" is the actual value of the constant.  All duplicate entries have been removed. There are no precision constraints applied as in the original publication, i.e., |predicted - target| is always within the uncertainty of the target value as defined by the Standard Model.

S. V. Chekanov and H.Kjellerstrand, 
June 2025

