# GC4PhysicalConstants

Genetic computing for physical constants.

This repository contains analytic snippets created from generic computation  for future AI processing to identify patterns and relationships between fundamental constants.
The data are stored as txt and json files. 

If you use these data with analytic functions, please cite this work as:

 "Discovering the underlying analytic structure within Standard Model  constants using artificial intelligence"
  S. V. ~Chekanov and H.Kjellerstrand, HEP-ANL-197373, June 26, 2025. aXiv (link will be provided)

# Instruction

Here is how you can use the files uploaded to this repository. All analytic expressions up to the rank 70 are orginized as a dictionary stored in the JSON file. Here is the exmple how to read such files:


```
import gzip,json
jsonfilename="standard_model_snippets.json.gz"
with gzip.open(jsonfilename, 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))
```

Here "data" is a dictionary with the key=6 ... 70 representing analytic ranks. The dictionary values for a given key are lists which are orginized like this:

```
[equation,error,predicted,target]
```
where "equation" is a symbolic equation, "error" is uncertainty (expressed in  percent), "predicted" is the predicted value and "target" is the target value. 



S. V. ~Chekanov nad H.Kjellerstrand

