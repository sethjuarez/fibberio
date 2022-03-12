# fibber

Teaching machine learning things is hard. The idea behind this library is to generate data in such a way that certain principles can be highlighted without resorting to "finding" the perfect dataset to do so.

Once the library is installed in your python environment, you can start generating data by:

```
fibber -t .\tests\data\programmers.json -o .\sandbox\programmers.csv -c 10000
```

where `-t` is the Task Description file and `-o` is the output file. To specify the record count, the `-c` flag is used. Successfully running the command should show the following:

```
Generating 10000 items using "programmers.json"
-----------------------------------------------

       FirstName  LastName           age  style          desc accept
count      10000     10000  10000.000000  10000  10000.000000  10000
unique       966      1000           NaN      2           NaN      2
top         Remy  Anthony            NaN   tabs           NaN  False
freq          29        21           NaN   6642           NaN   5378
mean         NaN       NaN     35.985700    NaN     21.736883    NaN
std          NaN       NaN      4.983832    NaN     10.526532    NaN
min          NaN       NaN     18.000000    NaN      5.010000    NaN
25%          NaN       NaN     33.000000    NaN     12.580000    NaN
50%          NaN       NaN     36.000000    NaN     20.070000    NaN
75%          NaN       NaN     39.000000    NaN     34.660000    NaN
max          NaN       NaN     57.000000    NaN     36.800000    NaN

Saving csv to C:\projects\fibberio\sandbox\programmers.csv
Task complete
```

The [programmers.json](./tests/data/programmers.json) file is a good starting point for understanding task descriptions.

# Task Description

The best way to understand how it works is to look at a task description:

```json
{
  "sources": {
    "names": {
      "path": "./full_names.csv",
      "read_csv": {
        "encoding": "unicode_escape",
        "engine": "python"
      }
    }
  },
  "features": {
    "FirstName": {
      "source": {
        "id": "names",
        "target": "FirstName"
      }
    }
    "age": {
      "normal": {
        "mean": 36,
        "stddev": 5,
        "precision": 0
      }
    },
    "style": {
      "discrete": {
        "tabs": 2,
        "spaces": 1
      }
    }
  }
}
```

There are two specific sections:

1. **Sources** - external reference data
2. **Features** - columns to generate

## Sources

The `sources` section contains a dictionary containing references to external files with data that can be sampled later as features.

```json
{
    "key": {
        "path": "path_to_file",
        "read_csv": {
            "encoding": "unicode_escape",
            "engine": "python"
        }
    }
}
```

The `key` is the identifier used to reference this data source later in the features. [`read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) in this case is the call to the pandas [`read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) function call with the enclosed dictionary representing the `**kwargs` passed to that function. In theory, any pandas call to load any file type can be used here (although as of the time of this writing, `read_csv` is the only one that has been tried).

## Features

The `features` section contains the features the system should generate along with their corresponding distributions:

```json
  "features": {
    "FirstName": {
      "source": {
        "id": "names",
        "target": "FirstName"
      }
    },
    "age": {
      "normal": {
        "mean": 36,
        "stddev": 5,
        "precision": 0
      }
    },
    "style": {
      "discrete": {
        "tabs": 2,
        "spaces": 1
      }
    }
  }
```

In this example there are exactly three features:

1. **FirstName** - this references the `names` source and samples from the `FirstName` column
2. **age** - this samples from the `normal` distribution with three parameters passed in to the `Normal` class as `**kwargs`
3. **style** - this samples from a discrete distribution that will generate `tabs` and `spaces` in a 2 to 1 ratio

The standard definition for a feature therefore consists of:

```json
{
  "feature_id": {
    "distribution_class": {
      [... distribution args ...]
    },
    "conditional": {
      [... optional conditional feature generator ...]
    }
  }
}
```

Where the `feature_id` represents the id of the feature and the column name (this can be overriden in certain samplers). The `distribution_class` is the name of a `Distribution` class which is instantiated with the corresponding args.

Essentially, if the Distribution class is instantiated by:

```
distribution_class(prop1=2, prop2=seismic)
```

then the corresponding `kwargs` should look like

```
{
  "prop1": 2,
  "prop2": "seismic"
}
```

and get instantiated by

```
distribution_class(**kwargs)
```

I am optimizing for readibility as opposed to brevity. This requires the class to have an `__init()__` with default named parameters.

The optional `conditional` part of the feature is described next.

## Conditionals

Feature conditionals allow for conditional sampling based on the parent distribution. Here's an example:

```json
{
  "age": {
    "uniform": {
        "low": 14,
        "high": 85,
        "itype": "float",
        "precision": 2
    },
    "conditional": {
      "score": {
        "[14, 65)": {
          "uniform": {
            "low": 5,
            "high": 25,
            "itype": "float",
            "precision": 2
          }
        },
        "[65, *)": {
          "normal": {
            "mean": 35,
            "stddev": 0.5
          }
        },
        "*": {
          "uniform": {
            "low": 5,
            "high": 25,
            "itype": "float",
            "precision": 2
          }
        }
      }
    }
  }
}
```

This describes `score` feature conditioned on the `age` feature. Since the parent distribution is continuous, the conditional subdivisions should be represented by ranges:

- $[a, b]$ the closed interval ${ x \in \mathbb{R}: a \le x \le b }$
- $[a, b)$ the interval ${ x \in \mathbb{R}: a \le x \lt b }$
- $(a, b]$ the interval ${ x \in \mathbb{R}: a \lt x \le b }$
- $(a, b)$ the open interval ${ x \in \mathbb{R}: a \lt x \lt b }$

with `*` representing a catch within the range interval or as the "catch-all" - these are processed in order and an exception is raised if none of the criteria fit.

The task processes each top level feature and then passes the generated value to the conditional which evaluates each range and generates from the distribution which "catches" the generated top level value.

This also is true for discrete probability distributions:

```json
{
  "style": {
    "discrete": {
      "tabs": 234,
      "spaces": 2332,
      "agile": 21,
      "scrum": 128
    },
    "conditional": {
      "score": {
        "tabs": {
          "uniform": {
            "low": 5,
            "high": 25,
            "itype": "float",
            "precision": 2
          }
        },
        "*": {
          "normal": {
            "mean": 12,
            "stddev": 3
          }
        }
      }
    }
  }
}
```

In this case, the conditional `score` feature will sample from the `uniform` distribution if "tabs" is generated for the `style` feature, otherwise the catch-all `*` will sample from the `normal` distribution.

These can be infinitely nested:

```json
{
  "style": {
    "discrete": {
      "tabs": 234,
      "spaces": 2332,
      "agile": 21,
      "scrum": 128
    },
    "conditional": {
      "score": {
        "tabs": {
          "uniform": {
            "low": 5,
            "high": 25,
            "itype": "float",
            "precision": 2
          }
        },
        "*": {
          "normal": {
            "mean": 12,
            "stddev": 3
          }
        }
      }
    },
    "conditional": {
      "accepted": {
        "[14, 65)": {
          "uniform": {
            "low": 5,
            "high": 25,
            "itype": "float",
            "precision": 2
          }
        },
        "[65, *)": {
          "normal": {
            "mean": 35,
            "stddev": 0.5
          }
        },
        "*": {
          "uniform": {
            "low": 5,
            "high": 25,
            "itype": "float",
            "precision": 2
          }
        }
      }
    }
  }
}
```

Notice that in this case, the first conditional required discrete values while the second used ranges. An exception is raised if there is a mismatch.

The main idea is that every Feature has a `distribution` and an optional `conditional`.


