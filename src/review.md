# Review of `labfinal.c`

This file explains what each part of `labfinal.c` is doing in simple language.

File reference: [labfinal.c](/Users/ashisrahman/Developer/RAGSystem/src/labfinal.c)

## 1. Header files

Line 1:
`#include <stdio.h>`

- This header is used for input and output.
- In this file it is needed for `printf()`.

Line 2:
`#include <string.h>`

- This header is used for string-related functions.
- In this file it is needed for `strlen()`.

## 2. `#define` constants

Lines 4 to 6:

```c
#define V 5
#define E 5
#define INF 1000000000
```

- `#define` is used to create symbolic constants.
- `V` means number of vertices.
- `E` means number of edges.
- `INF` means a very large value, used like infinity.

Why this is useful:

- Instead of writing `5` again and again, we write `V` or `E`.
- It makes the code easier to read.
- If we change the graph size later, we can change it in one place.

## 3. `typedef struct`

Lines 8 to 12:

```c
typedef struct {
    int src;
    int dest;
    int weight;
} edge_t;
```

- `struct` is used to group related data together.
- Here, one edge has 3 values:
- `src` = source vertex
- `dest` = destination vertex
- `weight` = edge cost

What `typedef` does:

- Normally we would have to write `struct edge_name`.
- With `typedef`, we can directly write `edge_t`.
- So `edge_t` becomes a custom data type.

Example:

```c
edge_t e;
```

This means `e` is a variable of edge structure type.

## 4. Function with return type `int`

Lines 14 to 16:

```c
int max_int(int a, int b) {
    return (a > b) ? a : b;
}
```

- This is a function definition.
- Function name is `max_int`.
- Return type is `int`, so this function must return an integer value.
- It takes two integer parameters: `a` and `b`.
- It returns the bigger one.

About `return`:

- `return` sends a value back from the function.
- Since the return type is `int`, the returned value must also be an integer.

## 5. LCS function

Lines 18 to 34:

```c
int lcs(char *X, char *Y, int m, int n)
```

- This function calculates the LCS length.
- `X` and `Y` are strings.
- `m` is length of `X`.
- `n` is length of `Y`.
- Return type is `int`, because it returns the LCS length.

### 5.1 Parameters

Line 18:

- `char *X` means pointer to character, used as a string.
- `char *Y` also means another string.
- `int m` and `int n` store the lengths.

### 5.2 DP array

Line 19:

```c
int dp[m + 1][n + 1];
```

- This creates a 2D integer array.
- `dp[i][j]` stores the LCS answer for first `i` characters of `X` and first `j` characters of `Y`.

### 5.3 Nested loop

Lines 21 to 31:

- The outer loop moves through string `X`.
- The inner loop moves through string `Y`.
- This is used to fill the DP table step by step.

### 5.4 Base case

Lines 23 to 24:

```c
if (i == 0 || j == 0) {
    dp[i][j] = 0;
}
```

- If one string length is 0, common subsequence length is 0.
- So first row and first column are initialized with 0.

### 5.5 Matching case

Lines 25 to 26:

```c
else if (X[i - 1] == Y[j - 1]) {
    dp[i][j] = dp[i - 1][j - 1] + 1;
}
```

- If current characters are same, we increase previous answer by 1.
- `i - 1` and `j - 1` are used because array indexing starts from 0.

### 5.6 Non-matching case

Lines 27 to 28:

```c
dp[i][j] = max_int(dp[i - 1][j], dp[i][j - 1]);
```

- If characters do not match, take the maximum of:
- top cell
- left cell

### 5.7 Final return

Line 33:

```c
return dp[m][n];
```

- This returns the final LCS length.
- The answer is stored in the bottom-right cell of the table.

## 6. `main` function

Line 36:

```c
int main(void)
```

- This is the starting point of the C program.
- Execution begins from `main`.
- Return type is `int`, so it returns an integer to the operating system.
- `void` inside `main(void)` means this function takes no arguments.

Important:

- Here `void` does not mean the function returns nothing.
- The return type is `int`.
- The `void` here is only for parameter list.

## 7. Edge list

Lines 37 to 43:

```c
edge_t edges[E] = {
    {0, 1, 6},
    {0, 2, 7},
    {1, 3, 5},
    {2, 3, -3},
    {3, 4, 2}
};
```

- This creates an array of `edge_t`.
- Size is `E`, which is 5.
- Each entry stores one graph edge.

Example:

- `{0, 1, 6}` means edge from vertex 0 to vertex 1 with weight 6.

## 8. Distance array

Line 44:

```c
int dist[V];
```

- This creates an integer array named `dist`.
- Size is `V`, which is 5.
- It stores shortest distance from source vertex 0 to every other vertex.

