# Mathematical Explanation (v1)

This explains the mathematical logic of the Moonstone skill rating algorithm.

This explanation covers version 1 of the algorithm. This logic may change with subsequent versions.

## Summary
**Player symbols:**
* $r^1$ is new rating of player 1 (`r1_new`). This also indicates player 1 in general.
* $r^2$ is new rating of player 2 (`r2_new`). This also indicates player 2 in general.
* $r^1_{0}$ is old rating of player 1 (`r1_old`)
* $r^2_{0}$ is old rating of player 2 (`r2_old`)

**Without multiplier (v1):**\
```math
r = r_{0} + psb = r_{0} + p_1 \times \dfrac{r_{0}}{\bar{r_{0}}} \times \dfrac{|r_{0} - \neg r_{0}|}{24}
```
wheras:
* $r$ is the new rating (`r_new`)
* $r_{0}$ is the old rating (`r_old`)
* $p$ is the polarity (positive, negative) of the change (`r_polarity`)
* $s$ is the rating scaling (`r_scaling`)
* $b$ is the rating base change/balance (`r_balance`)

**With multiplier (v1x):**\
```math
r = r_{0} + mpsb
```
wheras:
* $m$ is the multiplier of the rating change. Multiplier is user defined.
* all other values are explained above.

**Determining $w$ (`winner`):**\
```math
w = 
\begin{cases}
    \quad -1 & \quad \text{when no result}\\
    \quad 0 & \quad \text{when a tie occurs}\\
    \quad 1 & \quad \text{when $r^{1}$ wins}\\
    \quad 2 & \quad \text{when $r^{2}$ wins}
\end{cases}
```

## Detailed Explanation
### Determining Scaling (`r_scaling`)
1. 
   Compute the mean of both players' old ratings - `r1_old` and `r2_old`:\
  ```math
  \bar{r_{0}} = \dfrac{r^1_{0} + r^2_{0}}{2}
  ```

2. 
   Compute the ratio of the opponent's rating against the mean. This will be the `r_scaling` value of that player.
   
   For player 1, use `r2_old` ($r^2_{0}$). For player 2, use `r1_old` ($r^1_{0}$).\

   ```math
   s_1 = \dfrac{r^2_{0}}{\bar{r_{0}}} \quad \quad s_2 = \dfrac{r^1_{0}}{\bar{r_{0}}}
   ```

### Determining Balance (`r_balance`)

3. Compute the rating change balance as follows:
   
   ```math
   b = 
   \begin{cases}
        \quad \dfrac{|r^1_{0} - r^2_{0}|}{24} \qquad \text{when} \quad |r^1_{0} - r^2_{0}| > 24 \\
        \quad {24} \quad \qquad \text{when}\quad |r^1_{0} - r^2_{0}| \le 24 \\
   \end{cases}
   ```

### Determining Polarity (`r_polarity`)

4. Calculate the polarity of player 1:
   ```math
   p_1 = 
   \begin{cases}
     \quad 1 \space\quad\qquad \text{when} \quad w = 1 \\
     \quad -1 \space\space\qquad \text{when} \quad w = 2 \\
     \quad \dfrac{1}{2} \quad\qquad \text{when} \quad w = 0 \quad \text{and} \quad r^1_{0} \le r^2_{0}\\
     \quad -\dfrac{1}{2} \space\qquad \text{when} \quad w = 0 \quad \text{and} \quad r^1_{0} > r^2_{0}\\
     \quad 0 \quad\qquad\space \text{when} \quad w = -1
   \end{cases}
   ```

5. Calculate the polarity of player 2:
   ```math
   p_2 = 
   \begin{cases}
     \quad 1 \space\quad\qquad \text{when} \quad w = 2 \\
     \quad -1 \space\space\qquad \text{when} \quad w = 1 \\
     \quad \dfrac{1}{2} \quad\qquad \text{when} \quad w = 0 \quad \text{and} \quad r^1_{0} \ge r^2_{0}\\
     \quad -\dfrac{1}{2} \space\qquad \text{when} \quad w = 0 \quad \text{and} \quad r^1_{0} < r^2_{0}\\
     \quad 0 \quad\qquad\space \text{when} \quad w = -1
   \end{cases}
   ```

### Computing Rating Change `r_change`

```math
\Delta{r}_1 = r^1_{0} + p_1 \times \dfrac{r^2_{0}}{\bar{r_{0}}} \times \dfrac{|r^1_{0} - r^2_{0}|}{24}
```

```math
\Delta{r}_2 = r^2_{0} + p_2 \times \dfrac{r^1_{0}}{\bar{r_{0}}} \times \dfrac{|r^1_{0} - r^2_{0}|}{24}
```

### Apply Rating Change (`apply_changes()`)

```math
r_1 = r^1_{0} + \Delta{r}_1 = r^1_{0} + p_1 \times \dfrac{r^2_{0}}{\bar{r_{0}}} \times \dfrac{|r^1_{0} - r^2_{0}|}{24}
```

```math
r_2 = r^2_{0} + \Delta{r}_2 = r^2_{0} + p_1 \times \dfrac{r^1_{0}}{\bar{r_{0}}} \times \dfrac{|r^1_{0} - r^2_{0}|}{24}
```

# Licence
MIT Licence.
