from itertools import combinations
from pathlib import Path
import csv
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / 'results'
OUT.mkdir(exist_ok=True)


def greedy(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):
        q, amount = divmod(amount, coin)
        count += q
    return count if amount == 0 else None


def optimal(coins, amount):
    dp = [0] + [float('inf')] * amount
    for x in range(1, amount + 1):
        dp[x] = min((dp[x-c] + 1 for c in coins if c <= x), default=float('inf'))
    return int(dp[amount]) if dp[amount] != float('inf') else None


def experiment(max_coin=12, max_amount=40):
    rows = []
    for a, b in combinations(range(2, max_coin+1), 2):
        coins = (1, a, b)
        for amount in range(1, max_amount+1):
            g, o = greedy(coins, amount), optimal(coins, amount)
            if g != o:
                rows.append({'coins': str(coins), 'amount': amount, 'greedy': g, 'optimal': o, 'gap': g-o})
    return rows


if __name__ == '__main__':
    rows = experiment()
    path = OUT / 'counterexamples.csv'
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['coins', 'amount', 'greedy', 'optimal', 'gap'])
        writer.writeheader()
        writer.writerows(rows)

    print('反例总数：', len(rows))
    print('前10个反例：')
    for row in rows[:10]:
        print(row)
    print('数据保存位置：', path)

    if rows:
        gaps = [r['gap'] for r in rows]
        plt.figure(figsize=(7, 4))
        plt.hist(gaps, bins=range(1, max(gaps)+3), align='left', rwidth=0.8)
        plt.xlabel('Extra coins used by greedy')
        plt.ylabel('Number of counterexamples')
        plt.title('Greedy vs Optimal: Failure Gap Distribution')
        plt.tight_layout()
        plt.savefig(OUT / 'failure_gaps.png', dpi=200)
        plt.close()