Meaning of `int dist[V]`:

- `int` = data type is integer
- `dist` = array name
- `[V]` = array size is `V`

## 9. Loop variables

Line 45:

```c
int i, j;
```

- These are loop counter variables.
- `i` is usually used for outer loop.
- `j` is usually used for inner loop.

## 10. Sample strings for LCS

Lines 47 to 49:

```c
char X[] = "AGGTAB";
char Y[] = "GXTXAYB";
int ans;
```

- `X` and `Y` are strings for testing the corrected LCS function.
- `ans` will store the returned result.

## 11. Printing text with `printf`

Lines 51 onward contain many `printf()` statements.

- `printf()` is used to show output on the screen.
- In this file, it is used to display answers for Q1, Q2, and Q3.

## 12. Bellman-Ford distance initialization

Lines 63 to 66:

```c
for (i = 0; i < V; i++) {
    dist[i] = INF;
}
dist[0] = 0;
```

- First, all distances are set to `INF`.
- Then source vertex distance is set to 0.
- Source vertex is 0.

Why:

- At the start we assume every node is unreachable.
- Distance from source to itself is always 0.

## 13. Printing initial distance array

Lines 68 to 74:

- This loop prints each value of `dist`.
- If value is `INF`, it prints `INF`.
- Otherwise it prints the integer value.

## 14. Bellman-Ford relaxation

Lines 77 to 87:

```c
for (i = 0; i < V - 1; i++) {
    for (j = 0; j < E; j++) {
        int u = edges[j].src;
        int v = edges[j].dest;
        int w = edges[j].weight;

        if (dist[u] != INF && dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
        }
    }
}
```

- Outer loop runs `V - 1` times.
- Inner loop checks all edges.
- `u`, `v`, `w` are taken from current edge.
- If going from `u` to `v` gives smaller distance, then update `dist[v]`.

This is the main Bellman-Ford idea:

- Repeatedly relax all edges.
- After `V - 1` rounds, shortest paths are found if there is no negative cycle issue in this basic version.

## 15. Printing final distances

Lines 89 to 96:

- After relaxation, the program prints final shortest distances.

## 16. Q2 debugging text

Lines 98 to 119:

- These lines print the logical mistakes in the given LCS code.
- They also print the corrected version as text output.

## 17. Calling a function

Line 121:

```c
ans = lcs(X, Y, (int)strlen(X), (int)strlen(Y));
```

- This is a function call.
- Function name is `lcs`.
- It sends 4 arguments:
- `X`
- `Y`
- length of `X`
- length of `Y`

What happens here:

- `strlen(X)` finds string length.
- `(int)` is type casting. It converts the result to `int`.
- The return value from `lcs()` is stored in `ans`.

## 18. Q3 explanation text

Lines 124 to 132:

- These lines print the answer for 0/1 knapsack theory.
- It explains `dp[i][w]` and the recurrence.

## 19. Returning from `main`

Line 134:

```c
return 0;
```

- This means program finished successfully.
- `0` usually means no error.

## 20. Function definition vs function call

Function definitions in this file:

- Lines 14 to 16: `max_int`
- Lines 18 to 34: `lcs`
- Lines 36 to 135: `main`

Function calls in this file:

- Line 28: `max_int(...)`
- Line 51 onward: many `printf(...)`
- Line 121: `lcs(...)`
- Line 121: `strlen(...)`

Difference:

- Function definition means writing the full function body.
- Function call means using that function.

Example:

Definition:

```c
int max_int(int a, int b) {
    return (a > b) ? a : b;
}
```

Call:

```c
max_int(5, 9);
```

## 21. Return type and `void`

### Return type

- A return type tells what kind of value a function gives back.

Examples from this file:

- `int max_int(...)` returns an integer
- `int lcs(...)` returns an integer
- `int main(void)` returns an integer

### `void`

There are two common uses of `void` in C.

1. `main(void)`

- Means the function takes no parameters.

2. `void show(void)`

- This would mean the function returns nothing and also takes no parameters.

Example:

```c
void show(void) {
    printf("Hello");
}
```

- This kind of function does not return a value.

Important for your file:

- Your current file does not have a `void` return type function.
- But it does use `void` in `main(void)` to show no parameters.

## 22. Main concepts used in this file

The main C concepts used here are:

- Header file
- `#define`
- `typedef struct`
- Array
- 2D array
- Loop
- `if-else`
- Function definition
- Function call
- Return type
- `return`
- String
- Type casting

## 23. Short summary

`labfinal.c` does three main things:

1. Shows Bellman-Ford core components using edge structure, edge list, distance array, and relaxation loop.
2. Fixes the LCS logic and runs the corrected function on sample strings.
3. Prints theory explanation for 0/1 knapsack.
