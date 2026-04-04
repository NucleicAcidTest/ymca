import bisect

def main():
    def get_tokens():
        try:
            while True:
                for p in input().split():
                    yield int(p)
        except EOFError:
            return

    tokens = get_tokens()
    
    try:
        numOfBox = next(tokens)
        prepTime = next(tokens)
        money = next(tokens)
        M = next(tokens)
        S = next(tokens)
    except StopIteration:
        return

    machines = [(0, prepTime)]
    for _ in range(M):
        mTime = next(tokens)
        mCost = next(tokens)
        machines.append((mCost, mTime))

    shops = [(0, 0)]
    for _ in range(S):
        sNum = next(tokens)
        sCost = next(tokens)
        shops.append((sCost, sNum))

    machines.sort(key=lambda x: x[0])
    
    m_costs = []
    m_min_times = []
    
    current_min_time = float('inf')
    for cost, time in machines:
        if time < current_min_time:
            current_min_time = time
        m_costs.append(cost)
        m_min_times.append(current_min_time)

    ans = float('inf')
    
    for sCost, sNum in shops:
        if sCost > money:
            continue
        
        rem_money = money - sCost
        boxes_to_make = max(0, numOfBox - sNum)
        
        if boxes_to_make == 0:
            ans = 0
            break
            
        pos = bisect.bisect_right(m_costs, rem_money) - 1
        if pos >= 0:
            best_time = m_min_times[pos]
            time_taken = boxes_to_make * best_time
            if time_taken < ans:
                ans = time_taken

    print(ans % 1000007)

if __name__ == '__main__':
    main()