# Post-Gen Tasks

Here are some ideas for some post gen tasks:

1. Blend Columns with additions
   a. Noise
   b. Other features
2. Remove Columns

# Column Blending

Some general principles for column blending:

-   All column changes are additive (we will create a new columns for each op)
-   Can only work with two things at a time (i.e. can work with `Feature` + `Distribution` or `Feature` + `Feature`)
-   Column blending can only work with like columns (i.e. `Discrete` + `Discrete` or `Continuous` + `Continuous`) - otherwise an error is generated

## Operations
Allowed operations for column blending:

### Continuous
1. Add
2. Sub
3. Mult
4. Divide
5. Custom `a op b`

### Discrete
1. ?

# Feature + Distribution

Adding uniform noise to col 2

| col 1        | col 2 | col 3 |
| ------------ | ----- | ----- |
| Juicy Apples | 1.99  | 7     |
| Bananas      | 1.89  | 5234  |

```json
{
  "post": {
    "col 2": {
      "source": {
        "normal": {
          "mean": 36,
          "stddev": 5,
          "precision": 0
        }
      },
      "target": "col2noise",
      "operation": "add"
    }
  }
}
```

| col 1        | col 2 | col 3 | col2noise |
| ------------ | ----- | ----- | --------- |
| Juicy Apples | 1.99  | 7     | 2.33      |
| Bananas      | 1.89  | 5234  | 2.45      |
