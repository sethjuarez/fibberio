# fibber
Lib for generating fake data

# Sources
Sources can be either:
1. Pointer to an inline source description
2. A collection of items (`List`)
```
["cat", "dog", "horse"]
[1, 2, 3]
...
```

3. Range description (with optional type `[int, float(precision)]` otherwise inferred)
```
[12000, 32000) -> float   # without type inferred as int
(.01, .9)                 # inferred as float
(25, 45] -> int           # without type inferred as int (unecessary)
(100, 200) -> float(2)    # cast to float with 2 decimal places
```
For reference (helpful for ranges):
- $[a, b]$ the closed interval $\{ x \in \mathbb{R}: a \le x \le b \}$
- $[a, b)$ the interval $\{ x \in \mathbb{R}: a \le x \lt b \}$
- $(a, b]$ the interval $\{ x \in \mathbb{R}: a \lt x \le b \}$
- $(a, b)$ the open interval $\{ x \in \mathbb{R}: a \lt x \lt b \}$

# Distributions
Distributions fall into two categories: discrete and continuous

1. (**Discrete**) The cardinality of discrete probability densities need to match the inherent cardinality of the source classes. For example:
```
{
  "feature": "TabsVSpaces",
  "source": ["tabs", "spaces", "dots"],
  "distribution": [25, 75, 200],
}
```
The `TabsVSpaces` feature has three discrete items in the source. The distributional densities needs to also have a cardinality of 3. These values are normalized in the system and selected using a uniform distribution mapped to the respective densities.

2.  (**Continuous**) Continuous distributions are sampled according to the respective distribution class. For example:
```
distribution_class(1,2, prop1=2, prop2='seismic')
```
will create 'distribution_class' class by extracting `args` as `[1, 2]` and `argsv` as
```
{
  "prop1": 2,
  "prop2": 'seismic'
}
```
and instantiating by:
```
distribution_class(*args, **argsv)
```

## Conditionals

This can change when having a conditional from a continous range source to a discrete range source. Consider the following Feature :
```
{
  "feature": "NumberFeature",
  "source": "(100000, 200000] -> float(2)",
  "distribution": "uniform",
  "conditional": {
    "feature": "subfeature",
    "source": ["carts", "horses", "wheels"],
    "distribution": [
      "(150000, 18000]",
      "[*, 15000)",
      "*"
    ]
  }
}
```
In this case the `NumberFeature` is generated uniformly at random from the interval $\{ x \in \mathbb{R}: 100000 \lt x \le 200000 \}$. When projecting into the discrete conditional distribution we need to scope the original distribution _onto_ the three classes in the conditional. The distribution rules are applied in the order in which they appear with _truthiness_ being a measure of whether the class is selected or not. A `*` indicates a placeholder on either the min, max, or as a catch all.
In this case, as fibber generates a data point if `NumberFeature` fits the first distribution rule, it will also output `carts`. If it fails it proceeds to the next. If this rule is true it will produce `horses`. If none of them fit, then it will proceed to the catch-all and produce `wheels`. If it cannot find a successful match, fibber will throw an exception.

# Task Description
```
{
  "sources": [
    {
      "id": "names",
      "data": "./full_names.csv"
    }
  ],
  "features": [
    {
      "feature": "FirstName,LastName",
      "source": "names",
      "distribution": "uniform"
    },
    {
      "feature": "Age",
      "source": "(14, 85] -> int",
      "distribution:": "normal"
    },
    {
      "feature": "TabsVSpaces",
      "source": ["tabs", "spaces", "dots"],
      "distribution": [25, 75, 200],
      "conditional": {
        "feature": "subtabspaces",
        "source": "[12, 59] -> float(2)",
        "distribution": ["uniform", "normal(0.2)", "normal(12.2, 0.5)"]
      }
    },
    {
      "feature": "ScrumVAgile",
      "source": ["scrum", "agile"],
      "distribution": [25, 75],
      "conditional": {
        "feature": "subfeature",
        "source": ["cheese", "pepper", "macaroni", "pretzels"],
        "distribution": [
          [0, 0, 2, 20], 
          [10, 20, 2, 1]
        ],
        "conditional": {
          "feature": "subsubfeature",
          "source":"(100000, 200000] -> float",
          "distribution": [
            "uniform",
            "normal(0.2)",
            "uniform",
            "normal(.01)"
          ]
        }
      }
    },
    {
      "feature": "NumberFeature",
      "source": "(100000, 200000] -> float(2)",
      "distribution": "uniform",
      "conditional": {
        "feature": "subfeature",
        "source": ["carts", "horses", "wheels"],
        "distribution": [
          "(150000, 18000]",
          "[*, 15000)",
          "*"
        ],
        "conditional": {
          "feature": "subsubfeature",
          "source":"(100000, 200000]->float",
          "distribution": [
            "uniform",
            "normal(0.2)",
            "uniform",
            "normal(.01)"
          ]
        }
      }
    }
  ]
}
```