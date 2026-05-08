#include <stdio.h>
#include <string.h>

#define V 5
#define E 5
#define INF 1000000000

typedef struct {
    int src;
    int dest;
    int weight;
} edge_t;

int max_int(int a, int b) {
    return (a > b) ? a : b;
}

int lcs(char *X, char *Y, int m, int n) {
    int dp[m + 1][n + 1];

    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            } else if (X[i - 1] == Y[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max_int(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[m][n];
}

int main(void) {
    edge_t edges[E] = {
        {0, 1, 6},
        {0, 2, 7},
        {1, 3, 5},
        {2, 3, -3},
        {3, 4, 2}
    };
    int dist[V];
    int i, j;

    char X[] = "AGGTAB";
    char Y[] = "GXTXAYB";
    int ans;

    printf("Part 1: Implementation\n");
    printf("Q1. Bellman-Ford (Core Components Only)\n\n");

    printf("(a) Edge structure:\n");
    printf("edge_t has 3 integer fields: src, dest, weight\n\n");

    printf("(b) Edge list initialization:\n");
    for (i = 0; i < E; i++) {
        printf("Edge %d: %d -> %d  weight = %d\n", i + 1, edges[i].src, edges[i].dest, edges[i].weight);
    }

    printf("\n(c) Distance array initialization:\n");
    for (i = 0; i < V; i++) {
        dist[i] = INF;
    }
    dist[0] = 0;

    for (i = 0; i < V; i++) {
        if (dist[i] == INF) {
            printf("dist[%d] = INF\n", i);
        } else {
            printf("dist[%d] = %d\n", i, dist[i]);
        }
    }

    printf("\n(d) Edge relaxation:\n");
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

    printf("After Bellman-Ford relaxation:\n");
    for (i = 0; i < V; i++) {
        if (dist[i] == INF) {
            printf("dist[%d] = INF\n", i);
        } else {
            printf("dist[%d] = %d\n", i, dist[i]);
        }
    }

    printf("\nPart 2: Debugging\n");
    printf("Q2. LCS\n\n");
    printf("At least 3 logical mistakes are:\n");
    printf("1. Base case should be 0, not 1.\n");
    printf("2. Character compare should use X[i-1] and Y[j-1].\n");
    printf("3. When characters match, +1 should be added.\n\n");

    printf("Corrected code:\n");
    printf("int lcs(char *X, char *Y, int m, int n) {\n");
    printf("    int dp[m+1][n+1];\n");
    printf("    for (int i = 0; i <= m; i++) {\n");
    printf("        for (int j = 0; j <= n; j++) {\n");
    printf("            if (i == 0 || j == 0)\n");
    printf("                dp[i][j] = 0;\n");
    printf("            else if (X[i-1] == Y[j-1])\n");
    printf("                dp[i][j] = dp[i-1][j-1] + 1;\n");
    printf("            else\n");
    printf("                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);\n");
    printf("        }\n");
    printf("    }\n");
    printf("    return dp[m][n];\n");
    printf("}\n");

    ans = lcs(X, Y, (int)strlen(X), (int)strlen(Y));
    printf("\nExample output of corrected LCS = %d\n", ans);

    printf("\nPart 3: Understanding\n");
    printf("Q3. 0/1 Knapsack\n\n");
    printf("(a) dp[i][w] means the maximum value we can get using first i items and capacity w.\n\n");
    printf("(b) Transition explanation:\n");
    printf("dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w - weight[i]])\n");
    printf("If we do not take the item, answer stays dp[i-1][w].\n");
    printf("If we take the item, we add its value and reduce capacity by its weight.\n");
    printf("Then we take the maximum of these two choices.\n");
    printf("This is called 0/1 knapsack because each item is either taken once or not taken.\n");

    return 0;
}
//codex resume 019dacc1-962e-72d0-a5f2-ce7a8b7c551b
