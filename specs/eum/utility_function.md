# Utility Function Formulation

The instantaneous utility derived by a user from the selection of a single meal (Recipe $i$), denoted $U_i$, is formulated within the framework of a **Random Utility Model (RUM)**. This structure allows us to capture the heterogeneity in consumer preference, the non-linear trade-offs between attributes, and the necessary idiosyncratic shock.

The total utility, $U_i$, is defined as a weighted additive combination of distinct, non-linear **Constant Elasticity of Substitution (CES)** sub-utility functions, where the weights ($w_k$) represent the user's stated and revealed preference for each consumption category $k$.

$$
    U_i = V_i + \epsilon_i
$$
Where $V_i$ is the observable, deterministic component of utility (the focus of the EUM), and $\epsilon_i$ is the unobserved, stochastic component (the preference shock).

## Deterministic Utility Component

The deterministic utility component is a weighted sum of the primary sub-utility categories: **Convenience ($Conv$ - combining Cost and Time)**, Nutrition ($N$), and Taste/Aesthetics ($A$). This structure allows the crucial trade-off between money and time to be explicitly modeled by a single elasticity parameter.

$$
    V_i = w_{Conv} \cdot U_{Conv}(\mathbf{X}_{i, Conv}) + w_{N} \cdot U_{N}(\mathbf{X}_{i, N}) + w_{A} \cdot U_{A}(\mathbf{X}_{i, A})
$$

## Definition of Sub-Utility Functions ($U_k$)

Each multi-attribute sub-utility $U_k$ is modeled as a CES aggregator of its constituent attributes $\mathbf{X}_{i, j, k}$. This allows the elasticity of substitution ($\sigma_k = 1/(1-\rho_k)$) to vary across categories.

$$
    U_k(\mathbf{X}_{i, k}) = \left[\sum_{j=1}^{J_k} \alpha_{j, k}(\mathbf{X}_{i, j, k})^{\rho_k}\right]^{1/\rho_k}
$$

| **Category** ($k$) | **Sub-Utility** ($U_k$) | **Attributes** ($\mathbf{X}_{i, j, k}$) | **Key Parameter** |
| :--- | :--- | :--- | :--- |
| **Convenience** ($Conv$) | Models the higher-order trade-off between the disutilities of **Cost** ($\text{Cost}_i$) and **Time** ($\text{Time}_i$). | $\mathbf{X}_{i, C, Conv}$: Total ingredient cost (dollars) $\mathbf{X}_{i, T, Conv}$: Total preparation and cook time (minutes) | $\rho_{Conv}$: **Elasticity of substitution between money and time** (the willingness to pay to save a minute). |
| **Nutrition** ($N$) | Models the fulfillment of health goals beyond minimum constraints. | $\mathbf{X}_{i, N}$: Vector of essential metrics (e.g., $\text{Protein}_i$, $\text{Fiber}_i$, $\text{Sugar}_i$). | $\rho_{N}$: Substitution elasticity among core nutritional elements. |
| **Taste** ($A$) | Models preference for flavor profiles and cuisine enjoyment. | $\mathbf{X}_{i, A}$: Vector of categorical variables (e.g., $\text{Cuisine Type}_i$, $\text{Spice Level}_i$). | $\rho_{A}$: Substitution elasticity among aesthetic/flavor attributes. |